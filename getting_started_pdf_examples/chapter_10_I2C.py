"""
https://github.com/UCTRONICS/KB0005/tree/master/lcd
"""
import I2C_LCD_driver
import utime

mylcd = I2C_LCD_driver.lcd()

adc = machine.ADC(4)
CONVERSION_FACTOR = 3.3 / 65535

while True:
    reading = adc.read_u16() * CONVERSION_FACTOR
    temperature = 27 - (reading - 0.706) / (0.001721)
    temp_f = (temperature * (9 / 5)) + 32
    mylcd.lcd_display_string(f'Temp: {temperature:.1f} {temp_f:.1f}', 1)
    utime.sleep(2)
    
