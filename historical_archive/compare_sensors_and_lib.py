import sys
from machine import Pin, I2C
from time import sleep

import adafruit_bme680
import bme680
import bme680i
import bme280
import bme280_float
import bme280_int

USE_I2C1 = True

# Select one of these for I2C1
BME280 = True
BME680_02 = False # Need to test

if BME280 and BME680_02:
    print('Yikes: only one device on I2C1')
    sys.exit()

i2c_bme680 = I2C(0, sda=Pin(0), scl=Pin(1))
i2c_bme680_addr = i2c_bme680.scan()[0]
print(f'i2c_bme680: {i2c_bme680}')
print(f'i2c_bme680.scan()[0]: {i2c_bme680_addr}')

if USE_I2C1:
    if BME280 or BME680_02:
        i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
        i2c1_addr = i2c1.scan()[0]
        print(f'i2c1: {i2c1}')
        print(f'i2c1.scan(): {i2c1_addr}')

print(f'{"#"*40}')


bme680_sensor_ada = adafruit_bme680.BME680_I2C(i2c_bme680, address=i2c_bme680_addr, debug=False)
bme680_sensor_rhh = bme680.BME680_I2C(i2c_bme680, address=i2c_bme680_addr)
bme680_sensor_rhi = bme680i.BME680_I2C(i2c_bme680, address=i2c_bme680_addr)
#print(f'bme680_sensor_ada: {dir(bme680_sensor_ada)}')
#print(f'bme680_sensor_rhh: {dir(bme680_sensor_rhh)}')

while True:
    print(f'bme680_sensor_ada: {bme680_sensor_ada.temperature} {bme680_sensor_ada.humidity} {bme680_sensor_ada.pressure} {bme680_sensor_ada.gas}')
    print(f'bme680_sensor_rhh: {bme680_sensor_rhh.temperature} {bme680_sensor_rhh.humidity} {bme680_sensor_rhh.pressure} {bme680_sensor_rhh.gas}')
    print(f'bme680_sensor_rhi: {bme680_sensor_rhh.temperature} {bme680_sensor_rhh.humidity} {bme680_sensor_rhh.pressure} {bme680_sensor_rhh.gas}')




    if USE_I2C1:
        if BME280:
            i2c1_ada = bme280.BME280(i2c=i2c1, address=i2c1_addr)
            i2c1_rhh = bme280_float.BME280(i2c=i2c1, address=i2c1_addr)
            i2c1_rhh_mode_1 = bme280_float.BME280(mode=1, i2c=i2c1, address=i2c1_addr)
            i2c1_rhi = bme280_int.BME280(i2c=i2c1, address=i2c1_addr)
            print(f'i2c1_ada: {i2c1_ada.values}')
            print(f'i2c1_rhh: {i2c1_rhh.values}')
            print(f'i2c1_rhh_mode_1: {i2c1_rhh_mode_1.values}')
            print(f'i2c1_rhi: {i2c1_rhi.values}')
        elif BME680_02:
            # Need to test this code
            i2c1_ada = adafruit_bme680.BME680_I2C(i2c1, address=i2c1_addr, debug=False)
            i2c1_rhh = bme680.BME680_I2C(i2c1, address=i2c1_addr)
            i2c1_rhi = bme680i.BME680_I2C(i2c1, address=i2c1_addr)
            print(f'i2c1_ada: {i2c1_ada.temperature} {i2c1_ada.humidity} {i2c1_ada.pressure} {i2c1_ada.gas}')
            print(f'i2c1_rhh: {i2c1_rhh.temperature} {i2c1_rhh.humidity} {i2c1_rhh.pressure} {i2c1_rhh.gas}')
            print(f'i2c1_rhi: {i2c1_rhh.temperature} {i2c1_rhh.humidity} {i2c1_rhh.pressure} {i2c1_rhh.gas}')
        else:
            pass


    print(f'{"#"*40}')
    sleep(60*30)
# vim: ai et ts=4 sw=4 sts=4 nu
