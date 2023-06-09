from machine import Pin, I2C
from time import sleep, time, gmtime, localtime

import notecard
import time
import adafruit_bme680
import secrets

START_TIME = 0
DEBUG = True
CARD_RESTORE = False
IMEI = ''
DO_NOT_WAIT_FOR_GPS = True

led_onboard = Pin(25, Pin.OUT)
i2c_bme680 = I2C(0, sda=Pin(16), scl=Pin(17))
i2c_notecarrier = I2C(1, sda=Pin(18), scl=Pin(19))
USB_POWER = Pin(24, Pin.IN)

i2c_bme680_addr = i2c_bme680.scan()[0]
i2c_notecarrier_addr = i2c_notecarrier.scan()[0]

if DEBUG:
    print(f'i2c_bme_680: {i2c_bme680}, {i2c_bme680_addr}')
    print(f'i2c_notecarrier: {i2c_notecarrier}, {i2c_notecarrier_addr}')
    

bme680_sensor = adafruit_bme680.BME680_I2C(i2c_bme680, address=i2c_bme680_addr)
card = notecard.OpenI2C(i2c_notecarrier, i2c_notecarrier_addr, 0, debug=DEBUG)

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
    led_onboard.value(1)
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

    led_onboard.value(0)
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
    # Need to test
    #req = {"req": "card.triangulate"}
    #req['mode'] =  "-"
    #rsp = card.Transaction(req)
    #if DEBUG:
    #    print(f"Turning off card.triangulate: {rsp}")
#
#    sleep(2)

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
            led_onboard.value(0)
        else:
            for i in range(5):
                led_onboard.value(1)
                sleep(2)
                led_onboard.value(0)
                sleep(2)

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

    usb_power = True
    try:
        if USB_POWER() != 1:
            usb_power = False
    except Exception as e:
        print(f'USB_POWER() error: {e}')

    uptime = f'uptime: {START_TIME} {((now - START_TIME)) / (60*60*24):.3f}days {st_year}-{st_mon:02}-{st_day:02}T{st_hr:02}:{st_min:02}:{st_sec:02}Z {temp:.0f}C {(temp*9/5)+32:.0f}F, {hum:.0f}%RH, now: {nw_year}-{nw_mon:02}-{nw_day:02}T{nw_hr:02}:{nw_min:02}:{nw_sec:02}Z USB_Power(): {usb_power}'

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

    for n in range(10):
            led_onboard.value(1)
            sleep(1)
            led_onboard.value(0)
            sleep(1)

    #           5min * 12 = 1 hour, minus sleep (sec) above
    sleeping = ((300*12)-20)
    if DEBUG:
        print(f'FINISHED: sleeping {sleeping} seconds')
    sleep(sleeping)


# vim: ai et ts=4 sw=4 sts=4 nu
