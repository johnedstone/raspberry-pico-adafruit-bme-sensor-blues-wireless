# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# works on both QT-rp2040 and Feather-rp2040
"""CircuitPython blink example for built-in NeoPixel LED"""
import time
import board
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.1

while True:
    pixel.fill((255, 0, 0))
    time.sleep(0.5)
    pixel.fill((0, 0, 0))
    time.sleep(0.5)
