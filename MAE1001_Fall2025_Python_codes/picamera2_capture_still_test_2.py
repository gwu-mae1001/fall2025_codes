"""
==== Still image capture with Raspberry Pi Camera
==== Source code written by Prof. Kartik Bulusu and Gustavo Londono for CS1010-Fall2023
==== CS and MAE Department, SEAS GWU
==== Description:
======== Takes a simple still-image using the connected camera
======== and saves the image to the current directory. displays a countdown before taking picture.
========
==== Requirements:
============ The program requires Python 3.9.2 dependent libraries:
============ OpenCV 4.6.0, picamera2
======== It has been written exclusively for CS1010 and CS4907 students in GWU.
======== It may not be used for any other purposes unless author's prior permission is aquired.
==== Testing:
==== 1. Developed and tested on 11/03/2023 using Python 3.9.2 on Raspberry Pi 4B
"""
# modified by Prof. Kartik Bulusu and Gustavo Londono for CS1010-Fall2023


#imports
from picamera2 import Picamera2
import time

#create an instance of the Picamera2
picam2 = Picamera2()

#set and load the configuration to be used
capture_config = picam2.create_still_configuration(lores={"size": (320, 240)}, display="lores")

#start the camera and display a preview
picam2.start(show_preview=True)

#countdown for picture
countdown = 5
while countdown != 0:
    
    #print the number of seconds left in countdown
    print(countdown)
    
    #wait for one second to pass
    time.sleep(1)
    
    #decrement the countdown variable by 1
    countdown-=1

print("Say Cheese!")

#buffer time to allow for people to say cheese
time.sleep(0.5)

#Take the picture and save it as "image.jpg" to the current directory
picam2.switch_mode_and_capture_file(capture_config, "image5.jpg")

#Turn the camera and preview off
picam2.stop()

#Exit the program and also close the preview window
exit()
