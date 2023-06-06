from machine import Pin, I2C
from time import sleep

import notecard
import utime
import bme280
import adafruit_bme680
import secrets

START_TIME = 0
DEBUG = True
CARD_RESTORE = False

led = (Pin(25), Pin.OUT)
i2c_bme680 = I2C(0, sda=Pin(0), scl=Pin(1))
i2c_notecarrier = I2C(1, sda=Pin(6), scl=Pin(7))

i2c_bme680_addr = i2c_bme680.scan()[0]
i2c_notecarrier_addr = i2c_notecarrier.scan()[0]

if DEBUG:
    print(f'i2c_bme_680: {i2c_bme680}, {i2c_bme680_addr}')
    print(f'i2c_notecarrier: {i2c_notecarrier}, {i2c_notecarrier_addr}')
    

bme680_sensor = adafruit_bme680.BME680_I2C(i2c_bme680, address=i2c_bme680_addr)
card = notecard.OpenI2C(i2c_notecarrier, i2c_notecarrier_addr, 0, debug=True)

def set_start_time(card):
    global START_TIME
    counter = 1
    while START_TIME == 0:
        req = {"req": "card.time"}
        rsp = card.Transaction(req)
        if DEBUG:
            print(rsp)
            print(counter)
            counter += 1
        if 'time' in rsp.keys():
            START_TIME = rsp['time']
            if DEBUG:
                print(f'START_TIME: {START_TIME}')
        sleep(10)
        
if CARD_RESTORE:
    req = {"req": "card.restore"}
    req["delete"] = True
    card.Transaction(req)
    print("Resetting card, sleeping 2min")
    sleep(120)

req = {"req": "hub.set"}
req["product"] = secrets.productUID
req["mode"] = "periodic"
rsp = card.Transaction(req)

_ = set_start_time(card)




# vim: ai et ts=4 sw=4 sts=4 nu