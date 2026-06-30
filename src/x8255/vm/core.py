# Copyright (c) 2026 iiPython

# Modules
import operator

from x8255.cli import cexit
from x8255.isa import INSTRUCTIONS, Addresses
from x8255.vm.drivers import DriverManager

REG_MAPPING = {
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

class Emu8255:
    def __init__(self, enabled_drivers: list[str] = ["stdio"]) -> None:
        self.memory = bytearray(0x4000)

        # Load drivers
        self.drivers = DriverManager(self.memory, enabled_drivers)

    def read_register(self, register_id: int) -> int:
        offset = REG_MAPPING[register_id]
        return int.from_bytes(self.memory[offset:offset + 2])

    def write_register(self, register_id: int, value: int) -> None:
        offset = REG_MAPPING[register_id]
        self.memory[offset:offset + 2] = value.to_bytes(2)

    def push_stack(self, value: int) -> None:
        existing_offset = self.read_register(0xC)
        stack_offset = Addresses.STACK.end - existing_offset
        self.memory[stack_offset:stack_offset + 2] = value.to_bytes(2)
        self.write_register(0xC, existing_offset + 2)

    def pop_stack(self) -> int:
        existing_offset = self.read_register(0xC) - 2
        stack_offset = Addresses.STACK.end - existing_offset
        self.write_register(0xC, existing_offset)
        return int.from_bytes(self.memory[stack_offset:stack_offset + 2])

    def step(self) -> None:
        current_line = self.read_register(0xA)

        # Fetch next instruction
        offset = Addresses.CODE.start + current_line
        opcode = self.memory[offset]
        if opcode not in INSTRUCTIONS:
            return cexit(f"Invalid instruction {hex(opcode)} at {hex(offset)}!")

        instruction = INSTRUCTIONS[opcode]

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
                self.push_stack(self.read_register(0xA) + read_offset)
                self.write_register(0xA, arguments[0])

            case "RET":
                self.write_register(0xA, self.pop_stack())

            case "LBA" | "LBR" | "LWA" | "LWR" as op:
                offset, data_size = arguments[1], 1 if op[1] == "B" else 2
                if op[2] == "R":
                    offset = self.read_register(offset)

                self.write_register(
                    arguments[0],
                    self.drivers.on_read(offset) or int.from_bytes(self.memory[offset:offset + data_size])
                )

            case "SBA" | "SBR" | "SWA" | "SWR" as op:
                offset, data_size = arguments[1], 1 if op[1] == "B" else 2
                if op[2] == "R":
                    offset = self.read_register(offset)

                value = self.read_register(arguments[0])
                if not self.drivers.on_write(offset, value):
                    self.memory[offset:offset + data_size] = value.to_bytes(data_size)

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

    def write_range(self, data: bytes, offset: int) -> None:
        self.memory[offset:offset + len(data)] = data

    def terminate(self) -> None:
        terminate_instruction = self.memory[0x2700]
        if terminate_instruction:
            self.write_register(0xA, terminate_instruction)
