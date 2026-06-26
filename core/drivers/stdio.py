# Copyright (c) 2026 iiPython

from core.drivers import DriverManager

class STDIODriver:
    def __init__(self, core: DriverManager) -> None:
        core.bind_write(0x0020, self.write_character)
        core.bind_write(0x0022, self.write_string)
        core.bind_write(0x0024, self.clear_screen)

    def write_codepoint(self, codepoint: int) -> None:
        print(chr(codepoint), end = "", flush = True)

    def write_character(self, memory: bytearray, value: int) -> None:
        self.write_codepoint(value)

    def write_string(self, memory: bytearray, value: int) -> None:
        for item in memory[value:]:
            if not item:
                break

            self.write_codepoint(item)

    def clear_screen(self, memory: bytearray, value: int) -> None:
        print(f"\033[2J\033[H", end = "", flush = True)
