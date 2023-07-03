#adafruit_feather_rp2040_mp_blink.py
# Adafruit Feather RP2040 Micropython "blink"

from machine import Pin
from time import sleep

led = Pin(13, Pin.OUT)

while True:
    led.value(1)
    sleep(2)
    led.value(0)
    sleep(2)

# vim: ai et ts=4 sw=4 sts=4 nu
