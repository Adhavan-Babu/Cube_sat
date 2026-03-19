# The following file will be used to test the different components of the software before merging them in cubesat.py
# The following components are: Camera Clicking, Inertial and Gyroscope testing, Uploading images to github  

import time
import board
import os
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

# --- VARIABLES ---
THRESHOLD = 4                           # Desired value from the accelerometer
REPO_PATH = "/home/nikhil/Cube_sat"     # Your github repo path
FOLDER_PATH = "images"                  # Your image folder path in your GitHub repo

# --- HARDWARE SETUP ---
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)

def img_gen(name):
    """Generates a new image name with timestamp."""
    t = time.strftime("_%H%M%S")
    return os.path.join(REPO_PATH, FOLDER_PATH, f"{name}{t}.jpg")
def is_moving(threshold=2):
    """Detects motion based on accelerometer data."""
    accelx, accely, accelz = accel_gyro.acceleration

    accelz -= 10 #This is only used for testing purposes, to simulate motion since we are not in zero G environment. Remove this line when testing in space or zero G environment.

    magnitude = (accelx**2 + accely**2 + accelz**2)**0.5
    print(f"Acceleration Magnitude: {magnitude:.2f} m/s^2")
    return magnitude > threshold



def git_push():
    """Stages, commits, and pushes new images to your GitHub repo."""
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('Connecting to remote...')
        origin.pull()
        print('Pulled changes.')
        
        repo.git.add(os.path.join(REPO_PATH, FOLDER_PATH))
        print("Added images to git.")
        
        repo.index.commit('New Photo')
        print('Committed changes.')
        
        origin.push()
        print('Pushed successfully!')
    except Exception as e:
        print(f"Couldn't upload to git: {e}")

def run_mission_test(iterations=2):
    """Modularized function to handle camera capture and git upload."""
    print(f"Starting mission test for {iterations} iterations...")
    i = 1
    while(True):

            if is_moving():
                print("Motion detected! Capturing image...")
                # Capture image code here
                # For example:

     
            
                # Start camera
                picam2.start(show_preview=False)
                # Set focus to infinity for space/long distance
                picam2.set_controls({"AfMode": 0, "LensPosition": 0.0})
                
                print("Camera ready...")
                time.sleep(2) 

                # Generate name and capture
                image_name = img_gen("NikhilS")
                print(f"Capturing: {image_name}")
                picam2.capture_file(image_name)
                
                # Release camera hardware
                picam2.stop()
                print("Photo saved and camera released.")

                # Upload to GitHub
                git_push()

                i = i + 1

                
            

            else:
                print("No motion detected. Waiting...")

            time.sleep(0.1)  # Adjust the sleep time as needed



            #Exit Condition for testing purposes

            if i > iterations:
                print(f"Completed {iterations} iterations. Ending test.")
                break

# --- MAIN EXECUTION ---
try:
    run_mission_test(2)
finally:
    # Final safety check to ensure hardware is closed
    picam2.stop()
    print("\nTest complete.")