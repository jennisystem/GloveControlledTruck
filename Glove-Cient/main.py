# Write your code here :-)
from analogio import AnalogIn
import board
import time

analog_in = AnalogIn(board.A0)

while True:
    print((analog_in.value - 18000) / 14000)
    time.sleep(0.1)
