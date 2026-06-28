# Copyright (c) 2026 iiPython

# Modules
import operator

from x8255.isa import INSTRUCTIONS
from x8255.vm.drivers import DriverManager

MEM_CODE_RANGE = (0x0100, 0x2000)
MEM_STACK_RANGE = (0x3000, 0x4000)

REG_MAPPING = {
    0x0: 0x00,
    0x1: 0x02,
    0x2: 0x04,
    0x3: 0x06,
    0x4: 0x08,
    0x5: 0x0A,
    0xA: 0x0C,
    0xB: 0x0E,
    0xC: 0x10
}

class Emu8255:
    def __init__(self) -> None:
        self.cycle = 0
        self.memory = bytearray(0x4000)

        # Load drivers
        self.drivers = DriverManager(self.memory)

    def read_register(self, register_id: int) -> int:
        offset = REG_MAPPING[register_id]
        return int.from_bytes(self.memory[offset:offset + 2])

    def write_register(self, register_id: int, value: int) -> None:
        offset = REG_MAPPING[register_id]
        self.memory[offset:offset + 2] = value.to_bytes(2)

    def push_stack(self, value: int) -> None:
        existing_offset = self.read_register(0xC)
        stack_offset = MEM_STACK_RANGE[1] - existing_offset
        self.memory[stack_offset:stack_offset + 2] = value.to_bytes(2)
        self.write_register(0xC, existing_offset + 2)

    def pop_stack(self) -> int:
        existing_offset = self.read_register(0xC) - 2
        stack_offset = MEM_STACK_RANGE[1] - existing_offset
        self.write_register(0xC, existing_offset)
        return int.from_bytes(self.memory[stack_offset:stack_offset + 2])

    def step(self) -> None:
        current_line = self.read_register(0xA)

        # Fetch next instruction
        offset = MEM_CODE_RANGE[0] + current_line
        instruction = INSTRUCTIONS[self.memory[offset]]

        # Read arguments
        read_offset, arguments = 1, []
        for arg in instruction.args:
            base_offset = offset + read_offset
            arguments.append(int.from_bytes(self.memory[base_offset:base_offset + arg.size]))
            read_offset += arg.size

        # Evaluate
        match instruction.opcode:
            case "HLT":
                exit()

            case "LDI":
                self.write_register(arguments[0], arguments[1])

            case "ADD" | "SUB" | "MUL" | "DIV" | "POW" as op:
                result = getattr(operator, {"DIV": "floordiv"}.get(op, op.lower()))(
                    self.read_register(arguments[0]),
                    self.read_register(arguments[1])
                )
                self.write_register(arguments[0], int(result))

            case "JMP":
                self.write_register(0xA, arguments[0])

            case "CAL":
                self.push_stack(self.read_register(0xA) + 1)
                self.write_register(0xA, arguments[0])

            case "RET":
                self.write_register(0xA, self.pop_stack())

            case "STR":
                offset, value = arguments[1], self.read_register(arguments[0])
                if not self.drivers.on_write(offset, value):
                    self.memory[offset:offset + 2] = value.to_bytes(2)

            case "LDM":
                offset = arguments[1]
                self.write_register(
                    arguments[0],
                    self.drivers.on_read(offset) or int.from_bytes(self.memory[offset:offset + 2])
                )

            case "CMP":
                left, right = self.read_register(arguments[0]), self.read_register(arguments[1])
                result = 255 if left < right else 1 if left > right else 0
                self.write_register(0xB, result)

            case "JEQ" if self.read_register(0xB) == 0:
                self.write_register(0xA, arguments[0])
                
            case "JNE" if self.read_register(0xB) != 0:
                self.write_register(0xA, arguments[0])

            case "JGT" if self.read_register(0xB) == 1:
                self.write_register(0xA, arguments[0])

            case "JLT" if self.read_register(0xB) == 255:
                self.write_register(0xA, arguments[0])

            case "JGE" if self.read_register(0xB) in {1, 0}:
                self.write_register(0xA, arguments[0])

            case "JLE" if self.read_register(0xB) in {0, 255}:
                self.write_register(0xA, arguments[0])

        new_current_line = self.read_register(0xA)
        if current_line == new_current_line:
            self.write_register(0xA, new_current_line + read_offset)

        self.cycle += 1

    def write_range(self, data: bytes, offset: int) -> None:
        self.memory[offset:offset + len(data)] = data
