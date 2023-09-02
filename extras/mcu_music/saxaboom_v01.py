import time

import board
import audiomp3
from audiopwmio import PWMAudioOut as AudioOut

#from digitalio import DigitalInOut, Direction, Pull
import keypad

# range: 0.1 - 1.0
TONE_VOLUME = 0.5
CURRENTLY_PLAYING = '' 

audio = AudioOut(board.GP0)

rhythm = audiomp3.MP3Decoder(open("/sax_music/rhythm.mp3", "rb"))
track1 = audiomp3.MP3Decoder(open("/sax_music/track1.mp3", "rb"))
track2 = audiomp3.MP3Decoder(open("/sax_music/track2.mp3", "rb"))
rhythm_and_track1 = audiomp3.MP3Decoder(open("/sax_music/rhythm_and_track1_short.mp3", "rb"))
rhythm_and_track2 = audiomp3.MP3Decoder(open("/sax_music/rhythm_and_track2_short.mp3", "rb"))

# https://github.com/adafruit/circuitpython/issues/5136
# Documents clipping
KEY_PINS = (
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
)

MP3_CODES = (
        ('Stop the music', track1),
        ('Track 1', track1),
        ('Track 2', track2),
        ('Rhythm', rhythm),
        ('Play rhythm and track', ''),
)

MP3_CODES_RHYTHM = (
        ('Stop the music', track1),
        ('Rhythm and Track 1', rhythm_and_track1),
        ('Rhythm and Track 2', rhythm_and_track2),
        ('Rhythm', rhythm),
        ('Play rhythm and track', ''),
)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

PLAY_MP3_CODES = True
CURRENT_KEY_NUMBER = None

while True:
    event = keys.events.get()
    if event and event.pressed:

        if event.key_number == 4:
            PLAY_MP3_CODES = not PLAY_MP3_CODES 
            # Switch what is being played:
            print(f'#4: CURRENT_KEY_NUMBER: {CURRENT_KEY_NUMBER}')
            if CURRENT_KEY_NUMBER not in [0,4]:
                if PLAY_MP3_CODES:
                    key, mp3 = MP3_CODES[CURRENT_KEY_NUMBER]
                    CURRENTLY_PLAYING = key
                else:
                    key, mp3 = MP3_CODES_RHYTHM[CURRENT_KEY_NUMBER]
                    CURRENTLY_PLAYING = key

                audio.stop()
                audio.play(mp3, loop=True)

                print(f'#4: event.key_number: {event.key_number}')
                print(f'#4: PLAY_MP3_CODES: {PLAY_MP3_CODES}')
                print(f'#4: CURRENTLY_PLAYING: {CURRENTLY_PLAYING}')
            continue

        print(f'event.key_number: {event.key_number}')
        print(f'PLAY_MP3_CODES: {PLAY_MP3_CODES}')

        if PLAY_MP3_CODES:
            key, mp3 = MP3_CODES[event.key_number]
        else:
            key, mp3 = MP3_CODES_RHYTHM[event.key_number]

        if event.key_number == 0:
            audio.stop()
            CURRENTLY_PLAYING = ''
        elif CURRENTLY_PLAYING != key:
            audio.stop()
            CURRENTLY_PLAYING = key
            audio.play(mp3, loop=True)
        else:
            print('Do nothing #1')
            pass

        CURRENT_KEY_NUMBER = event.key_number

        print(f'END: CURRENTLY_PLAYING: {CURRENTLY_PLAYING}')


# vim: ai et ts=4 sts=4 sw=4 nu
