# Copyright (c) 2026 iiPython

from dataclasses import dataclass

@dataclass
class Argument:
    name: str
    size: int

class Register(Argument):
    def __init__(self, name: str) -> None:
        super().__init__(name = name, size = 1)

class Address(Argument):
    def __init__(self, name: str) -> None:
        super().__init__(name = name, size = 2)

class Value(Argument):
    def __init__(self, name: str) -> None:
        super().__init__(name = name, size = 2)

@dataclass
class Instruction:
    args:   list[Argument]
    opcode: str
    name:   str

INSTRUCTIONS = {
    0x00: Instruction([], "HLT", "HALT"),
    0x01: Instruction(
        [Register("TO LOAD INTO"), Value("TO LOAD")],
        "LDI",
        "LOAD IMMEDIATE"
    ),
    0x02: Instruction(
        [Register("TO LOAD INTO"), Address("TO LOAD FROM")],
        "LBA",
        "LOAD BYTE ADDRESS"
    ),
    0x03: Instruction(
        [Register("TO LOAD INTO"), Register("TO LOAD FROM")],
        "LBR",
        "LOAD BYTE REGISTER"
    ),
    0x04: Instruction(
        [Register("TO LOAD INTO"), Address("TO LOAD FROM")],
        "LWA",
        "LOAD WORD ADDRESS"
    ),
    0x05: Instruction(
        [Register("TO LOAD INTO"), Register("TO LOAD FROM")],
        "LWR",
        "LOAD WORD REGISTER"
    ),
    0x06: Instruction(
        [Register("TO LOAD FROM"), Address("TO LOAD INTO")],
        "SBA",
        "STORE BYTE ADDRESS"
    ),
    0x07: Instruction(
        [Register("TO LOAD FROM"), Register("TO LOAD INTO")],
        "SBR",
        "STORE BYTE REGISTER"
    ),
    0x08: Instruction(
        [Register("TO LOAD FROM"), Address("TO LOAD INTO")],
        "SWA",
        "STORE WORD ADDRESS"
    ),
    0x09: Instruction(
        [Register("TO LOAD FROM"), Register("TO LOAD INTO")],
        "SWR",
        "STORE WORD REGISTER"
    ),
    0x0A: Instruction(
        [Register("TO ADD TO"), Register("TO ADD")],
        "ADD",
        "ADD"
    ),
    0x0B: Instruction(
        [Register("TO SUBTRACT FROM"), Register("TO SUBTRACT")],
        "SUB",
        "SUBTRACT"
    ),
    0x0C: Instruction(
        [Register("TO MULTIPLY"), Register("TO MULTIPLY BY")],
        "MUL",
        "MULTIPLY"
    ),
    0x0D: Instruction(
        [Register("TO DIVIDE"), Register("TO DIVIDE BY")],
        "DIV",
        "DIVIDE"
    ),
    0x0E: Instruction(
        [Register("TO RAISE"), Register("TO RAISE TO")],
        "POW",
        "POWER"
    ),
    0x0F: Instruction(
        [Register("LEFT COMP"), Register("RIGHT COMP")],
        "CMP",
        "COMPARE"
    ),
    0x10: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JEQ",
        "JUMP EQUAL"
    ),
    0x11: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JNE",
        "JUMP NOT EQUAL"
    ),
    0x12: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JGT",
        "JUMP GREATER THAN"
    ),
    0x13: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JLT",
        "JUMP LESS THAN"
    ),
    0x14: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JGE",
        "JUMP GREATER EQUAL"
    ),
    0x15: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JLE",
        "JUMP LESS EQUAL"
    ),
    0x16: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JMP",
        "JUMP"
    ),
    0x17: Instruction(
        [Address("PROGRAM ADDRESS")],
        "CAL",
        "CALL SUBROUTINE"
    ),
    0x18: Instruction([], "RET", "RETURN FROM SUBROUTINE"),
    0x19: Instruction(
        [Register("TO PUSH ONTO STACK")],
        "PSH",
        "PUSH REGISTER TO STACK"
    ),
    0x1A: Instruction(
        [Register("TO POP FROM STACK")],
        "POP",
        "POP STACK TO REGISTER"
    )
}

REGISTERS = {
    "R1": 0x0,
    "R2": 0x1,
    "R3": 0x2,
    "R4": 0x3,
    "R5": 0x4,
    "R6": 0x5,
    "R7": 0x6,
    "R8": 0x7,
    "R9": 0x8,
    "LC": 0xA,
    "CR": 0xB,
    "SP": 0xC,
}

REGISTER_MAPPING = {
    0x0: 0x00,
    0x1: 0x02,
    0x2: 0x04,
    0x3: 0x06,
    0x4: 0x08,
    0x5: 0x0A,
    0x6: 0x0C,
    0x7: 0x0E,
    0x8: 0x10,
    0xA: 0x12,
    0xB: 0x14,
    0xC: 0x16
}

class MemoryAddress:
    def __init__(self, start: int, end: int) -> None:
        self.start, self.end, self.size = start, end, end - start

class Addresses:
    REGISTERS = MemoryAddress(0x0000, 0x0100)
    CODE      = MemoryAddress(0x0100, 0x2000)
    DATA      = MemoryAddress(0x2000, 0x3000)
    STACK     = MemoryAddress(0x3000, 0x4000)
