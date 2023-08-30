import time
import array
import math

import board
import audiomp3
from audiocore import RawSample
from audiopwmio import PWMAudioOut as AudioOut

#from digitalio import DigitalInOut, Direction, Pull
import keypad

# range: 0.1 - 1.0
TONE_VOLUME = 0.5

def get_note(tone_frequency):
    length = 8000 // tone_frequency
    sine_wave = array.array("H", [0] * length)
    for index in range(length):
        sine_wave[index] = int((1 + math.sin(math.pi * 2 * index / length))
                               * TONE_VOLUME * (2 ** 15 - 1))

    return RawSample(sine_wave)

audio = AudioOut(board.GP0)

#decoder = audiomp3.MP3Decoder(open("/music/somewhere_2min.mp3", "rb"))
decoder = audiomp3.MP3Decoder(open("/music/somewhere_01.mp3", "rb"))

note_C4 = get_note(262)
note_E4 = get_note(330)
note_G4 = get_note(392)
chord_C4M = note_C4 + note_E4 + note_G4

KEY_PINS = (
        board.GP1,
        board.GP3,
        board.GP4,
        board.GP5,
)

NOTE_CODES = (
        ('C4', note_C4),
        ('E4', note_E4),
        ('G4', note_G4),
        ('chord_C4M', chord_C4M),
)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

while True:
    event = keys.events.get()
    if event:
        key, tone = NOTE_CODES[event.key_number]
        #print(NOTE_CODES[event.key_number])
        if event.pressed:
            print(f"playing: {key}")
            audio.play(tone, loop=True)
        if event.released:
            print(f"stoping: {key}")
            audio.stop()

# vim: ai et ts=4 sts=4 sw=4 nu
