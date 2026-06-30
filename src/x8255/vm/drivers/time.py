# Copyright (c) 2026 iiPython

# Driver: time
# Purpose: Provide time related utilities to 8255
#
# Registers:
#   R 0x0050 - Read current MILLISECOND
#   R 0x0052 - Read current SECOND
#   R 0x0054 - Read current MINUTE
#   R 0x0056 - Read current HOUR
#   R 0x0058 - Read current DAY
#   R 0x005A - Read current MONTH
#   R 0x005C - Read current YEAR
#   W 0x005E - Sleep main thread for specified duration in milliseconds

from time import sleep
from datetime import datetime

from x8255.vm.drivers import DriverManager

class Driver:
    def __init__(self, core: DriverManager) -> None:
        core.bind_read(0x0050, self.read_millisecond)
        core.bind_read(0x0052, self.read_second)
        core.bind_read(0x0054, self.read_minute)
        core.bind_read(0x0056, self.read_hour)
        core.bind_read(0x0058, self.read_day)
        core.bind_read(0x005A, self.read_month)
        core.bind_read(0x005C, self.read_year)
        core.bind_write(0x005E, self.write_sleep)

    @property
    def now(self) -> datetime:
        return datetime.now()

    def read_millisecond(self, memory: bytearray) -> int:
        return self.now.microsecond // 10

    def read_second(self, memory: bytearray) -> int:
        return self.now.second

    def read_minute(self, memory: bytearray) -> int:
        return self.now.minute

    def read_hour(self, memory: bytearray) -> int:
        return self.now.hour

    def read_day(self, memory: bytearray) -> int:
        return self.now.day

    def read_month(self, memory: bytearray) -> int:
        return self.now.month

    def read_year(self, memory: bytearray) -> int:
        return self.now.year

    def write_sleep(self, memory: bytearray, value: int) -> None:
        sleep(value / 1000)
