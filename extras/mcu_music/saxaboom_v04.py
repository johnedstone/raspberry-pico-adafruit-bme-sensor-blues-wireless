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

import adafruit_logging as logging
logger = logging.getLogger('saxaboom')

#logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

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
MUSIC_KEYS = [1, 2]

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

PLAY_WAVE_CODES = True # That is, no rhythm
PLAY_LOOP = False

CURRENT_KEY = ''
CURRENT_KEY_NUMBER = None

while True:
    event = keys.events.get()
    if event and event.pressed:
        logger.debug(f"Start of loop, key pressed: {event.key_number}")
        if event.key_number == STOP_KEY:
            audio.stop()
            CURRENTLY_KEY = ''
            CURRENT_KEY_NUMBER = None
            logger.info(f"STOP and CURRENTLY_PLAYING: {CURRENTLY_PLAYING}")
            continue

        if event.key_number == TOGGLE_LOOP_KEY:
            audio.stop()
            CURRENTLY_KEY = ''
            CURRENT_KEY_NUMBER = None
            PLAY_LOOP = not PLAY_LOOP 
            logger.info(f"STOP and PLAY_LOOP Value: {PLAY_LOOP}")
            continue

        if event.key_number == TOGGLE_RHYTHM_KEY:
            PLAY_WAVE_CODES = not PLAY_WAVE_CODES 

            try:
                if CURRENT_KEY_NUMBER:
                    if PLAY_WAVE_CODES:
                        key, wave = WAVE_CODES[CURRENT_KEY_NUMBER]
                    else:
                        key, wave = WAVE_CODES_RHYTHM[CURRENT_KEY_NUMBER]

                    if PLAY_LOOP:
                        audio.stop()
                        audio.play(wave, loop=PLAY_LOOP)
                        CURRENT_KEY = key
                    else:
                        continue
                else:
                    continue
            except Exception as e:
                logger.error(f"Error playing audio during rhythm toggle: {e}")

            finally:
                logger.info(f"Toggle: event.key_number: {event.key_number}")
                logger.info(f"Toggle: PLAY_WAVE_CODES: {PLAY_WAVE_CODES}")
                logger.info(f"Toggle: PLAY_LOOP: {PLAY_LOOP}")
                logger.info(f"Toggle: CURRENTLY_KEY_NUMBER: {CURRENT_KEY_NUMBER}")
                logger.info(f"Toggle: CURRENTLY_KEY: {CURRENT_KEY}")

            continue

        if event.key_number in MUSIC_KEYS:
            logger.info(f"event.key_number: {event.key_number} | MUSIC_KEYS: {MUSIC_KEYS}")
            if PLAY_WAVE_CODES:
                key, wave = WAVE_CODES[event.key_number]
            else:
                key, wave = WAVE_CODES_RHYTHM[event.key_number]

            try:
                audio.stop()
                audio.play(wave, loop=PLAY_LOOP)
                if PLAY_LOOP:
                    CURRENT_KEY = key
                    CURRENT_KEY_NUMBER = event.key_number
                else:
                    CURRENTLY_KEY = ''
                    CURRENT_KEY_NUMBER = None
            except Exception as e:
                logger.error(f"Error playing audio: {e}")
            finally:
                logger.info(f"event.key_number: {event.key_number}")
                logger.info(f"PLAY_WAVE_CODES: {PLAY_WAVE_CODES}")
                logger.info(f"PLAY_LOOP: {PLAY_LOOP}")
                logger.info(f"CURRENT_KEY_NUMBER: {CURRENT_KEY_NUMBER}")
                logger.info(f"END: CURRENT_KEY: {CURRENT_KEY}")
        else:
            logger.warning("PASS: how did we get here?")

# vim: ai et ts=4 sts=4 sw=4 nu
