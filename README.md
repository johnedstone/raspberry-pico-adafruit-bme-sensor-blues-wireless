### Description
* Getting started with [Blues Wireless](https://blues.io) notecarriers and notecards
* Using microcontrollers, such as Rasperry PI Pico, Adafruit Feather or QT RP2040

#### Note on power
* For development, both the MCU and the Notecarrier are USB powered to the same computer
* In production, only the Notecarrier is powered, and the MCU receives power from the Notecarrier
* The LiPo ([example](https://www.adafruit.com/product/2011)), connected to the Notecarrier, is optional

#### Raspberry Pi Pico
* Using Micropython
* Using Adafruit BME680
* Script _(in progress)_: `pico_notecarrier_a_v2.py`
* Need image of Pico and files

### Micropython Adafruit Feather RP2040
* Using Micropython
* Script: `adafruit_qt_feather_rp2040_mp.py`
* Sensor library:[lib/adafruit_bme680.py](https://github.com/bsatrom/notecard-pico)
* need image here for both NC-F and NC-A
* Need image files

### Circuitpython Adafruit Feather RP2040
* Using Circuitpython
* Script _(in progress)_:
* Sensor library: [Using Adafruit's library](https://github.com/adafruit/Adafruit_CircuitPython_BME680/blob/main/adafruit_bme680.py) renamed for this project to adafruit_bme680_cp.py
* need image here for both NC-F and NC-A
* Need image files
