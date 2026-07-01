# Copyright (c) 2026 iiPython

from argparse import ArgumentParser

p = ArgumentParser(
    description = "A 16-bit CPU with 16 KiB of RAM.",
    epilog = "Copyright (c) 2024-2026 iiPython"
)
p.add_argument("-d", "--drivers", help = "enabled list of drivers, default: stdio", default = "stdio")
p.add_argument("-N", "--no-drivers", action = "store_true", help = "disable all drivers", default = False)

def cexit(message: str) -> None:
    print(message)
    exit(1)
