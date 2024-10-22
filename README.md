### Description
* Getting started with [Blues Wireless](https://blues.io) notecarriers and notecards
* Using microcontrollers, such as Rasperry PI Pico, Adafruit Feather or QT RP2040

### Latest: Blues.io Notecarrier alone.
* Most current configuration: [this script: `extras/Readme_x20894_et_al_USB_Power_Off_with_LiPo_v2.0.md`](https://github.com/johnedstone/raspberry-pico-adafruit-bme-sensor-blues-wireless/blob/main/extras/Readme_x20894_et_al_USB_Power_Off_with_LiPo_v2.0.md)

#### Note on power
* For development, both the MCU and the Notecarrier are USB powered to the same computer
    * Usually, it's best to plug the notecarrier into your computer first, then the MCU,
      as the notecarrier will power both. The MCU plugged in is just to get to the code (Thonny).
      Plugging the MCU in first, then the notecarrier, means that the MCU will power on, but fail, in some cases, to see
      the I2C devices plugged into the notecarrier, as it sometimes doesn't power the notecarrier alone, some _mystery_ here.
* In production, only the Notecarrier is powered, and the MCU receives power from the Notecarrier
* The LiPo ([example](https://www.adafruit.com/product/2011)), connected to the Notecarrier, is optional

### Raspberry Pi Pico
* Using Micropython for rp2040: [link](https://micropython.org/download/rp2-pico/)
* Sensor: Adafruit BME680
* Script _(in progress)_: `pico_notecarrier_a_v2.py`
* Sensor library: [lib/adafruit_bme680.py](https://github.com/bsatrom/notecard-pico) which is a modification for micropython from Adafruit's circuitpython library.

### Micropython Adafruit Feather RP2040
* Using Micropython for rp2040: [link](https://micropython.org/download/ADAFRUIT_FEATHER_RP2040/)
* Sensor: Adafruit BME680
* Script: `adafruit_qt_feather_rp2040_mp.py`
* Sensor library: [lib/adafruit_bme680.py](https://github.com/bsatrom/notecard-pico) which is a modification for micropython from Adafruit's circuitpython library.

### Circuitpython Adafruit Feather RP2040
* Using [Circuitpython for Feather RP2040](https://circuitpython.org/board/adafruit_feather_rp2040/)
* Sensor: Adafruit BME680
* Script: `adafruit_rp2040_sensor_cp.py`
* Sensor library: [Using Adafruit's original library](https://github.com/adafruit/Adafruit_CircuitPython_BME680/blob/main/adafruit_bme680.py) renamed for this project to adafruit_bme680_cp.py

### Images

#### Adafruit Feather RP2040 in Notecarrier F
* Notecarrier F Antennas for WBNA-500 Notecard: GPS [Pulse W3908B0100](https://www.digikey.com/en/products/detail/pulse-electronics/W3908B0100/7667475) and for WBNA-500 [Pulse W6112B0100 cut in half](https://www.digikey.com/en/products/detail/pulse-electronics/W6112B0100/6566097)
* Antenna for NBGL-500: [Taoglas MFX3](https://www.mouser.com/ProductDetail/960-MFX3.07.0150C)

![Notecarrier F/Adafruit Feather RP2040](images/NC-F_feather_rp2040.png)

#### Adafruit Feather RP2040 with Notecarrier A
_Note: ignore numbering on breadboard, as it's a pico-numbered breadboard_
![Notecarrier A/Adafruit Feather RP2040](images/NC-A_feather_rp2040.png)
##### Closeup image
![Notecarrier A/Adafruit Feather RP2040 closup](images/NC-A_feather_rp2040_closeup.png)

#### Adafruit Feather RP2040 with Notecarrier A **with  no breadboard**
_Note: feather is powered by I2C, i.e. no breadboard_
![Notecarrier A/Adafruit Feather RP2040 - No Breadboard](images/NC-A_feather_rp2040_no_breadboard.png)

#### Raspberry Pi Pico with Notecarrier A
Need to test here: changing power config, to using an I2C from notecarrier to pico. This should work, as it does in the other boards.

![Notecarrier A/Raspberry Pi Pico](images/NC-A_pico.png)

#### Extras
See the extras folder for an example of monitoring power with a notecard, notecarrier and a LiPo battery.

<!--
# vim: ai et ts=4 sts=4 sw=4 nu
-->
