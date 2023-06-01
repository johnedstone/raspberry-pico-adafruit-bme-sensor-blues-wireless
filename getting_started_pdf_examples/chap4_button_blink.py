import machine
import utime

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
led_external = machine.Pin(15, machine.Pin.OUT)

while True:
    if button.value() == 1:
        print("Button has been pushed")
        #led_external.value(1)
        led_external.toggle()
        utime.sleep(2)
    #led_external.value(0)
    # comment