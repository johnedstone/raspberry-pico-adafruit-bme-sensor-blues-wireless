"""
wave: https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
ffmpeg example:
    ffmpeg -i sbLoop.wav -i sbLoop1.wav \
            -filter_complex amix=inputs=2:duration=shortest:dropout_transition=0:weights="1 1":normalize=0 \
            -bitexact -ac 1 -ar 22050  sbLoop1_rhythm.wav

Monitor: sudo screen /dev/ttyACM0 115200
"""
from time import sleep

import board
import digitalio

from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

import keypad

import adafruit_logging as logging
logger = logging.getLogger('saxaboom')

#logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

play_once = digitalio.DigitalInOut(board.D5)
play_once.pull = digitalio.Pull.UP  # True/False when switch Open/Closed

# range: 0.1 - 1.0
TONE_VOLUME = 0.5

audio = AudioOut(board.A0)


track0_file = open("/sax_music/sbLoop.wav", "rb")
track0_wave = WaveFile(track0_file)
track1_file = open("/sax_music/sbLoop1.wav", "rb")
track1_wave = WaveFile(track1_file)
track2_file = open("/sax_music/sbLoop2.wav", "rb")
track2_wave = WaveFile(track2_file)
track3_file = open("/sax_music/sbLoop3.wav", "rb")
track3_wave = WaveFile(track3_file)
track4_file = open("/sax_music/sbLoop4.wav", "rb")
track4_wave = WaveFile(track4_file)
track5_file = open("/sax_music/sbLoop5.wav", "rb")
track5_wave = WaveFile(track5_file)
track6_file = open("/sax_music/sbLoop6.wav", "rb")
track6_wave = WaveFile(track6_file)
track8_file = open("/sax_music/sbLoop8.wav", "rb")
track8_wave = WaveFile(track8_file)


KEY_PINS = (
        board.D24, # Stop the music
        board.D25, # Track 0 Rhythm
        board.D4,  # Track 8
        board.D13, # Track 6
        board.D12, # Track 5
        board.D11, # Track 4
        board.D10, # Track 3
        board.D9,  # Track 2
        board.D6,  # Track 1
)

WAVE_CODES = (
        ('Stop the music', ''),  # Stop the music
        ('Track 0', track0_wave), # Rhythm
        ('Track 8', track8_wave),
        ('Track 6', track6_wave),
        ('Track 5', track5_wave),
        ('Track 4', track4_wave),
        ('Track 3', track3_wave),
        ('Track 2', track2_wave),
        ('Track 1', track1_wave),
)


STOP_KEY = 0
MUSIC_KEYS = range(1,9) 

try:
    PLAY_ONCE = play_once.value  # Default when switch is not closed
except Exception as e:
    logger.error(f'PLAY_ONCE not detected, setting to True')
    PLAY_ONCE = True  # Default when switch is not closed

logger.info(f'PLAY_ONCE: {PLAY_ONCE}')

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

while True:
    event = keys.events.get()

    try:
        current_play_once = play_once.value

        if current_play_once == PLAY_ONCE:
            pass # no change
        else:
            PLAY_ONCE = current_play_once
            audio.stop()
            logger.info(f'PLAY_ONCE changed to {current_play_once}')
            continue

    except Exception as e:
        logger.error(f'error getting play_once: {e}')

    if event and event.pressed:
        logger.debug(f"Start of while loop, key pressed: {event.key_number}")
        if event.key_number == STOP_KEY:
            audio.stop()
            logger.info(f"STOP")
            continue

        if event.key_number in MUSIC_KEYS:
            logger.info(f"event.key_number: {event.key_number} | MUSIC_KEYS: {MUSIC_KEYS}")
            key, wave = WAVE_CODES[event.key_number]
            try:
                audio.stop()
                audio.play(wave, loop=not PLAY_ONCE)
            except Exception as e:
                logger.error(f"Error playing audio: {e}")
            finally:
                logger.info(f"END: key: {key}")
        else:
            logger.warning("PASS: how did we get here?")

# vim: ai et ts=4 sts=4 sw=4 nu
