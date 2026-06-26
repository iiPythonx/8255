# Copyright (c) 2026 iiPython

# Modules
import operator
from sys import argv
from pathlib import Path

from core import INSTRUCTIONS

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

    def read_register(self, register_id: int) -> int:
        offset = REG_MAPPING[register_id]
        return int.from_bytes(self.memory[offset:offset + 2])

    def write_register(self, register_id: int, value: int) -> None:
        offset = REG_MAPPING[register_id]
        self.memory[offset:offset + 2] = value.to_bytes(2)

    def push_stack(self, value: int) -> None:
        print(f"Stack push! {value}")
        existing_offset = self.read_register(0xC)
        stack_offset = MEM_STACK_RANGE[1] - existing_offset
        self.memory[stack_offset:stack_offset + 2] = value.to_bytes(2)
        self.write_register(0xC, existing_offset + 2)

    def pop_stack(self) -> int:
        print("Stack pop!")
        existing_offset = self.read_register(0xC) - 2
        stack_offset = MEM_STACK_RANGE[1] - existing_offset
        self.write_register(0xC, existing_offset)
        return int.from_bytes(self.memory[stack_offset:stack_offset + 2])

    def step_screen(self) -> None:
        print(f"SYSTEM STEP! CYCLE {self.cycle}\n")
        for _ in range(5):
            print(f"R{_ + 1}: {str(self.read_register(_)):<5}", end = " " + ("| " if _ < 4 else ""))

        print()
        for _, r in enumerate(("LC", "CR", "SP")):
            print(f"{r}: {str(self.read_register(0xA + _)):<5}", end = " " + ("| " if _ < 2 else ""))

        print("\n")

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
        print(instruction, "\n")

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

        new_current_line = self.read_register(0xA)
        if current_line == new_current_line:
            self.write_register(0xA, new_current_line + read_offset)
            print(f"Autostepped to {new_current_line + read_offset} from {current_line}")

        self.cycle += 1
        self.step_screen()

    def write_range(self, data: bytes, offset: int) -> None:
        self.memory[offset:offset + len(data)] = data

if __name__ == "__main__":
    if len(argv) < 2:
        exit("8255e: missing snapshot file")

    file = Path(argv[1])
    if not file.is_file():
        exit("8255e: file does not exist")

    data = file.read_bytes()
    code_range = 0x2000 - 0x0100

    # Setup emulation
    system = Emu8255()
    system.write_range(data[:code_range], 0x0100)
    system.write_range(data[code_range:], 0x2000)

    system.step_screen()
    while True:
        input("[ENTER] Step")
        system.step()
