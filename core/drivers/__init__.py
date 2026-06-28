# Copyright (c) 2026 iiPython

import typing
import importlib

ENABLED_DRIVERS = [
    ("stdio", "STDIODriver"),
    ("random", "RandomDriver")
]

class DriverManager:
    def __init__(self, emulator: "Emu8255") -> None:
        self.memory = emulator.memory

        # Mappings
        self.read_mapping: dict[int, typing.Callable] = {}
        self.write_mapping: dict[int, typing.Callable] = {}

        # Begin initializing drivers
        for package, driver in ENABLED_DRIVERS:
            getattr(importlib.import_module(f".{package}", package = "core.drivers"), driver)(self)

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
