"""
Reference:
    https://dev.blues.io/guides-and-tutorials/notecard-guides/diagnosing-cellular-connectivity-issues/#check-cellular-signal-quality
    https://www.rangeful.com/what-is-rssi-sinr-rsrp-rsrq-how-does-this-affect-signal-quality/

### WBNA with Notecarrier A
Built in Antenna - almost as good as Pulse W6112 below
rsrq: -16 | band: LTE BAND 2 | sinr: 13 | rssir: -63 | bars: 2 | rssi: -63 | rsrp: -98
rsrq: -16 | band: LTE BAND 2 | sinr: 13 | rssir: -63 | bars: 2 | rssi: -63 | rsrp: -98
rsrq: -16 | band: LTE BAND 2 | sinr: 13 | rssir: -63 | bars: 2 | rssi: -63 | rsrp: -98
rsrq: -16 | band: LTE BAND 2 | sinr: 13 | rssir: -63 | bars: 2 | rssi: -63 | rsrp: -98

Pulse W3906 
rsrq: -13 | band: LTE BAND 2 | sinr: 16 | rssir: -69 | bars: 1 | rssi: -69 | rsrp: -101
rsrq: -12 | band: LTE BAND 2 | sinr: 16 | rssir: -71 | bars: 1 | rssi: -72 | rsrp: -103
rsrq: -12 | band: LTE BAND 2 | sinr: 16 | rssir: -71 | bars: 1 | rssi: -72 | rsrp: -103
rsrq: -12 | band: LTE BAND 2 | sinr: 16 | rssir: -71 | bars: 1 | rssi: -72 | rsrp: -103

Molex which came with Notecarrier F - worst
rsrq: -11 | band: LTE BAND 2 | sinr: 10 | rssir: -69 | bars: 1 | rssi: -69 | rsrp: -101
rsrq: -12 | band: LTE BAND 2 | sinr: 16 | rssir: -69 | bars: 2 | rssi: -69 | rsrp: -100
rsrq: -12 | band: LTE BAND 2 | sinr: 16 | rssir: -69 | bars: 2 | rssi: -69 | rsrp: -100
rsrq: -12 | band: LTE BAND 2 | sinr: 16 | rssir: -69 | bars: 2 | rssi: -69 | rsrp: -100

Pulse W6112 recommended by Blues.io Slightly Best based on SINR and RSRP
rsrq: -13 | band: LTE BAND 2 | sinr: 20 | rssir: -63 | bars: 2 | rssi: -63 | rsrp: -94
rsrq: -14 | band: LTE BAND 2 | sinr: 22 | rssir: -61 | bars: 2 | rssi: -62 | rsrp: -93
rsrq: -11 | band: LTE BAND 2 | sinr: 21 | rssir: -63 | bars: 2 | rssi: -64 | rsrp: -94
rsrq: -11 | band: LTE BAND 2 | sinr: 21 | rssir: -63 | bars: 2 | rssi: -64 | rsrp: -94

### NBGL with Notecarrier A
Built in Antenna: appears to be better for NBGL based on bars and rsrp
rsrq: -17 | band: LTE BAND 2 | sinr: 159 | rssir: -69 | bars: 2 | rssi: -70 | rsrp: -98
rsrq: -11 | band: LTE BAND 2 | sinr: 149 | rssir: -73 | bars: 2 | rssi: -73 | rsrp: -97
rsrq: -11 | band: LTE BAND 2 | sinr: 149 | rssir: -73 | bars: 2 | rssi: -73 | rsrp: -97
rsrq: -11 | band: LTE BAND 2 | sinr: 149 | rssir: -73 | bars: 2 | rssi: -73 | rsrp: -97
rsrq: -11 | band: LTE BAND 2 | sinr: 149 | rssir: -73 | bars: 2 | rssi: -73 | rsrp: -97

Taoglas MFX3.07 recommended by Blues
rsrq: -15 | band: LTE BAND 2 | sinr: 187 | rssir: -77 | bars: 1 | rssi: -78 | rsrp: -102
rsrq: -15 | band: LTE BAND 2 | sinr: 158 | rssir: -77 | bars: 1 | rssi: -78 | rsrp: -102
rsrq: -15 | band: LTE BAND 2 | sinr: 158 | rssir: -77 | bars: 1 | rssi: -78 | rsrp: -102
rsrq: -15 | band: LTE BAND 2 | sinr: 158 | rssir: -77 | bars: 1 | rssi: -78 | rsrp: -102
rsrq: -15 | band: LTE BAND 2 | sinr: 158 | rssir: -77 | bars: 1 | rssi: -78 | rsrp: -102
"""

from machine import Pin, I2C
from time import sleep, time, gmtime, localtime
import notecard
import secrets

START_TIME = 0
DEBUG = True
CARD_RESTORE = False
SHOW_RAW_WIRELESS_RSP = False

led_onboard = Pin(25, Pin.OUT)
i2c_notecarrier = I2C(1, sda=Pin(18), scl=Pin(19))
i2c_notecarrier_addr = i2c_notecarrier.scan()[0]
#card = notecard.OpenI2C(i2c_notecarrier, i2c_notecarrier_addr, 0, debug=DEBUG)
card = notecard.OpenI2C(i2c_notecarrier, i2c_notecarrier_addr, 0, debug=False)

if DEBUG:
    print(f'i2c_notecarrier: {i2c_notecarrier}, {i2c_notecarrier_addr}')

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
if DEBUG:
    print(f'hub.set: {rsp}')

_ = set_start_time()

while True:
    rsrq = ''
    band = ''
    sinr = ''
    rssir = ''
    bars = ''
    rssi = ''
    rsrp = ''

    req = {"req": "card.wireless"}
    rsp = card.Transaction(req)

    if SHOW_RAW_WIRELESS_RSP:
        print(f'card.wireless: {rsp}')
    if 'net' in rsp.keys():
        rsrq = rsp['net'].get('rsrq', 0)
        band = rsp['net'].get('band')
        sinr = rsp['net'].get('sinr', 0)
        rssir = rsp['net'].get('rssir', 0)
        bars = rsp['net'].get('bars', 0)
        rssi = rsp['net'].get('rssi', 0)
        rsrp = rsp['net'].get('rsrp', 0)


    print(f'rsrq: {rsrq} | ' +
            f'band: {band} | ' +
            f'sinr: {sinr} | ' +
            f'rssir: {rssir} | ' +
            f'bars: {bars} | ' +
            f'rssi: {rssi} | ' +
            f'rsrp: {rsrp}'
            )

    sleep(60)

# vim: ai et ts=4 sw=4 sts=4 nu
