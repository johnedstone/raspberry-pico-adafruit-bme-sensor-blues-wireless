import machine
import utime
import _thread

led_red = machine.Pin(15, machine.Pin.OUT)
led_amber = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(13, machine.Pin.OUT)
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(12, machine.Pin.OUT)

global button_pressed
button_pressed = False

def button_reader_thread():
    global button_pressed
    counter = 1
    while True:
        if button.value() == 1:
            button_pressed = True
            print(f'button pressed: {counter}')
            counter += 1
        utime.sleep(0.01)

_thread.start_new_thread(button_reader_thread, ())

try:
    while True:
        if button_pressed == True:
            led_red.value(1)
            for i in range(10):
                buzzer.value(1)
                utime.sleep(0.2)
                buzzer.value(0)
                utime.sleep(0.2)
            global button_pressed
            button_pressed = False
            print('button turned off')
            
        led_red.value(1)
        utime.sleep(5)
        led_amber.value(1)
        #print('should be amber for at least 2 seconds')
        utime.sleep(2)
        led_red.value(0)
        led_amber.value(0)
        led_green.value(1)
        utime.sleep(5)
        led_green.value(0)
        led_amber.value(1)
        utime.sleep(5)
        led_amber.value(0)
        print('again')
        #utime.sleep(5)
except Exception as e:
    print(f'{e}')
    print(f'{type(e)}')