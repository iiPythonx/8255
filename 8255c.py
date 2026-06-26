# Copyright (c) 2026 iiPython

# Modules
import re
from sys import argv
from pathlib import Path
from time import perf_counter
from dataclasses import dataclass

from core import INSTRUCTIONS, REGISTERS

# Exceptions
class CompilationError(Exception):
    def __init__(self, offset: int, section: "Section", message: str) -> None:
        target_line = offset + section.start
        target_code = section.file.lines[target_line]
        
        print(f"\033[31m8255c: compilation issue")
        print("=" * 50, end = "\033[0m\n\n")
        print(f"\033[90mLine \033[33m{target_line}\033[90m in \033[33m{section.file.path}\033[90m is invalid:")
        print(f"  > \033[33m{target_code}\033[31m\n")
        print(f"E: \033[4m{message}\033[24m\033[0m")
        exit(1)

# Compilation
PRELOAD_REGEX = re.compile(rb"(\w+):\s+\"(.+)\"")
INSTRUCTS_BY_VERB = {v.opcode: (k, v) for k, v in INSTRUCTIONS.items()}

def generate_preload(section: "Section") -> tuple[bytearray, int]:
    store, offset = bytearray([0] * (0x4000 - 0x2000 + 1)), 0
    for index, line in enumerate(section.lines):
        line_match = PRELOAD_REGEX.match(line.encode() + b"\0")
        if line_match is None:
            raise CompilationError(index, section, "Invalid line inside preload section!")

        key, value = line_match.groups()
        for byte in value:
            store[offset] = byte
            offset += 1

    return store, index

def generate_snapshot(sections: dict[str, "Section"]) -> bytearray:
    components = {"code": [bytearray([0] * (0x2000 - 0x0100 + 1)), 0]}
    def write(item: int | bytes) -> None:
        array, index = components["code"]
        if isinstance(item, int):
            array[index] = item
            components["code"][1] += 1
            return

        array[index : index + len(item)] = item
        components["code"][1] += len(item)

    print(f"OFFSET | {'INSTRUCTION':<30} | BYTECODE")
    print("-" * 80)

    subroutines: dict[str, int] = {}
    for name, section in sections.items():
        if name == "preload":
            components["data"] = generate_preload(section)
            continue

        subroutines[name] = components["code"][1]
        for index, line in enumerate(section.lines):
            arguments = line.split(",")
            instruction, *arguments = [a.strip() for a in arguments[0].split() + arguments[1:]]

            # Ensure instruction is valid
            id, instruction = INSTRUCTS_BY_VERB.get(instruction.upper()) or (None, None)
            if instruction is None:
                raise CompilationError(index, section, "Invalid instruction!")

            write(id)

            # Confirm argument types
            total_size = 1
            for aindex, argument in enumerate(instruction.args):
                target = arguments[aindex]
                if argument.size == 2:

                    # This should either be a memory address (preferred), or a
                    # direct value (loadi), or lastly a subroutine address
                    if target.startswith("&"):
                        if target[1:] not in subroutines:
                            raise CompilationError(index, section, "Reference to unknown subroutine!")

                        write(subroutines[target[1:]].to_bytes(2))
                    
                    elif target.startswith("0x"):
                        write(int(target, 16).to_bytes(2))

                    else:
                        write(int(target).to_bytes(2))

                elif argument.size == 1:
                    register_id = REGISTERS[target.upper()]
                    if register_id is None:
                        raise CompilationError(index, section, "Reference to unknown register!")

                    write(register_id)

                total_size += argument.size

            current_array, current_index = components["code"]
            print(f"0x{current_index:04x} | {line:<30} | {current_array[current_index - total_size:current_index].hex(' ', 1)}")

    return components["code"][0]

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

    file = File(path, [line.strip() for line in path.read_text().splitlines() if line.strip()])
    for index, line in enumerate(file.lines):
        if line.startswith("//"):
            continue

        if line[0] == ".":
            push_section()
            active_section = Section(line[1:], index + 1, 0, file, [])

        else:

            # TODO: This is naive. In the future we need to split only if the found
            # substring isn't inside a string block. i.e. a preload section.
            active_section.lines.append(line.split("//")[0].strip())

    push_section()
    return sections

if __name__ == "__main__":
    if len(argv) < 2:
        exit("8255c: missing program file")

    file = Path(argv[1])
    if not file.is_file():
        exit("8255c: file does not exist")

    sections = parse_sections_from_file(file)

    start_time = perf_counter()
    file.with_suffix(".bin").write_bytes(generate_snapshot(sections))
    print(f"\nCompiled in {(perf_counter() - start_time) * 1000:.2f}ms to {file.with_suffix('.bin')}")
