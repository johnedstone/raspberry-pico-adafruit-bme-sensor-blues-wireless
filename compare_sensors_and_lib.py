from machine import Pin, I2C

import adafruit_bme680
import bme680
import bme680i
import bme280
import bme280_float
import bme280_int

i2c_bme680 = I2C(0, sda=Pin(0), scl=Pin(1))
i2c_bme680_addr = i2c_bme680.scan()[0]
print(f'i2c_bme680: {i2c_bme680}')
print(f'i2c_bme680.scan()[0]: {i2c_bme680_addr}')

i2c_bme280 = I2C(1, sda=Pin(2), scl=Pin(3))
i2c_bme280_addr = i2c_bme280.scan()[0]
print(f'i2c_bme280: {i2c_bme280}')
print(f'i2c_bme280.scan(): {i2c_bme280_addr}')

print(f'{"#"*40}')


bme680_sensor_ada = adafruit_bme680.BME680_I2C(i2c_bme680, address=i2c_bme680_addr, debug=False)
bme680_sensor_rhh = bme680.BME680_I2C(i2c_bme680, address=i2c_bme680_addr)
bme680_sensor_rhi = bme680i.BME680_I2C(i2c_bme680, address=i2c_bme680_addr)
#print(f'bme680_sensor_ada: {dir(bme680_sensor_ada)}')
#print(f'bme680_sensor_rhh: {dir(bme680_sensor_rhh)}')
print(f'bme680_sensor_ada: {bme680_sensor_ada.temperature} {bme680_sensor_ada.humidity} {bme680_sensor_ada.pressure} {bme680_sensor_ada.gas}')
print(f'bme680_sensor_rhh: {bme680_sensor_rhh.temperature} {bme680_sensor_rhh.humidity} {bme680_sensor_rhh.pressure} {bme680_sensor_rhh.gas}')
print(f'bme680_sensor_rhi: {bme680_sensor_rhh.temperature} {bme680_sensor_rhh.humidity} {bme680_sensor_rhh.pressure} {bme680_sensor_rhh.gas}')

print(f'{"#"*40}')

bme280_sensor_ada = bme280.BME280(i2c=i2c_bme280, address=i2c_bme280_addr)
bme280_sensor_rhh = bme280_float.BME280(i2c=i2c_bme280, address=i2c_bme280_addr)
bme280_sensor_rhh_mode_1 = bme280_float.BME280(mode=1, i2c=i2c_bme280, address=i2c_bme280_addr)
bme280_sensor_rhi = bme280_int.BME280(i2c=i2c_bme280, address=i2c_bme280_addr)
print(f'bme280_sensor_ada: {bme280_sensor_ada.values}')
print(f'bme280_sensor_rhh: {bme280_sensor_rhh.values}')
print(f'bme280_sensor_rhh_mode_1: {bme280_sensor_rhh_mode_1.values}')
print(f'bme280_sensor_rhi: {bme280_sensor_rhi.values}')

# vim: ai et ts=4 sw=4 sts=4 nu
