"""
https://www.hackster.io/shilleh/how-to-connect-bme280-to-raspberry-pi-pico-micropython-91a392
https://github.com/SebastianRoll/mpy_bme280_esp8266
"""
from machine import Pin, I2C
from time import sleep

import bme280


i2c=I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
print(f'i2c.scan(): {i2c.scan()}')

# https://forums.raspberrypi.com/viewtopic.php?t=343123
bme_i2c_address = i2c.scan()[0]

while True:
    bme = bme280.BME280(i2c=i2c, address=bme_i2c_address)
    temp, pressure, rh = bme.read_compensated_data()
    print(bme.values)
    #print(temp, pressure, rh)
    #https://github.com/SebastianRoll/mpy_bme280_esp8266
    print(f'{temp/100:.2f}C {((temp*9/5)/100)+32:.2f}F, {pressure/25600:.2f}hPa, {rh/1024:.2f}%RH')
    sleep(300)

# vim: ai et ts=4 sw=4 sts=4 nu
