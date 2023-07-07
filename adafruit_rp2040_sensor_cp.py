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
            print(f'NOW: {now}, {localtime(now)}')

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
    st_year, st_mon, st_day, st_hr, st_min, st_sec, st_wkday, st_yrday, st_isdst = (0, 0, 0, 0, 0, 0, 0, 0, -1)
    try:
        st_year, st_mon, st_day, st_hr, st_min, st_sec, st_wkday, st_yrday, st_isdst = localtime(START_TIME)
    except Exception as e:
        print(f'localtime(START_TIME) error: {e}')

    now = get_now()
    nw_year, nw_mon, nw_day, nw_hr, nw_min, nw_sec, nw_wkday, nw_yrday, nw_isdst = (0, 0, 0, 0, 0, 0, 0, 0, -1)
    try:
        nw_year, nw_mon, nw_day, nw_hr, nw_min, nw_sec, nw_wkday, nw_yrday, nw_isdst = localtime(now)
    except Exception as e:
        print(f'localtime(now) error: {e}')

    lat, lon = get_gps()

    # From https://docs.circuitpython.org/projects/bme680/en/latest/examples.html
    # You will usually have to add an offset to account for the temperature of
    # the sensor. This is usually around 5 degrees but varies by use. Use a
    # separate temperature sensor to calibrate this one.
    #temperature_offset = -5
    temperature_offset = 0 

    # let's take the 2nd reading here
    for n in range(2):
        temp = 0.00
        try:
            temp = bme680_sensor.temperature + temperature_offset
        except Exception as e:
            print(f'bme680 temperature error: {e}')

        hum = 0.00
        try:
            hum = bme680_sensor.relative_humidity
            if DEBUG:
                print(f'relative_humidity: {hum}, humidity: {bme680_sensor.humidity}')
        except Exception as e:
            print(f'bme680 humidity error: {e}')

        sleep(2)


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


    sleeping = ((300*12))
    if DEBUG:
        print(f'FINISHED: sleeping {sleeping} seconds')

    for n in range(5):
        led.value = True
        sleep(2)
        led.value = False
        sleep(2)

    sleep(sleeping)


# vim: ai et ts=4 sw=4 sts=4 nu
