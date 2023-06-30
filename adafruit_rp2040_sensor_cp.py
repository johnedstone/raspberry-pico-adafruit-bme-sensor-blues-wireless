# adafruit_rp2040_sensor.py
# Using Circuitpython
# Using with Adafruit Feather RP2040, BME680, and 
#     optionally Adafruit MAX17048 LiPoly / LiIon Fuel Gauge and Battery Monitor

import time
import notecard
import board
import neopixel
import digitalio
import secrets

import adafruit_bme680_cp as adafruit_bme680

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Turn off Neopixel
pixel.deinit()

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

# vim: ai et ts=4 sw=4 sts=4 nu
