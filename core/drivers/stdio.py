# Copyright (c) 2026 iiPython

from core.drivers import DriverManager

class STDIODriver:
    def __init__(self, core: DriverManager) -> None:
        core.bind_write(0x0020, self.write_character)
        core.bind_write(0x0022, self.write_string)
        core.bind_write(0x0024, self.write_integer)
        core.bind_write(0x0026, self.clear_screen)

    def write(self, data: str) -> None:
        print(data, end = "", flush = True)

    def write_character(self, memory: bytearray, value: int) -> None:
        self.write(chr(value))

    def write_string(self, memory: bytearray, value: int) -> None:
        for item in memory[value:]:
            if not item:
                break

            self.write(chr(item))

    def write_integer(self, memory: bytearray, value: int) -> None:
        self.write(str(value))

    def clear_screen(self, memory: bytearray, value: int) -> None:
        self.write("\033[2J\033[H")
