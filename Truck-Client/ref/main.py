import board
import busio
import adafruit_vl53l0x
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

while True:
    rge = sensor.range
    print(f"Range: {rge / 25.4}.")
    time.sleep(0.5)
