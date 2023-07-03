# adafruit_rp2040_sensor.py
# Using Circuitpython
# Using with Adafruit Feather RP2040, BME680, and 
#     optionally Adafruit MAX17048 LiPoly / LiIon Fuel Gauge and Battery Monitor

from time import sleep, localtime
import notecard
import board
import busio
import neopixel
import digitalio
import secrets

import adafruit_bme680_cp as adafruit_bme680

START_TIME = 0
DEBUG = True
CARD_RESTORE = False
IMEI = ""
DO_NOT_WAIT_FOR_GPS = False 

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Turn off Neopixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.deinit()

i2c1 = busio.I2C(board.SCL, board.SDA)

if DEBUG:
    i2c1.try_lock()
    print(f"i2c1.scan(): {i2c1.scan()}")
    i2c1.unlock()

bme680_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c1, 0x77) 
card = notecard.OpenI2C(i2c1, 0x17, 0, debug=DEBUG)

def set_start_time():
    global START_TIME
    led.value = True
    counter = 1
    while START_TIME == 0:
        req = {"req": "card.time"}
        rsp = card.Transaction(req)
        if DEBUG:
            print(rsp)
            print(counter)
            counter += 1
        if "time" in rsp.keys():
            START_TIME = rsp["time"]
            if DEBUG:
                print(f"START_TIME: {START_TIME}, {localtime(START_TIME)}")
        else:
            sleep(10)

    led.value = False
    return

def get_usb_status():
    req = {"req": "card.voltage"}
    rsp = card.Transaction(req)

    usb_status = rsp.get("usb", False)

    if DEBUG:
            print(f"USB Status: {usb_status}")

    return usb_status


def start_gps():
    req = {"req": "card.triangulate"}
    req["mode": "-"}
    rsp = card.Transaction(req)
        if DEBUG:
            print(f"Turning off card.triangulate: {rsp]")

    sleep(2)

    req = {"req": "card.location.mode"}
    req["mode"] = "off"
    rsp = card.Transaction(req)
    sleep(2)

    req = {"req": "card.location.mode"}
    req["mode"] = "periodic"
    req["seconds"] = 3600
    rsp = card.Transaction(req)

    if DO_NOT_WAIT_FOR_GPS:
        return

    gps_location_off = True
    while gps_location_off:
        req = {"req": "card.location"}
        rsp = card.Transaction(req)

        if "lat" in rsp.keys():
            gps_location_off = False
            led.value = False
        else:
            for i in range(5):
                led.value = True
                sleep(2)
                led.value = False
                sleep(2)
            if DEBUG:
                print(f"card.location: {rsp}")

    if DEBUG:
        req = {"req": "card.location"}
        rsp = card.Transaction(req)
        print(f"GPS STATUS: {rsp['status']}")

    return

## Let's get started
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

_ = set_start_time()
_ = start_gps()
_ = get_usb_status()
#_ = get_IMEI()

sleep(5) # to let sensors settle in

while True:
    led.value = True
    sleep(0.5)
    led.value = False
    sleep(0.5)

# vim: ai et ts=4 sw=4 sts=4 nu
