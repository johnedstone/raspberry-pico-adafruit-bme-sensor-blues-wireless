# Adafruit QT RP2040 with micropython
# https://micropython.org/download/ADAFRUIT_QTPY_RP2040/
# https://learn.adafruit.com/adafruit-qt-py-2040/pinouts
# Using just I2C1 and STEMMA QT Connector

# This also works with the Adafruit Feather RP2040

from machine import Pin, I2C
from time import sleep, time, gmtime, localtime

import notecard
import time
import adafruit_bme680
import secrets

# for QT set to False as there is no led on a QT
FEATHER = True
if FEATHER:
    from machine import Pin
    led = Pin(13, Pin.OUT)

START_TIME = 0
DEBUG = True
CARD_RESTORE = False
IMEI = ''
DO_NOT_WAIT_FOR_GPS = True

if FEATHER:
    i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
else:
    # For QT RP2040
    i2c1 = I2C(1, sda=Pin(22), scl=Pin(23))

print(f'i2c1.scan(): {i2c1.scan()}')

bme680_sensor = adafruit_bme680.BME680_I2C(i2c1, address=119)
card = notecard.OpenI2C(i2c1, 23, 0, debug=DEBUG)

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
                print(f'START_TIME: {START_TIME}, {gmtime(START_TIME)} {localtime(START_TIME)}')
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
    st_year, st_mon, st_day, st_hr, st_min, st_sec, st_wkday, st_yrday = (0, 0, 0, 0, 0, 0, 0, 0)
    try:
        st_year, st_mon, st_day, st_hr, st_min, st_sec, st_wkday, st_yrday = gmtime(START_TIME)
    except Exception as e:
        print(f'gmtime(START_TIME) error: {e}')

    now = get_now()
    nw_year, nw_mon, nw_day, nw_hr, nw_min, nw_sec, nw_wkday, nw_yrday = (0, 0, 0, 0, 0, 0, 0, 0)
    try:
        nw_year, nw_mon, nw_day, nw_hr, nw_min, nw_sec, nw_wkday, nw_yrday = gmtime(now)
    except Exception as e:
        print(f'gmtime(now) error: {e}')

    lat, lon = get_gps()

    temp = 0.00
    try:
        temp = bme680_sensor.temperature
    except Exception as e:
        print(f'bme680 temperature error: {e}')

    hum = 0.00
    try:
        hum = bme680_sensor.humidity
    except Exception as e:
        print(f'bme680 humidity error: {e}')


    uptime = f'uptime: {START_TIME} {((now - START_TIME)) / (60*60*24):.3f}days {st_year}-{st_mon:02}-{st_day:02}T{st_hr:02}:{st_min:02}:{st_sec:02}Z {temp:.0f}C {(temp*9/5)+32:.0f}F, {hum:.0f}%RH, now: {nw_year}-{nw_mon:02}-{nw_day:02}T{nw_hr:02}:{nw_min:02}:{nw_sec:02}Z'

    if DEBUG:
        print(f'UPTIME: {uptime}')
        print(f'bme680_sensor: {START_TIME} {temp:.2f}C {(temp*9/5)+32:.2f}F, {hum:.2f}%RH')

    req = {"req": "note.add"}
    req["file"] = "sensors.qo"
    req["body"] = {'imei_string': IMEI,
                   'start_time': START_TIME,
                   'uptime': uptime,
                   'temperature': f'{temp:.2f}',
                   'humidity': f'{hum:.2f}',
                   'latitude': f'{lat}',
                   'longitude': f'{lon}',
                   }
    req["sync"] = True
    rsp = card.Transaction(req)
    if DEBUG:
        print(f'POST response (note.add): {rsp}')


    sleeping = ((300*12))
    if DEBUG:
        print(f'FINISHED: sleeping {sleeping} seconds')

    if FEATHER:
        for n in range(5):
            led.value(1)
            sleep(2)
            led.value(0)
            sleep(2)

    sleep(sleeping)


# vim: ai et ts=4 sw=4 sts=4 nu
