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

# Run the UNIX epoch example
python3 -m core assemble examples/epoch.asm
python3 -m core run examples/epoch.bin
```

## Specifications

Last updated: JUNE 26, 2026  
Version: 1.1

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
0xA: LC (LINE COUNTER)
0xB: CR (COMPARE RESULT)
0xC: SP (STACK POINTER)
```

### Instructions

```js
A = CPU REG
R = MEM ADDR

0x00: HLT     (HALT)
0x01: LDM R A (LOAD MEMORY)
0x02: LDI R V (LOAD IMMEDIATE)
0x03: STR R A (STORE MEMORY)
0x04: ADD R R (ADD)
0x05: SUB R R (SUBTRACT)
0x06: MUL R R (MULTIPLY)
0x07: DIV R R (DIVIDE)
0x08: POW R R (POWER)
0x09: CMP R R (COMPARE)
0x0A: JEQ A   (JUMP EQUAL)
0x0B: JNE A   (JUMP NOT EQUAL)
0x0C: JGT A   (JUMP GREATER THAN)
0x0D: JLT A   (JUMP LESS THAN)
0x0E: JGE A   (JUMP GREATER EQUAL)
0x0F: JLE A   (JUMP LESS EQUAL)
0x10: JMP A   (JUMP)
0x11: CAL A   (CALL SUBROUTINE)
0x12: RET     (RETURN FROM SUBROUTINE)
0x13: PSH R   (PUSH REGISTER TO STACK)
0x14: POP R   (POP STACK TO REGISTER)
```

### Drivers

See the [core/drivers](./core/drivers) tree for a list of drivers.  
It's up to the driver maintainer to produce accurate documentation regarding their use.

## Inspiration

8255 is based on [BASIC](https://en.wikipedia.org/wiki/BASIC) and [Assembly](https://en.wikipedia.org/wiki/Assembly_language).  
The CPU itself has no real backing inspiration, it's just a normal 16-bit chip w/ RAM.

## Copyright

© 2024-2026 Benjamin "iiPython" O'Brien, see [LICENSE.txt](LICENSE.txt) for details.
