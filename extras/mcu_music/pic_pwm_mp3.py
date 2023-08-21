"""
Reference:
    https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3

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
