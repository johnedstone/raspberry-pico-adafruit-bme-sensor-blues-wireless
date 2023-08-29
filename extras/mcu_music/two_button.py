import board
import audiomp3

import time
import array
import math
import board
from audiocore import RawSample
from audiopwmio import PWMAudioOut as AudioOut

from digitalio import DigitalInOut, Direction, Pull

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

# a
#decoder = audiomp3.MP3Decoder(open("/music/somewhere_2min.mp3", "rb"))
decoder = audiomp3.MP3Decoder(open("/music/somewhere_01.mp3", "rb"))

# b
note_C4_freq = 262

if not True:
    audio.play(decoder)
    while audio.playing:
        pass

    print("Done playing!")
if True:
    #length = 8000 // tone_frequency
    #sine_wave = array.array("H", [0] * length)
    #for index in range(length):
    #    sine_wave[index] = int((1 + math.sin(math.pi * 2 * index / length))
    #                           * tone_volume * (2 ** 15 - 1))
    #sine_wave_sample = RawSample(sine_wave)
    sine_wave_sample = get_note(note_C4_freq)

    #print(f'tone_frequency: {tone_frequency}')
    audio.play(sine_wave_sample, loop=True)
    time.sleep(1.5)
    audio.stop()
    time.sleep(1)


button_note_C4 = DigitalInOut(board.GP1)
button_note_C4.direction = Direction.INPUT
button_note_C4.pull = Pull.UP

button_note_D4 = DigitalInOut(board.GP2)
button_note_D4.direction = Direction.INPUT
button_note_D4.pull = Pull.UP

while not True:
    if not button_note_C4.value:
        print("Button activated")

# vim: ai et ts=4 sts=4 sw=4 nu
