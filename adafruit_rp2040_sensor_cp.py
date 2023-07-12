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
from secrets import productUID, TEMPERATURE_OFFSET, HUMIDITY_OFFSET, TIME_SPENT_FUDGE

START_TIME = 0
DEBUG = True
CARD_DEBUG = True
CARD_RESTORE = False
IMEI = ''
DO_NOT_WAIT_FOR_GPS = True

TWO_SENSORS = False

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
card = notecard.OpenI2C(i2c1, 0x17, 0, debug=CARD_DEBUG)  # 23

if TWO_SENSORS:
    # Connecting 2nd BME680 SD0 to GRND to change address
    bme680_sensor_02 = adafruit_bme680.Adafruit_BME680_I2C(i2c1, 0x76) # 118

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
req["product"] = productUID
req["mode"] = "periodic"
rsp = card.Transaction(req)

_ = set_start_time()
_ = start_gps()
_ = get_IMEI()

while True:
    time_spent = 0
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

    temp_01_list = []
    hum_01_list = []
    if TWO_SENSORS:
        temp_02_list = []
        hum_02_list = []

    for n in range(30):
        if n > 14: # discard first 15 readings
            try:
                temp_01_list.append(bme680_sensor.temperature)
                if TWO_SENSORS:
                    temp_02_list.append(bme680_sensor_02.temperature)
            except Exception as e:
                print(f'bme680 temperature error: {e}')

            try:
                hum_01_list.append(bme680_sensor.relative_humidity)
                if TWO_SENSORS:
                    hum_02_list.append(bme680_sensor_02.relative_humidity)
            except Exception as e:
                print(f'bme680 humidity error: {e}')

        time_spent += 1
        sleep(1)

    if DEBUG:
        print(f'temp_01_list: {temp_01_list}')
        print(f'hum_01_list: {hum_01_list}')
        if TWO_SENSORS:
            print(f'temp_02: {temp_02_list}')
            print(f'hum_02: {hum_02_list}')

    hum_01_list = [n for n in hum_01_list if round(n) != 100] # remove 100
    if TWO_SENSORS:
        hum_02_list = [n for n in hum_02_list if round(n) != 100] # remove 100

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


    uptime = f'uptime: {START_TIME} {((now - START_TIME)) / (60*60*24):.3f}days {st_year}-{st_mon:02}-{st_day:02}T{st_hr:02}:{st_min:02}:{st_sec:02}Z {temp:.0f}C {(temp*9/5)+32:.0f}F, {hum:.0f}%RH, now: {nw_year}-{nw_mon:02}-{nw_day:02}T{nw_hr:02}:{nw_min:02}:{nw_sec:02}Z, USB Status:{get_usb_status()}, Offset: {TEMPERATURE_OFFSET}C, {HUMIDITY_OFFSET}%RH'

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
        led.value = True
        sleep(2)
        led.value = False
        sleep(2)

        time_spent += 4

    # 300 * 12 = 1hr
    sleeping = ((300 * 12) - (time_spent + TIME_SPENT_FUDGE))

    print(f'FINISHED: sleeping {sleeping} seconds')

    sleep(sleeping)


# vim: ai et ts=4 sw=4 sts=4 nu
