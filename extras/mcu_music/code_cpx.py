"""
-bitexact -acodec pcm_s16le -ac 1 -ar 22050
https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/issues/97
"""
import sys 
from adafruit_circuitplayground.express import cpx

while True:
    if cpx.switch:
        print("slide switch off!")
        cpx.pixels.fill((0, 0, 0))
        cpx.stop_tone()
        continue

    print("slide switch ok!")
    if cpx.touch_A4 and not cpx.touch_A5:
        print('Touched A4!')
        cpx.pixels.fill((15, 0, 0))
        cpx.start_tone(262)
    elif cpx.touch_A5 and not cpx.touch_A4:
        print('Touched A5!')
        cpx.pixels.fill((15, 5, 0))
        cpx.start_tone(294)
    elif cpx.touch_A4 and cpx.touch_A5:
        print('Touched A4 and A5 at the same time!')
        cpx.pixels.fill((25, 0, 25))
        cpx.play_file('/audio/somewhere.wav')
    elif cpx.touch_A6:
        print('Touched A6!')
        cpx.pixels.fill((15, 15, 0))
        cpx.start_tone(330)
    elif cpx.touch_A7:
        print('Touched A7!')
        cpx.pixels.fill((0, 15, 0))
        cpx.start_tone(346)
    elif cpx.touch_A1:
        print('Touched A1!')
        cpx.pixels.fill((0, 15, 15))
        cpx.start_tone(392)
    elif cpx.touch_A2 and not cpx.touch_A3:
        print('Touched A2!')
        cpx.pixels.fill((0, 0, 15))
        cpx.start_tone(440)
    elif cpx.touch_A3 and not cpx.touch_A2:
        print('Touched A3!')
        cpx.pixels.fill((5, 0, 15))
        cpx.start_tone(494)
    elif cpx.touch_A2 and  cpx.touch_A3:
        print('Touched A2 and A3 at the same time!')
        cpx.pixels.fill((15, 0, 15))
        cpx.start_tone(523)
    elif cpx.touch_A4 and cpx.touch_A5:
        print('Touched A4 and A5 at the same time!')
        cpx.pixels.fill((25, 0, 25))
        cpx.play_file('audio/somewhere.wav')
    else:
        cpx.pixels.fill((0, 0, 0))
        cpx.stop_tone()

# vim: ai et ts=4 sw=4 sts=4 nu
