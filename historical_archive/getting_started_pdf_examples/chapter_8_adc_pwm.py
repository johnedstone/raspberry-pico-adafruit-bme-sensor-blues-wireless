import machine
import utime

potentiometer = machine.ADC(26)
sensor_temp = machine.ADC(4)
led = machine.PWM(machine.Pin(15))

conversion_factor = 3.3 / (65535)
led.freq(1000)


while True:
    #print(f'potentiometer: {potentiometer.read_u16() * conversion_factor}')
    #reading = sensor_temp.read_u16() * conversion_factor
    #temperature = 27 - (reading - 0.706)/0.001721
    #print(f'cpu temperature: {temperature}')
    #utime.sleep(2)
    led.duty_u16(potentiometer.read_u16())
    