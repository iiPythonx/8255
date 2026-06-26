# Copyright (c) 2026 iiPython

import inspect
from sys import argv
from pathlib import Path
from time import perf_counter

from core.emulate import Emu8255
from core.compile import parse_sections_from_file, generate_snapshot

# Usage
def usage() -> None:
    print(inspect.cleandoc("""
    8255 - A 16-bit CPU with 16 KiB of RAM.
       https://github.com/iiPythonx/8255

    8255 <command> <file>

    Available commands:
      - 8255 assemble <file.asm>  | assemble an 8255 source file
      - 8255 run <file.bin>       | emulate a compiled 8255 executable

    Available options (for assemble):
        -Z, --zero-jump (default: OFF) | auto jump to the .main label on launch by
                                       | inserting a jump instruction at addr 0x0

    Copyright (c) 2024-2026 iiPython
    """))
    exit()

# Initialization
if len(argv) < 3:
    usage()

file = Path(argv[2])
if not file.is_file():
    exit("8255: file does not exist")

# Handle CLI
match argv[1]:
    case "assemble":
        sections = parse_sections_from_file(file)

        # Build snapshot
        start_time = perf_counter()
        snapshot = generate_snapshot(
            sections,
            zero_jump = any(a in {"--zero-jump", "-Z"} for a in argv)
        )
        elapsed = perf_counter() - start_time

        # Write to binary file and show status
        file.with_suffix(".bin").write_bytes(snapshot)
        print(f"Compiled in {elapsed * 1000:.2f}ms to {file.with_suffix('.bin')}")

    case "run":
        data = file.read_bytes()
        code_range = 0x2000 - 0x0100

        # Setup emulation
        system = Emu8255()
        system.write_range(data[:code_range], 0x0100)
        system.write_range(data[code_range:], 0x2000)
        while True:
            system.step()

    case _ as e:
        usage()
