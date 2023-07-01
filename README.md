### Description
* Getting started with Raspberry Pico, Adafruit BME280, and [Blues Wireless](https://blues.io/)
* Getting started with Adafruit Feather RP2040 and CircuitPython as well.

#### Currently running
* `adafruit_rp2040_sensor_cp.py`: Circuitpython, Adafruit Feather RP2040, BME680, Notecarrier A
    * in development - not working yet
* `adafruit_qt_rp2040_mp.py`: Micropython, Adafruit QT RP2040, BME680, Notecarrier A, Notecard WBNA-500 or NBGL-500
    * great combination if you don't need a battery
    * no soldering or breadboard needed
    * Works with STEMMA QT connected to Notecarrier header, and BME680 connected to Notecarier I2C connector
* `pico_sensor_notecard_A01.py`:  Micropython, Raspberry Pi Pico, BME680, Notecarrier A, Notecard WBNA-500 or NBGL-500
    * great combination if you don't need a battery
    * shim works, just doesn't power up Pico until battery is recharged.

### Development scripts
* `compare_sensors_and_lib.py`
* `pico_blues_bme280_bme680.py`
* `pico_blues_bme280.py`
* etc., etc.

### Troubleshooting
* When all else fails, power cycle the Raspberry Pi Pico

### Micropython packages for BME280 and BME680
* BME680: _(Currently using)_ [lib/adafruit_bme680.py](https://github.com/bsatrom/notecard-pico)
* BME680: [lib/bme680.py](https://github.com/robert-hh/BME680-Micropython/tree/master)
* BME280: [lib/bme280](https://github.com/SebastianRoll/mpy_bme280_esp8266)
* BME280: _(Recommended)_ [lib/bme280_float.py](https://github.com/robert-hh/BME280)
* BME280: [lib/bme280_int.py](https://github.com/robert-hh/BME280)
* Note: these are not *circuitpython libraries*

Recommending:
* bm680 libraries are all about the same: go with `adafruit_bme680.py` 
* bme280: go with `bme_280_float.py`, though the humidity is a little hight

Results running `compare_sensors_and_lib.py`:
```
bme680_sensor_ada: 23.16711 47.33186 985.0639 23455
bme680_sensor_rhh: 23.29191 47.38399 985.0844 13908
bme680_sensor_rhi: 24.44328 47.17461 985.1328 19586
bme280_sensor_ada: ('20.82C', '668.43hPa', '64.96%')
bme280_sensor_rhh: ('22.56C', '985.90hPa', '58.32%')
bme280_sensor_rhi: ('22.56C', '985.90hPa', '58.32%')
```

#### Raspberry Pi Pico with BME680 with LiPo Shim
![current project](./images/pico_blues_bme680.png)

### References Pico and BME280
* [How to Connect BME280 to Raspberry Pi Pico MicroPython](https://www.hackster.io/shilleh/how-to-connect-bme280-to-raspberry-pi-pico-micropython-91a392)
* [Troubleshooting error:  added address parameter](https://forums.raspberrypi.com/viewtopic.php?t=343123)
* [dev.blues.io api](https://dev.blues.io/api-reference/notecard-api/introduction/)
* These two are together:
    * [Adding Cellular to the raspberry Pico bme680](https://www.hackster.io/brandonsatrom/adding-cellular-to-the-raspberry-pi-pico-b8a4b6)
    * [code for bme680 and pico - github](https://github.com/bsatrom/notecard-pico)

### Notes about Pico LiPo Shim
It appears, that once on battery, and once the Pico/Shim/Notecard stops reporting, e.g after some hours, that
after the USB Power is connected, the device waits 6 hours, charging the battery, before starting up the Pico.
That is, using the shim is not a relevant indicator for "when" the power is restored, because time is spent recharging the
battery, before restarting the Pico. Question: is the Adafruit RP2040 Feather a better indicator for when power is restored?

### Blues Wireless Reference
* [note-python: python library](https://github.com/blues/note-python)
* [installing lib on Pico](https://dev.blues.io/tools-and-sdks/firmware-libraries/python-library/)
* [Getting Started (useful intro video)](https://blues.io/blog/get-started-cellular-raspberry-pi-webinar/)
* [Notecarrier A and GPS](https://www.hackster.io/rob-lauer/sending-a-cellular-gps-tracker-around-the-world-literally-4b830c)
* [Quick Start: Notecard and Notecarrier](https://dev.blues.io/quickstart/notecard-quickstart/notecard-and-notecarrier-f/)
* [Transforming data](https://dev.blues.io/guides-and-tutorials/routing-data-to-cloud/general-http-https/)
* [Notecard Built-in time and location](https://dev.blues.io/notecard/notecard-walkthrough/time-and-location-requests/)
    * Enabling GPS periodic, only checks when motion has been detected.
    * In the request then, `"best_location_type":"gps"`
* [Creating Routes, Using webhook for testing](https://dev.blues.io/guides-and-tutorials/routing-data-to-cloud/general-http-https/#introduction)
* [SDK (python)](https://dev.blues.io/tools-and-sdks/firmware-libraries/python-library/)
* [Adding Cellular to the Raspberry Pi Pico with the Blues Wireless Notecard Video](https://www.youtube.com/watch?v=rxq9vc1sW_0)
* [Notecard coverage comparison](https://dev.blues.io/datasheets/notecard-datasheet/note-nbna-500/)

### Adafruit
* Notes about BME680 library.
    * [Using Adafruit's library](https://github.com/adafruit/Adafruit_CircuitPython_BME680/blob/main/adafruit_bme680.py)
    * Renamed adafruit_bme680.py in this project to adafruit_bme680_cp.py to avoid conflicts from micropython bme680 packages (listed above).
* [Adafruit: working with two I2C devices](https://learn.adafruit.com/working-with-multiple-i2c-devices/two-devices-using-alternate-address)
* [Adafruit Feather RP2040 and I2C](https://picockpit.com/raspberry-pi/circuitpython-adafruit-feather-rp2040-and-i2c/)
* [Adafruit Feather RP2040 Pinout](https://learn.adafruit.com/adafruit-feather-rp2040-pico/pinouts)
* [Adafruit Feather M4 on Notecarrier with CircuitPython](https://dev.blues.io/guides-and-tutorials/collecting-sensor-data/notecarrier-f/adafruit-feather-m4-express/circuitpython/)
* [Getting started with Raspberry Pi Pico and CircuitPython ](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/overview)
* [CircuitPython Essentials](https://learn.adafruit.com/circuitpython-essentials/circuitpython-pins-and-modules)
* [Feather RP2040](https://learn.adafruit.com/adafruit-feather-rp2040-pico)
* [Introducing the New Feather Compatible Notecarrer](https://dev.blues.io/guides-and-tutorials/collecting-sensor-data/notecarrier-f/adafruit-feather-m4-express/circuitpython/)
* [More from Adafuit on Notecarrier](https://blog.adafruit.com/2021/12/02/eye-on-npi-blues-wireless-notecard-cellular-modem-modules-and-notecarriers-eyeonnpi-digikey-digikey-blueswireless/)

### Other References
* [Drop micropython on Pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
* [micropython docs](https://docs.micropython.org/en/latest/rp2/quickref.html)
* https://www.robmiles.com/journal/2021/9/27/pico-and-feather-what-are-the-differences
* https://dev.blues.io/notecard/notecard-walkthrough/time-and-location-requests/
* [Detecting USB/battery power](https://forums.raspberrypi.com/viewtopic.php?t=300676)
