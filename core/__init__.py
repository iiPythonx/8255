# Copyright (c) 2026 iiPython

from dataclasses import dataclass

@dataclass
class Argument:
    name: str
    size: int

class Register(Argument):
    size = 1

class Address(Argument):
    size = 2

class Value(Argument):
    size = 2

@dataclass
class Instruction:
    args:   list[Argument]
    opcode: str
    name:   str

INSTRUCTIONS = {
    0x00: Instruction([], "HLT", "HALT"),
    0x01: Instruction(
        [Register("TO LOAD INTO"), Address("TO LOAD FROM")],
        "LDM",
        "LOAD MEMORY"
    ),
    0x02: Instruction(
        [Register("TO LOAD INTO"), Value("TO LOAD")],
        "LDI",
        "LOAD IMMEDIATE"
    ),
    0x03: Instruction(
        [Register("TO LOAD FROM"), Address("TO LOAD INTO")],
        "STR",
        "STORE MEMORY"
    ),
    0x04: Instruction(
        [Register("TO ADD TO"), Register("TO ADD")].
        "ADD",
        "ADD"
    ),
    0x05: Instruction(
        [Register("TO SUBTRACT FROM"), Register("TO SUBTRACT")].
        "SUB",
        "SUBTRACT"
    ),
    0x06: Instruction(
        [Register("TO MULTIPLY"), Register("TO MULTIPLY BY")].
        "MUL",
        "MULTIPLY"
    ),
    0x07: Instruction(
        [Register("TO DIVIDE"), Register("TO DIVIDE BY")].
        "DIV",
        "DIVIDE"
    ),
    0x08: Instruction(
        [Register("TO RAISE"), Register("TO RAISE TO")].
        "POW",
        "POWER"
    ),
    0x09: Instruction(
        [Register("LEFT COMP"), Register("RIGHT COMP")].
        "CMP",
        "COMPARE"
    ),
    0x0A: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JEQ",
        "JUMP EQUAL"
    ),
    0x0B: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JNE",
        "JUMP NOT EQUAL"
    ),
    0x0C: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JGT",
        "JUMP GREATER THAN"
    ),
    0x0D: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JLT",
        "JUMP LESS THAN"
    ),
    0x0E: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JGE",
        "JUMP GREATER EQUAL"
    ),
    0x0F: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JLE",
        "JUMP LESS EQUAL"
    ),
    0x10: Instruction(
        [Address("PROGRAM ADDRESS")],
        "JMP",
        "JUMP"
    )
}
