"""
Reference:
    https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3
    What is next: https://embeddedcomputing.com/technology/open-source/i2s-volume-control-with-raspberry-pi-pico-and-circuitpython
                  https://embeddedcomputing.com/technology/processing/interface-io/simple-mp3-audio-playback-with-raspberry-pi-pico
                  https://www.adafruit.com/product/3006
                  https://www.onetransistor.eu/2021/04/media-keys-rpi-pico-circuitpython.html
                  https://github.com/JeremySCook/circuitpython-experiments/blob/main/sound-playback/i2s_mp3_wav_volume_control.py
                  https://forums.adafruit.com/viewtopic.php?t=124233

    device: raspberryp pi pico
"""
# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import audiomp3
import audiopwmio

audio = audiopwmio.PWMAudioOut(board.GP0)

decoder = audiomp3.MP3Decoder(open("/music/somewhere_01.mp3", "rb"))

audio.play(decoder)
while audio.playing:
    pass

print("Done playing!")


# vim: ai et ts=4 sw=4 sts=4 nu
