import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

def is_moving(threshold=2):
    """Detects motion based on accelerometer data."""
    accelx, accely, accelz = accel_gyro.acceleration

    accelz -= 10 #This is only used for testing purposes, to simulate motion since we are not in zero G environment. Remove this line when testing in space or zero G environment.

    magnitude = (accelx**2 + accely**2 + accelz**2)**0.5
    print(f"Acceleration Magnitude: {magnitude:.2f} m/s^2")
    return magnitude > threshold

while True:

    if is_moving():
        print("Motion detected! Capturing image...")
        # Capture image code here
        # For example:
    else:
        print("No motion detected. Waiting...")

    time.sleep(1)  # Adjust the sleep time as needed