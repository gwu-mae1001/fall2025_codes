"""
==== Realtime video captuer and filtering toward IoT applications
==== Source code written by Prof. Kartik Bulusu
==== CS and MAE Department, SEAS GWU
==== Description:
======== Video capture and real-time image filtering using OpenCV toward IoT applications
========
==== Requirements:
============ The program requires Python 3.9.x dependent libraries:
============ OpenCV 4.6.x, picamera2
======== It has been written exclusively for CS4907 students in GWU.
======== It may not be used for any other purposes unless author's prior permission is aquired.
==== Testing:
==== 1. Developed and tested on 03/01/2024 using Python 3.9.x on Raspberry Pi 4B
"""

# from picamera.array import PiRGBArray
from picamera2 import Picamera2
import time
import numpy as np
import cv2

# initialize the camera and grab a reference to the raw camera capture
picam2 = Picamera2()
# picam2.resolution = (640, 480)
picam2.resolution = (320, 240)
picam2.framerate = 32
picam2.rotation = 180

picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": picam2.resolution}))
picam2.start()


# allow the camera to warmup
time.sleep(0.1)


# capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while True:
    
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)
    edges = cv2.Canny(frame, 100, 200)
#     
    cv2.imshow('original', frame)
    cv2.imshow('laplacian', laplacian)
    cv2.imshow('sobelx', sobelx)
    cv2.imshow('sobely', sobely)
    cv2.imshow('edges', edges)
    
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()