# Copyright (c) 2026 iiPython

import typing
import importlib

from x8255.cli import cexit

class DriverManager:
    def __init__(self, memory: bytearray, enabled_drivers: list[str]) -> None:
        self.memory = memory

        # Mappings
        self.read_mapping: dict[int, typing.Callable] = {}
        self.write_mapping: dict[int, typing.Callable] = {}

        # Begin initializing drivers
        for package in enabled_drivers:
            try:
                module = importlib.import_module(f"x8255.vm.drivers.{package}")
                driver = getattr(module, "Driver")
                if driver is None:
                    return cexit(f"Attempted to load driver '{package}', but it has no Driver class!")

                driver(self)

            except ModuleNotFoundError:
                cexit(f"Attempted to load driver '{package}', but it was not found!")

    def bind_write(self, address: int, callback: typing.Callable) -> None:
        self.write_mapping[address] = callback

    def bind_read(self, address: int, callback: typing.Callable) -> None:
        self.read_mapping[address] = callback

    def on_write(self, address: int, value: int) -> bool:
        if address in self.write_mapping:
            self.write_mapping[address](self.memory, value)
            return True

        return False

    def on_read(self, address: int) -> int | None:
        if address in self.read_mapping:
            return self.read_mapping[address](self.memory)

        return None
