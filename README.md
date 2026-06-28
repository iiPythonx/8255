<p align = "center">
    <picture>
        <source media = "(prefers-color-scheme: dark)" srcset = ".github/logo_dark.png">
        <source media = "(prefers-color-scheme: light)" srcset = ".github/logo_light.png">
        <img alt = "8255 logo" src = ".github/logo_dark.png">
    </picture>
    <hr>
</p>

A 16-bit CPU with 16 KiB of RAM, for playing around with.

## Installation

```bash
git clone git@github.com:iiPythonx/8255
cd 8255

# Activate environment
uv venv
source .venv/bin/activate
uv pip install -e .

# Run the UNIX epoch example
8255asm examples/epoch.asm
8255emu examples/epoch.bin
```

## Features

- Complete [ISA](https://en.wikipedia.org/wiki/Instruction_set_architecture) covering memory operations, math, and branching
- 9 general purpose registers (R1 - R9) with 3 hardware registers (LC, CR, & SP)
- [MMIO](https://en.wikipedia.org/wiki/Memory-mapped_I/O_and_port-mapped_I/O) for [drivers](#drivers) on the 0x0013 - 0x0100 range
- Subroutine and stack support, including `PSH`, `POP`, `CAL`, & `RET`

## Specifications

Last updated: June 28th, 2026  
Version: 1.2

### Memory

```js
16 KiB / 16386 B

0x0000 - 0x0100: REGISTERS
0x0100 - 0x2000: CODE
0x2000 - 0x3000: DATA
0x3000 - 0x4000: STACK
```

### Registers

```js
0x0: R1
0x1: R2
0x2: R3
0x3: R4
0x4: R5
0x5: R6
0x6: R7
0x7: R8
0x8: R9
0xA: LC (LINE COUNTER)
0xB: CR (COMPARE RESULT)
0xC: SP (STACK POINTER)
```

### Instructions

```js
R = CPU REG
A = MEM ADDR
V = VALUE (ASM EMBEDDED)

0x00: HLT     (HALT)
0x01: LDI R V (LOAD IMMEDIATE)
0x02: LBA A A (LOAD BYTE ADDRESS)
0x03: LBR R R (LOAD BYTE REGISTER)
0x04: LWA A A (LOAD WORD ADDRESS)
0x05: LWR R R (LOAD WORD REGISTER)
0x06: SBA A A (STORE BYTE ADDRESS)
0x07: SBR R R (STORE BYTE REGISTER)
0x08: SWA A A (STORE WORD ADDRESS)
0x09: SWR R R (STORE WORD REGISTER)
0x0A: ADD R R (ADD)
0x0B: SUB R R (SUBTRACT)
0x0C: MUL R R (MULTIPLY)
0x0D: DIV R R (DIVIDE)
0x0E: POW R R (POWER)
0x0F: CMP R R (COMPARE)
0x10: JEQ A   (JUMP EQUAL)
0x11: JNE A   (JUMP NOT EQUAL)
0x12: JGT A   (JUMP GREATER THAN)
0x13: JLT A   (JUMP LESS THAN)
0x14: JGE A   (JUMP GREATER EQUAL)
0x15: JLE A   (JUMP LESS EQUAL)
0x16: JMP A   (JUMP)
0x17: CAL A   (CALL SUBROUTINE)
0x18: RET     (RETURN FROM SUBROUTINE)
0x19: PSH R   (PUSH REGISTER TO STACK)
0x1A: POP R   (POP STACK TO REGISTER)
```

### Drivers

See the [vm/drivers](./src/x8255/vm/drivers) tree for a list of drivers.  
It's up to the driver maintainer to produce accurate documentation regarding their use.

## Inspiration

8255 is based on [BASIC](https://en.wikipedia.org/wiki/BASIC) and [Assembly](https://en.wikipedia.org/wiki/Assembly_language).  
The CPU itself has no real backing inspiration, it's just a normal 16-bit chip w/ RAM.

## Copyright

© 2024-2026 Benjamin "iiPython" O'Brien, see [LICENSE.txt](LICENSE.txt) for details.
