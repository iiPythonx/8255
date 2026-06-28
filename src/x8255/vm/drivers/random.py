# Copyright (c) 2026 iiPython

# Driver: random
# Purpose: Provide psuedo-random number generation to 8255
#
# Registers:
#   R 0x0030 - Read a random 16-bit integer
#   W 0x0032 - Set maximum bound
#
# Examples:
#   ldm r1, 0x0030  # Load random number between 0 - 65535 to R1
#   str r1, 0x0024  # Send R1 to screen
#
#   ldi r1, 100
#   str r1, 0x0032  # Set RNG upper bound to 100
#   ldm r1, 0x0030  # Load random number between 0 - 100 to R1
#   str r1, 0x0024  # Send R1 to screen

import random

from x8255.vm.drivers import DriverManager

class RandomDriver:
    def __init__(self, core: DriverManager) -> None:
        core.bind_read(0x0030, self.read_random)
        core.bind_write(0x0032, self.write_upper_bound)

        self.upper_bound = (2 ** 16) - 1

    def read_random(self, memory: bytearray) -> int:
        return random.randint(0, self.upper_bound)

    def write_upper_bound(self, memory: bytearray, value: int) -> None:
        self.upper_bound = value
