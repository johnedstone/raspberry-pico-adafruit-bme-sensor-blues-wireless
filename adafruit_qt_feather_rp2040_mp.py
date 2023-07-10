# script: adafruit_qt_feather_rp2040_mp.py
# Adafruit Feather/QT RP2040 with micropython

# https://micropython.org/download/ADAFRUIT_QTPY_RP2040/
# https://learn.adafruit.com/adafruit-qt-py-2040/pinouts
# Using just I2C1 and STEMMA QT Connector

# This also works with the Adafruit Feather RP2040

from machine import Pin, I2C

from time import sleep, time, gmtime, localtime
import time
import notecard

import adafruit_bme680
import secrets

START_TIME = 0
DEBUG = True
CARD_DEBUG = True
CARD_RESTORE = False
IMEI = ''
DO_NOT_WAIT_FOR_GPS = True

# for QT set to False as there is no led on a QT
FEATHER = True

TWO_SENSORS = True
TEMPERATURE_OFFSET = -1
HUMIDITY_OFFSET = +4

if FEATHER:
    led = Pin(13, Pin.OUT)
    i2c1 = I2C(1, sda=Pin(2), scl=Pin(3))
else:
    # For QT RP2040
    i2c1 = I2C(1, sda=Pin(22), scl=Pin(23))

if DEBUG:
    print(f'i2c1.scan(): {i2c1.scan()}')

bme680_sensor = adafruit_bme680.BME680_I2C(i2c1, address=119)
card = notecard.OpenI2C(i2c1, 23, 0, debug=DEBUG)

if TWO_SENSORS:
    # Connecting 2nd BME680 SD0 to GRND to change address
    bme680_sensor_02 = adafruit_bme680.BME680_I2C(i2c1, address=118)

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
    lat = 0.0 
    lon = 0.0 
    req = {"req": "card.location"}
    rsp = card.Transaction(req)

    rsp_keys = rsp.keys()
    if 'lat' in rsp_keys:
        lat = rsp['lat']

    if 'lon' in rsp_keys:
        lon = rsp['lon']

    if DEBUG:
            print(f'type(lat), type(lon): {type(lat)}, {type(lon)}')
            print(f'lat, lon: {lat:.8f}, {lon:.8f}')

    return (f'{lat:.8f}', f'{lon:.8f}')


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

while True:
    time_spent = 0
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

    temp_01_list = []
    hum_01_list = []
    if TWO_SENSORS:
        temp_02_list = []
        hum_02_list = []

    for n in range(12):
        if n > 1: # discard first two readings
            try:
                temp_01_list.append(bme680_sensor.temperature)
                if TWO_SENSORS:
                    temp_02_list.append(bme680_sensor_02.temperature)
            except Exception as e:
                print(f'bme680 temperature error: {e}')

            try:
                hum_01_list.append(bme680_sensor.humidity)
                if TWO_SENSORS:
                    hum_02_list.append(bme680_sensor_02.humidity)
            except Exception as e:
                print(f'bme680 humidity error: {e}')

        time_spent += 1
        sleep(1)

    hum_01_list = [n for n in hum_01_list if round(n) != 100] # remove 100
    if TWO_SENSORS:
        hum_02_list = [n for n in hum_02_list if round(n) != 100] # remove 100

    if DEBUG:
        print(f'temp_01_list: {temp_01_list}')
        print(f'hum_01_list: {hum_01_list}')
        if TWO_SENSORS:
            print(f'temp_02: {temp_02_list}')
            print(f'hum_02: {hum_02_list}')

    temp_01_list.remove(max(temp_01_list))
    temp_01_list.remove(min(temp_01_list))
    temp_01_avg = (sum(temp_01_list) / len(temp_01_list))

    hum_01_list.remove(max(hum_01_list))
    hum_01_list.remove(min(hum_01_list))
    hum_01_avg = sum(hum_01_list) / len(hum_01_list)

    if TWO_SENSORS:
        temp_02_list.remove(max(temp_02_list))
        temp_02_list.remove(min(temp_02_list))
        temp_02_avg = (sum(temp_02_list) / len(temp_02_list))

        hum_02_list.remove(max(hum_02_list))
        hum_02_list.remove(min(hum_02_list))
        hum_02_avg = sum(hum_02_list) / len(hum_02_list)

    if TWO_SENSORS:
        temp_wo_offset = (temp_01_avg + temp_02_avg) / 2
        hum_wo_offset = (hum_01_avg + hum_02_avg) / 2
    else:
        temp_wo_offset = temp_01_avg
        hum_wo_offset = hum_01_avg

    # From https://docs.circuitpython.org/projects/bme680/en/latest/examples.html
    # You will usually have to add an offset to account for the temperature of
    # the sensor. This is usually around 5 degrees but varies by use. Use a
    # separate temperature sensor to calibrate this one.

    temp = temp_wo_offset + TEMPERATURE_OFFSET
    hum = hum_wo_offset + HUMIDITY_OFFSET

    if DEBUG:
        print(f'temp_01_list: {temp_01_list}, avg: {temp_01_avg}')
        print(f'hum_01_list: {hum_01_list}, avg: {hum_01_avg}')
        if TWO_SENSORS:
            print(f'temp_02_list: {temp_02_list}, avg: {temp_02_avg}')
            print(f'hum_02_list: {hum_02_list}, avg: {hum_02_avg}')
        print(f'Final w/o offset: {temp_wo_offset:.0f}C {hum_wo_offset:.0f}%RH')
    print(f'Final: {temp:.0f}C {hum:.0f}%RH')

    uptime = f'uptime: {START_TIME} {((now - START_TIME)) / (60*60*24):.3f}days {st_year}-{st_mon:02}-{st_day:02}T{st_hr:02}:{st_min:02}:{st_sec:02}Z {temp:.0f}C {(temp*9/5)+32:.0f}F, {hum:.0f}%RH, now: {nw_year}-{nw_mon:02}-{nw_day:02}T{nw_hr:02}:{nw_min:02}:{nw_sec:02}Z, USB Status:{get_usb_status()}'

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

    for n in range(5):
        led.value(1)
        sleep(2)
        led.value(0)
        sleep(2)

        time_spent += 4

    # 300 * 12 = 1hr
    sleeping = ((300 * 12) - time_spent)

    print(f'FINISHED: sleeping {sleeping} seconds')

    sleep(sleeping)


# vim: ai et ts=4 sw=4 sts=4 nu
