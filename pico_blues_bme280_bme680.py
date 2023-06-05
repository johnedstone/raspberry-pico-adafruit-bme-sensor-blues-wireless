"""
https://www.hackster.io/shilleh/how-to-connect-bme280-to-raspberry-pi-pico-micropython-91a392
https://github.com/SebastianRoll/mpy_bme280_esp8266
https://www.hackster.io/brandonsatrom/adding-cellular-to-the-raspberry-pi-pico-b8a4b6
"""
from machine import Pin, I2C
from time import sleep

import bme280
import adafruit_bme680

i2c=I2C(1, sda=Pin(2), scl=Pin(3)) #, freq=400000)
i2c_bme680 = I2C(0, sda=Pin(0), scl=Pin(1))
# print(i2c_bme680) # to see actual frequency)

print(f'i2c.scan(): {i2c.scan()}, i2c_bme680.scan(): {i2c_bme680.scan()}')

# https://forums.raspberrypi.com/viewtopic.php?t=343123
bme_i2c_address = i2c.scan()[0]
bme680_i2c_address = i2c_bme680.scan()[0]

bme280_sensor = bme280.BME280(i2c=i2c, address=bme_i2c_address)
bme680_sensor = adafruit_bme680.BME680_I2C(i2c_bme680, address=bme680_i2c_address, debug=False)
print("Connected to BME680... which appears to be more accurate than the bme280")


while True:    
    temp, pressure, rh = bme280_sensor.read_compensated_data()
    print(bme280_sensor.values)
    #print(temp, pressure, rh)
    #https://github.com/SebastianRoll/mpy_bme280_esp8266
    print(f'bme280_sensor: {temp/100:.2f}C {(temp/100*9/5)+32:.2f}F, {pressure/25600:.2f}hPa, {rh/1024:.2f}%RH')
    print(f'bme680_sensor: {bme680_sensor.temperature:.2f}C {(bme680_sensor.temperature*9/5)+32:.2f}F, {bme680_sensor.pressure:.2f}hPa, {bme680_sensor.humidity:.2f}%RH')
    sleep(300)

# vim: ai et ts=4 sw=4 sts=4 nu
