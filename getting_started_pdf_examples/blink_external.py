import machine
import utime

led_external = machine.Pin(15, machine.Pin.OUT)

try:
    while True:
        print('boo')
        led_external.toggle()
        utime.sleep(5)
except Exception as e:
    print(f'{e}')
    print(f'{type(e)}')