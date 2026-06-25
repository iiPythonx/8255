# Copyright (c) 2026 iiPython

# Modules
import re
from sys import argv
from pathlib import Path
from dataclasses import dataclass

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

def generate_snapshot(sections: dict[str, "Section"]) -> bytes:
    components = {"code": (bytearray([0] * (0x2000 - 0x0100 + 1)), 0)}

    # Fetch string mapping / preload data
    if "preload" in sections:
        components["data"] = generate_preload(sections["preload"])

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
        if line[0] == ".":
            push_section()
            active_section = Section(line[1:], index + 1, 0, file, [])

        else:
            active_section.lines.append(line)

    push_section()
    return sections

if __name__ == "__main__":
    if len(argv) < 2:
        exit("8255c: missing program file")

    file = Path(argv[1])
    if not file.is_file():
        exit("8255c: file does not exist")

    sections = parse_sections_from_file(file)
    print(generate_snapshot(sections))
