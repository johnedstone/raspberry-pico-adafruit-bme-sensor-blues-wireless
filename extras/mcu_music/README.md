### References:
* [rp2040 mp3](https://learn.adafruit.com/mp3-playback-rp2040)
* [musical notes](https://learn.adafruit.com/circuit-playground-music/the-sound-of-music)
* [adafruit switches](https://learn.adafruit.com/make-it-switch/other-types-of-switches)
    * [coding switches](https://learn.adafruit.com/make-it-switch/code-your-micro)
    * [debouncing](https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/keys-one-key-per-pin)
* [feather power switch](https://io.adafruit.com/blog/tip/2016/12/14/feather-power-switch/) 
* [rp2040 pinout](https://learn.adafruit.com/adafruit-feather-rp2040-pico/pinouts)
* [Wiring Adafruit PAM8302A](https://learn.adafruit.com/adafruit-pam8302-mono-2-5w-class-d-audio-amplifier/pinouts)

### Sax-A-Boom wave files
* script: `saxaboom_v04.py`
* [Link to hardware_image_saxaboom_v04 rp2040 adafruit feather](media/saxaboom_v04.png)
* [Link to hardware image saxaboom_v03_rp2040_music_and_rhythm.py](media/saxaboom_v03_rp2040_music_and_rhythm.png)
* [Link to hardware image saxaboom_v02_pico.py](media/saxaboom_v02_pico.png)
* [Adafruit Feather RP2040](https://learn.adafruit.com/adafruit-feather-rp2040-pico)
* Amplifier: Adafruit PAM8302A
* Adafruit Mono Enclosed Speaker - 3W 4 Ohm Product ID: 3351 
* Adafruit Breadboard trim potentiometer - 10K Product ID: 356 
* [Original Sax-a-Boom wave files](https://github.com/david6983/saxaboom/tree/master/Samples)
* _Note:_ All wave files where remade and/or created with ffmpeg using at least this argument `-bitexact -ac 1  -ar 22050`
```
ffmpeg -i sbLoop1_orig.wav -bitexact -ac 1  -ar 22050  sbLoop1.wav

ffmpeg -i sbLoop.wav -i sbLoop1.wav -filter_complex amix=inputs=2:duration=shortest:dropout_transition=0:weights="1 1":normalize=0 -bitexact -ac 1  -ar 22050  sbLoop1_rhythm.wav
```

### Sax-A-Boom mp3 files _ignore because of audiomp3.MP3Decoder clipping at start_
* [Documentation:clipping audiomp3.MP3Decoder](https://github.com/adafruit/circuitpython/issues/5136)
* script: `saxaboom_v01.py`
* Raspberry Pi Pico
* Amplifier: Adafruit PAM8302A
* Adafruit Mono Enclosed Speaker - 3W 4 Ohm Product ID: 3351 
* Adafruit Breadboard trim potentiometer - 10K Product ID: 356 
* **Problem:** clipping sound for PWMAudioOut at the beginning of each loop :(
* Workaround: use wave files, not mp3
* Reference: https://github.com/david6983/saxaboom/tree/master
* ffmpeg (sbLoop.wav is rhythm and is the longest duration):
    * `ffmpeg -i sbLoop.wav -i sbLoop1.wav -filter_complex amix=inputs=2:duration=longest:dropout_transition=0:weights="0.40 1":normalize=0 rhythm_and_track1.mp3`
    * `ffmpeg -i sbLoop.wav -i sbLoop2.wav -filter_complex amix=inputs=2:duration=shortest:dropout_transition=0:weights="0.40 1":normalize=0 rthymn_and_track2_short.mp3`
    * `ffmpeg -i sbLoop.wav -i sbLoop2.wav -filter_complex amix=inputs=2:duration=shortest:dropout_transition=0:weights="1 1":normalize=0 rthymn_and_track2_short_equal.mp3`

### Adafruit Circuit Playground Express
* `code_cpx.py` for Adafruit Circuit Playground Express

### References, not directly relevant
* [circuitplayground: play tone](https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/play-tone)
* [rp2040 PIO CircuitPython](https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/overview)

#### I2S
* Amplifier: [Adafruit I2S 3W Class D Amplifier Breakout - MAX98357A](https://www.adafruit.com/product/3006)
* Reference: https://learn.adafruit.com/mp3-playback-rp2040/pico-i2s-mp3


<!---
# vim: ai et ts=4 sw=4 sts=4 nu
-->
