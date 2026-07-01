# Copyright (c) 2026 iiPython

import gzip
from pathlib import Path
from time import perf_counter

from x8255.cli import p, cexit
from x8255.asm.core import parse_sections_from_file, generate_snapshot

def main() -> None:
    p.add_argument("source", type = Path, help = "path to source code")
    p.add_argument("-G", "--gzip", action = "store_true", default = False, help = "compress output with gzip")
    p.add_argument("-Z", "--zero-jump", action = "store_true", default = False, help = "auto jump to the .main label on launch")
    args = p.parse_args()

    # Confirm file
    file = Path(args.source)
    if not file.is_file():
        cexit("The provided file path does not exist.")

    # Parse sections
    sections = parse_sections_from_file(file)

    # Build snapshot
    start_time = perf_counter()
    snapshot = generate_snapshot(
        sections,
        zero_jump = args.zero_jump
    )
    elapsed = perf_counter() - start_time

    # Compression
    if args.gzip:
        snapshot = gzip.compress(snapshot)

    # Write to binary file and show status
    file.with_suffix(".bin").write_bytes(snapshot)
    print(f"Compiled in \033[32m{elapsed * 1000:.2f}ms\033[0m to \033[32m{file.with_suffix('.bin')}\033[0m")
