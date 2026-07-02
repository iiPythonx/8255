# Copyright (c) 2026 iiPython

from dataclasses import dataclass

class Register:
    size = 1

class Address:
    size = 2

class Value:
    size = 2

type Argument = Register | Address | Value

@dataclass
class Instruction:
    args:   list[Argument]
    opcode: str
    name:   str

INSTRUCTIONS = {
    0x00: Instruction([], "HLT", "HALT"),
    0x01: Instruction(
        [Register(), Value()],
        "LDI",
        "LOAD IMMEDIATE"
    ),
    0x02: Instruction(
        [Register(), Address()],
        "LBA",
        "LOAD BYTE ADDRESS"
    ),
    0x03: Instruction(
        [Register(), Register()],
        "LBR",
        "LOAD BYTE REGISTER"
    ),
    0x04: Instruction(
        [Register(), Address()],
        "LWA",
        "LOAD WORD ADDRESS"
    ),
    0x05: Instruction(
        [Register(), Register()],
        "LWR",
        "LOAD WORD REGISTER"
    ),
    0x06: Instruction(
        [Register(), Address()],
        "SBA",
        "STORE BYTE ADDRESS"
    ),
    0x07: Instruction(
        [Register(), Register()],
        "SBR",
        "STORE BYTE REGISTER"
    ),
    0x08: Instruction(
        [Register(), Address()],
        "SWA",
        "STORE WORD ADDRESS"
    ),
    0x09: Instruction(
        [Register(), Register()],
        "SWR",
        "STORE WORD REGISTER"
    ),
    0x0A: Instruction(
        [Register(), Register()],
        "ADD",
        "ADD"
    ),
    0x0B: Instruction(
        [Register(), Register()],
        "SUB",
        "SUBTRACT"
    ),
    0x0C: Instruction(
        [Register(), Register()],
        "MUL",
        "MULTIPLY"
    ),
    0x0D: Instruction(
        [Register(), Register()],
        "DIV",
        "DIVIDE"
    ),
    0x0E: Instruction(
        [Register(), Register()],
        "POW",
        "POWER"
    ),
    0x0F: Instruction(
        [Register(), Register()],
        "CMP",
        "COMPARE"
    ),
    0x10: Instruction(
        [Address()],
        "JEQ",
        "JUMP EQUAL"
    ),
    0x11: Instruction(
        [Address()],
        "JNE",
        "JUMP NOT EQUAL"
    ),
    0x12: Instruction(
        [Address()],
        "JGT",
        "JUMP GREATER THAN"
    ),
    0x13: Instruction(
        [Address()],
        "JLT",
        "JUMP LESS THAN"
    ),
    0x14: Instruction(
        [Address()],
        "JGE",
        "JUMP GREATER EQUAL"
    ),
    0x15: Instruction(
        [Address()],
        "JLE",
        "JUMP LESS EQUAL"
    ),
    0x16: Instruction(
        [Address()],
        "JMP",
        "JUMP"
    ),
    0x17: Instruction(
        [Address()],
        "CAL",
        "CALL SUBROUTINE"
    ),
    0x18: Instruction([], "RET", "RETURN FROM SUBROUTINE"),
    0x19: Instruction(
        [Register()],
        "PSH",
        "PUSH REGISTER TO STACK"
    ),
    0x1A: Instruction(
        [Register()],
        "POP",
        "POP STACK TO REGISTER"
    ),
    0x1B: Instruction(
        [Register()],
        "INC",
        "INCREMENT"
    ),
    0x1C: Instruction(
        [Register()],
        "DEC",
        "DECREMENT"
    ),
    0x1D: Instruction(
        [Register(), Register()],
        "MOV",
        "COPY REGISTER"
    )
}

class CPURegister:
    def __init__(self, name: str, id: int, address: int) -> None:
        self.name, self.id, self.address = name, id, address

REGISTERS = [
    CPURegister("R1", 0x0, 0x00),
    CPURegister("R2", 0x1, 0x02),
    CPURegister("R3", 0x2, 0x04),
    CPURegister("R4", 0x3, 0x06),
    CPURegister("R5", 0x4, 0x08),
    CPURegister("R6", 0x5, 0x0A),
    CPURegister("R7", 0x6, 0x0C),
    CPURegister("R8", 0x7, 0x0E),
    CPURegister("R9", 0x8, 0x10),
    CPURegister("LC", 0xA, 0x12),
    CPURegister("CR", 0xB, 0x14),
    CPURegister("SP", 0xC, 0x16)
]

class MemoryAddress:
    def __init__(self, start: int, end: int) -> None:
        self.start, self.end, self.size = start, end, end - start

class Addresses:
    REGISTERS = MemoryAddress(0x0000, 0x0100)
    CODE      = MemoryAddress(0x0100, 0x2000)
    DATA      = MemoryAddress(0x2000, 0x3000)
    STACK     = MemoryAddress(0x3000, 0x4000)
