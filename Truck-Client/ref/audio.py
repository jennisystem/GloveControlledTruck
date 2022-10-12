# Write your code here :-)
import time
import board
from busio import I2C
import adafruit_bme680
import audioio
import digitalio
import audiocore

# import our utilites
import utils as u

# set up the SPI bus, and mount the sd card as "/sd"
u.mount_sd()

# open a file with append on the sd card, which is mounted at /sd
wave_file = open("/sd/bark.wav", "rb")
wave = audiocore.WaveFile(wave_file)
audio = audioio.AudioOut(board.A0)
while True:
    print("playing!")
    audio.play(wave)
    time.sleep(5)
