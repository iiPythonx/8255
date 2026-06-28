# Copyright (c) 2026 iiPython

from pathlib import Path

from x8255.cli import p, cexit
from x8255.vm.core import Emu8255

CODE_SECTION_RANGE = 0x2000 - 0x0100

def main() -> None:
    p.add_argument("executable", type = Path, help = "path to compiled executable")
    
    # Confirm file
    file = Path(p.parse_args().executable)
    if not file.is_file():
        cexit("The provided file path does not exist.")

    bytecode = file.read_bytes()

    # Setup emulation
    system = Emu8255()
    system.write_range(bytecode[:CODE_SECTION_RANGE], 0x0100)
    system.write_range(bytecode[CODE_SECTION_RANGE:], 0x2000)

    # System loop
    while True:
        system.step()
