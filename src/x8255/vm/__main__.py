# Copyright (c) 2026 iiPython

from pathlib import Path

from x8255.cli import p, cexit
from x8255.isa import Addresses
from x8255.vm.core import Emu8255

def main() -> None:
    p.add_argument("-N", "--no-drivers", action = "store_true", help = "disable all drivers", default = False)
    p.add_argument("-d", "--drivers", help = "enabled list of drivers, default is stdio", default = "stdio")
    p.add_argument("executable", type = Path, help = "path to compiled executable")

    args = p.parse_args()

    # Confirm file
    file = Path(args.executable)
    if not file.is_file():
        cexit("The provided file path does not exist.")

    bytecode = file.read_bytes()

    # Setup emulation
    system = Emu8255(args.drivers.split(",") if not args.no_drivers else [])
    system.write_range(bytecode[:Addresses.CODE.size], Addresses.CODE.start)
    system.write_range(bytecode[Addresses.CODE.size:], Addresses.CODE.end)

    # System loop
    while True:
        system.step()
