import time

import board
import audiomp3
from audiopwmio import PWMAudioOut as AudioOut

#from digitalio import DigitalInOut, Direction, Pull
import keypad

# range: 0.1 - 1.0
TONE_VOLUME = 0.5

audio = AudioOut(board.GP0)

#decoder = audiomp3.MP3Decoder(open("/music/somewhere_2min.mp3", "rb"))
decoder = audiomp3.MP3Decoder(open("/music/somewhere_01.mp3", "rb"))

KEY_PINS = (
        board.GP6,
)

NOTE_CODES = (
        ('Somewhere ...', decoder),
)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

while True:
    event = keys.events.get()
    if event:
        key, tone = NOTE_CODES[event.key_number]
        if event.pressed:
            audio.stop()
            print(f'playing: {key}')
            if key == 'Somewhere ...':
                audio.play(decoder, loop=True)
            else:
                pass

        #if event.released:
        #    print(f'stoping: {key}')
        #    audio.stop()

# vim: ai et ts=4 sts=4 sw=4 nu
