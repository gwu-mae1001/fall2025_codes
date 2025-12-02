"""
==== Face detection using OpenCV pretrained model toward IoT applications
==== Source code written by Prof. Kartik Bulusu
==== CS and MAE Department, SEAS GWU
==== Description:
======== Face detection using OpenCV pretrained model
======== https://github.com/opencv/opencv/tree/4.x/data/haarcascades
========
==== Requirements:
============ The program requires Python 3.9.2 dependent libraries:
============ OpenCV 4.6.0, picamera2
======== It has been written exclusively for CS4907 students in GWU.
======== It may not be used for any other purposes unless author's prior permission is aquired.
==== Testing:
==== 1. Developed and tested on 03/01/2024 using Python 3.9.x on Raspberry Pi 4B
==== Reference: # https://github.com/opencv/opencv/tree/4.x/data/haarcascades
"""

import cv2

from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
assert not face_detector.empty()
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    cv2.imshow("Camera", im)
    cv2.waitKey(1)

cv2.destroyAllWindows()