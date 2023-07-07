# adafruit_rp2040_sensor.py
# Using Circuitpython
# Using with Adafruit Feather RP2040 and BME680

import board
import busio
import neopixel
import digitalio

from time import sleep, localtime
import notecard

import adafruit_bme680_cp as adafruit_bme680
import secrets

START_TIME = 0
DEBUG = True
CARD_RESTORE = False
IMEI = ''
DO_NOT_WAIT_FOR_GPS = True

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

bme680_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c1, 0x77)  # 119
card = notecard.OpenI2C(i2c1, 0x17, 0, debug=DEBUG)  # 23


def get_usb_status():
    req = {"req": "card.voltage"}
    rsp = card.Transaction(req)

    usb_status = rsp.get("usb", False)

    if DEBUG:
        print(f"USB Status: {usb_status}")

    return usb_status


def get_IMEI():
    global IMEI
    while IMEI == '':
        req = {'req': 'card.wireless'}
        rsp = card.Transaction(req)
        if DEBUG:
            print(rsp)
        if 'net' in rsp.keys():
            if 'imei' in rsp['net'].keys():
                IMEI = rsp['net']['imei']
        if DEBUG:
            print(f'IMEI: {IMEI}')

        return

def set_start_time():
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
                print(f"START_TIME: {START_TIME}, {localtime(START_TIME)}")
        else:
            sleep(10)

    return

def get_now():
    now = 0
    req = {"req": "card.time"}
    rsp = card.Transaction(req)
    if 'time' in rsp.keys():
        now = rsp['time']
        if DEBUG:
            print(f'NOW: {now}, {gmtime(now)}')

    return now

def get_gps():
    lat = ''
    lon = ''
    req = {"req": "card.location"}
    rsp = card.Transaction(req)

    rsp_keys = rsp.keys()
    if 'lat' in rsp_keys:
        lat = rsp['lat']

    if 'lon' in rsp_keys:
        lon = rsp['lon']

    return (lat, lon)


def start_gps():
    req = {"req": "card.triangulate"}
    req['mode'] = "-"
    rsp = card.Transaction(req)
    if DEBUG:
        print(f"Turning off card.triangulate: {rsp}")

    sleep(2)

    req = {'req': 'card.location.mode'}
    req['mode'] = 'off'
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

        if 'lat' in rsp.keys():
            gps_location_off = False

        sleep(10)

    if DEBUG:
        req = {"req": "card.location"}
        rsp = card.Transaction(req)
        print(f'GPS STATUS: {rsp['status']}')

    return

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
_ = get_IMEI()

sleep(5) # to let sensors settle in

while True:
    led.value = True
    sleep(0.5)
    led.value = False
    sleep(0.5)

# vim: ai et ts=4 sw=4 sts=4 nu
