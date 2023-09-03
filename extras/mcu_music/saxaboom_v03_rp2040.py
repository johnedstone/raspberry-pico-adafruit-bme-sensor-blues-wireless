"""
wave: https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
ffmpeg:
    ffmpeg -i sbLoop.wav -i sbLoop1.wav \
            -filter_complex amix=inputs=2:duration=shortest:dropout_transition=0:weights="1 1":normalize=0 \
            -bitexact -ac 1 -ar 22050  sbLoop1_rhythm.wav
"""
import time

import board

from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

import keypad

# range: 0.1 - 1.0
TONE_VOLUME = 0.5
CURRENTLY_PLAYING = '' 

audio = AudioOut(board.A0)


track1_file = open("/sax_music/sbLoop1.wav", "rb")
track1_wave = WaveFile(track1_file)
track2_file = open("/sax_music/sbLoop2.wav", "rb")
track2_wave = WaveFile(track2_file)
#track3_file = open("/sax_music/sbLoop3.wav", "rb")
#track3_wave = WaveFile(track3_file)

track1_rhythm_file = open("/sax_music/sbLoop1_rhythm.wav", "rb")
track1_rhythm_wave = WaveFile(track1_rhythm_file)
track2_rhythm_file = open("/sax_music/sbLoop2_rhythm.wav", "rb")
track2_rhythm_wave = WaveFile(track2_rhythm_file)
#track3_rhythm_file = open("/sax_music/sbLoop3_rhythm.wav", "rb")
#track3_rhythm_wave = WaveFile(track3_rhythm_file)

KEY_PINS = (
        board.D24, # Stop the music
        board.D25, # Track 1
        board.D4,  # Track 2
        board.D12, # No Loop
        board.D13, # Toggle Rhythm
)

WAVE_CODES = (
        ('Stop the music', ''),
        ('Track 1', track1_wave),
        ('Track 2', track2_wave),
        ('Toggle Loop', ''),
        ('Toggle Rhythm', ''),
)

WAVE_CODES_RHYTHM = (
        ('Stop the music', ''),
        ('Track 1 Plus Rhythm', track1_rhythm_wave),
        ('Track 2 Plus Rhythm', track2_rhythm_wave),
        ('Toggle Loop', ''),
        ('Toggle Rhythm', ''),
)

STOP_KEY = 0
TOGGLE_LOOP_KEY = 3
TOGGLE_RHYTHM_KEY = 4

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

PLAY_WAVE_CODES = True # That is, no rhythm
PLAY_LOOP = True

CURRENT_KEY_NUMBER = None

while True:
    event = keys.events.get()
    if event and event.pressed:
        if event.key_number in [TOGGLE_RHYTHM_KEY, TOGGLE_LOOP_KEY]:
            if event.key_number == TOGGLE_RHYTHM_KEY:
                PLAY_WAVE_CODES = not PLAY_WAVE_CODES 
            else:
                PLAY_LOOP = not PLAY_LOOP 

            # Switch wave file
            if CURRENT_KEY_NUMBER not in [STOP_KEY, TOGGLE_RHYTHM_KEY, TOGGLE_LOOP_KEY]:
                if PLAY_WAVE_CODES:
                    key, wave = WAVE_CODES[CURRENT_KEY_NUMBER]
                else:
                    key, wave = WAVE_CODES_RHYTHM[CURRENT_KEY_NUMBER]

                audio.stop()
                try:
                    audio.play(wave, loop=PLAY_LOOP)
                except Exception as e:
                    print(f'Error playing audio: {e}')

                CURRENTLY_PLAYING = key

                print(f'Toggle: event.key_number: {event.key_number}')
                print(f'Toggle: PLAY_WAVE_CODES: {PLAY_WAVE_CODES}')
                print(f'Toggle: CURRENTLY_PLAYING: {CURRENTLY_PLAYING}')
                print(f'Toggle: PLAY_LOOP: {PLAY_LOOP}')

            continue

        # Below then, are the track keys and the stop key
        print(f'event.key_number: {event.key_number}')
        print(f'PLAY_WAVE_CODES: {PLAY_WAVE_CODES}')

        if PLAY_WAVE_CODES:
            key, wave = WAVE_CODES[event.key_number]
        else:
            key, wave = WAVE_CODES_RHYTHM[event.key_number]

        if event.key_number == STOP_KEY:
            audio.stop()
            CURRENTLY_PLAYING = ''
        elif not PLAY_LOOP or (CURRENTLY_PLAYING != key and PLAY_LOOP):
            audio.stop()
            CURRENTLY_PLAYING = key

            try:
                audio.play(wave, loop=PLAY_LOOP)
            except Exception as e:
                print(f'Error playing audio: {e}')

        else:
            print('Do nothing')
            pass

        CURRENT_KEY_NUMBER = event.key_number

        print(f'END: CURRENTLY_PLAYING: {CURRENTLY_PLAYING}')

# vim: ai et ts=4 sts=4 sw=4 nu
