# Copyright (c) 2026 iiPython

# Driver: time
# Purpose: Provide time related utilities to 8255
#
# Registers:
#   R 0x0030 - Read current MILLISECOND
#   R 0x0032 - Read current SECOND
#   R 0x0034 - Read current MINUTE
#   R 0x0036 - Read current HOUR
#   R 0x0038 - Read current DAY
#   R 0x003A - Read current MONTH
#   R 0x003C - Read current YEAR
# 
# Examples:

from datetime import datetime

from core.drivers import DriverManager

class TimeDriver:
    def __init__(self, core: DriverManager) -> None:
        core.bind_read(0x0030, self.read_millisecond)
        core.bind_read(0x0032, self.read_second)
        core.bind_read(0x0034, self.read_minute)
        core.bind_read(0x0036, self.read_hour)
        core.bind_read(0x0038, self.read_day)
        core.bind_read(0x003A, self.read_month)
        core.bind_read(0x003C, self.read_year)

    @property
    def now(self) -> datetime:
        return datetime.now()

    def read_millisecond(self, memory: bytearray) -> int:
        return self.now.millisecond

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
