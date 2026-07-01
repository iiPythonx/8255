# Copyright (c) 2026 iiPython

# Modules
import re
from pathlib import Path
from dataclasses import dataclass

from x8255.isa import INSTRUCTIONS, REGISTERS, Addresses

# Typing
class Component:
    bytes: bytearray
    index: int

    def __init__(self, bytes: bytearray = bytearray(), index: int = 0) -> None:
        self.bytes, self.index = bytes, index

# Exceptions
class CompilationError(Exception):
    def __init__(self, offset: int, section: "Section", message: str) -> None:
        target_line, line_track = offset + section.start, 0

        # Start reiterating over the file
        file_lines = section.file.path.read_text().splitlines()
        for index, line in enumerate(file_lines):
            actual_line = line.strip() and line.strip()[0] != ";"
            if actual_line:
                line_track += 1

            if target_line == line_track:
                target_line = index + 1  # +1 for label
                break

        target_code = file_lines[target_line].strip()
        
        print("\n\033[31m8255c: compilation issue\n")
        print(f"\033[33m{section.file.path}:{target_line + 1}\033[90m in label \033[33m{section.name}\033[90m is invalid:")
        print(f"  > \033[33m{target_code}\033[31m\n")
        print(f"E: \033[4m{message}\033[24m\033[0m")
        exit(1)

# Compilation
PRELOAD_REGEX = re.compile(rb"\.(\w+)\s+\"(.+)\"")
LABEL_REGEX = re.compile(r"^\w+\:")

REGISTERS_BY_NAME = {reg.name: reg for reg in REGISTERS}
INSTRUCTS_BY_VERB = {v.opcode: (k, v) for k, v in INSTRUCTIONS.items()}

def generate_preload(section: "Section") -> tuple[Component, dict[str, int]]:
    store, offset, strmap, index = bytearray([0] * Addresses.DATA.size), 0, {}, 0
    for index, line in enumerate(section.lines):
        line_match = PRELOAD_REGEX.match(line.encode())
        if line_match is None:
            raise CompilationError(index, section, "Invalid line inside preload section!")

        # Store in string mapping
        key, value = line_match.groups()
        strmap[key.decode()] = Addresses.DATA.start + offset

        # Place in block
        value += b"\0"
        store[offset : offset + len(value)] = value.decode("unicode-escape").encode("utf-8")
        offset += len(value)

    return Component(store, index), strmap

def generate_snapshot(sections: dict[str, "Section"], zero_jump: bool = False) -> bytearray:
    components, strmap = {"code": Component(bytearray([0] * Addresses.CODE.size))}, {}
    def write(item: int | bytes) -> None:
        index = components["code"].index
        if isinstance(item, int):
            components["code"].bytes[index] = item
            components["code"].index += 1
            return

        components["code"].bytes[index : index + len(item)] = item
        components["code"].index += len(item)

    def log(line: str, total_size: int):
        current_array, current_index = components["code"].bytes, components["code"].index
        print(f"\033[90m0x{current_index - total_size:04x}   \033[32m{line:<30}   \033[90m{current_array[current_index - total_size:current_index].hex(' ', 1)}\033[0m")

    print(f"\033[4m\033[34mOFFSET   {'INSTRUCTION':<30}   {'BYTECODE':<20}\033[0m")

    if zero_jump:
        write(INSTRUCTS_BY_VERB["JMP"][0])
        write(int(0).to_bytes(2))
        log("jmp main", 3)

    subroutines: dict[str, int] = {}
    for name, section in sections.items():
        if name == "preload":
            components["data"], strmap = generate_preload(section)
            continue

        subroutines[name] = components["code"].index
        for index, line in enumerate(section.lines):
            arguments = line.split(",")
            instruction, *arguments = [a.strip() for a in arguments[0].split() + arguments[1:]]

            # Ensure instruction is valid
            id, instruction = INSTRUCTS_BY_VERB.get(instruction.upper()) or (None, None)
            if instruction is None or id is None:
                raise CompilationError(index, section, "Invalid instruction!")

            write(id)

            # Confirm argument types
            total_size = 1
            for aindex, argument in enumerate(instruction.args):
                target = arguments[aindex]
                if argument.size == 2:
                    if target.startswith("0x"):
                        write(int(target, 16).to_bytes(2))

                    elif target.startswith("&") and target[1:] in strmap:
                        write(strmap[target[1:]].to_bytes(2))

                    else:
                        try:
                            write(int(target).to_bytes(2))

                        except ValueError:
                            if target not in subroutines:
                                raise CompilationError(index, section, "Reference to unknown subroutine!")

                            write(subroutines[target].to_bytes(2))

                elif argument.size == 1:
                    register_id = REGISTERS_BY_NAME[target.upper()]
                    if register_id is None:
                        raise CompilationError(index, section, "Reference to unknown register!")

                    write(register_id.id)

                total_size += argument.size

            log(line, total_size)

    # Update zero jump to match correct main address
    print()
    if "main" in subroutines and zero_jump:
        components["code"].bytes[1:3] = subroutines["main"].to_bytes(2)
        print(f"Zero-jump: \033[32mmain\033[0m is at \033[32m0x{subroutines['main']:04x}\033[0m")

    # Update data block if terminate exists
    if "terminate" in subroutines:
        components["data"].bytes[0x0700] = subroutines["terminate"]

    return components["code"].bytes + components.get("data", Component()).bytes

# Parsing
@dataclass
class File:
    path:  Path
    lines: list[str]

@dataclass
class Section:
    name:  str
    start: int
    end:   int
    file:  File
    lines: list[str]

def parse_sections_from_file(path: Path) -> dict[str, Section]:
    sections, active_section = {}, None
    def push_section() -> None:
        if active_section is not None:
            active_section.end = index - 1
            sections[active_section.name] = active_section

    clean_lines = [line.strip() for line in path.read_text().splitlines()]

    # Handle individual lines
    file = File(path, [line for line in clean_lines if line and line[0] != ";"])
    for index, line in enumerate(file.lines):
        if LABEL_REGEX.match(line):
            push_section()
            active_section = Section(line[:-1], index + 1, 0, file, [])

        elif active_section:

            # TODO: This is naive. In the future we need to split only if the found
            # substring isn't inside a string block. i.e. a preload section.
            active_section.lines.append(line.split(";")[0].strip())

    push_section()
    return sections
