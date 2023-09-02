### Notes
* `code_cpx.py` for Adafruit Circuit Playground Express

### References:
* [rp2040 mp3](https://learn.adafruit.com/mp3-playback-rp2040)
* [musical notes](https://learn.adafruit.com/circuit-playground-music/the-sound-of-music)
* [adafruit switches](https://learn.adafruit.com/make-it-switch/other-types-of-switches)
    * [coding switches](https://learn.adafruit.com/make-it-switch/code-your-micro)
    * [debouncing](https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/keys-one-key-per-pin)
### Sax-A-Boom wav files
* Reference: https://github.com/david6983/saxaboom/tree/master
* ffmpeg (sbLoop.wav is rhythm and is the longest duration):
    * ffmpeg -i sbLoop.wav -i sbLoop1.wav -filter_complex amix=inputs=2:duration=longest:dropout_transition=0:weights="0.40 1":normalize=0 rhythm_and_track1.mp3 
    * ffmpeg -i sbLoop.wav -i sbLoop2.wav -filter_complex amix=inputs=2:duration=shortest:dropout_transition=0:weights="0.40 1":normalize=0 rthymn_and_track2_short.mp3



### References, not directly relevant
* [circuitplayground: play tone](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/play-tone)
* [rp2040 PIO CircuitPython](https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/overview)


<!---
# vim: ai et ts=4 sw=4 sts=4 nu
-->
