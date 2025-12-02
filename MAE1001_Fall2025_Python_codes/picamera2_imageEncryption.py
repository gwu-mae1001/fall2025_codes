"""
==== Image encryption and decryption with Raspberry Pi Camera and display with OpenCV
==== Source code written by Prof. Kartik Bulusu 
==== CS and MAE Department, SEAS GWU
==== Description:
======== Captures as still image using the connected camera,
======== Perform Ceaser Cipher Encryption and Decryption
======== Saves all image to the current directory.
========
==== Requirements:
============ The program requires Python 3.9.2 dependent libraries:
============ picamera2
======== It has been written exclusively for CS1010 and CS4907 students in GWU.
======== It may not be used for any other purposes unless author's prior permission is aquired.
==== Testing:
==== 1. Developed by Prof. Kartik Bulusu on Raspberry Pi 3B+ for Fall2022
==== 2. Modified and tested on 03/01/2024 using Python 3.9.2 on Raspberry Pi 4B

"""

from picamera2 import Picamera2
from time import sleep
import time
from PIL import Image
import numpy as np
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

camera = Picamera2()
camera.rotation = 180

capture_config = camera.create_still_configuration(lores={"size": (320, 240)}, display="lores")

# camera.start_preview(alpha=200)
camera.start(show_preview=True)


for i in range(2):
    j = i+1
    sleep(2)
    camera.switch_mode_and_capture_file(capture_config, './image%s.jpg' % j)
#     camera.capture('/home/pi/Desktop/Fall2022/Week5-ImageEncrptDecrypt/image%s.jpg' % j)
    print(">>>> Image %s Captured <<<" % j)
    print('')
    
camera.stop()

# Include your SELFIE in the same folder as this file, and Replace picture1.jpeg with your own SELFIE
# if your image is in PNG format, simply substitute .png for .jpeg -for example picture1.png
# code reads your (color) image and converts to a grayscale image. A grayscale image is a 2-dimensional matrix
im = Image.open("image1.jpg")
im_gray = im.convert("L")
# the casting is necessary for the modulo function to work correctly. it converts the 8-bit
# pixel into a 16 bit...We can leave this discussion out for the students.
pix = np.array(im_gray, dtype="int16")

fig = plt.figure()
# display your image as a grayscale (i.e., black and white) image
ax1 = fig.add_subplot(221)
ax1.set_title('My Grayscale Image', fontsize=9)
plt.imshow(pix, cmap='gray')

# Key Image
# Key Image
# this is your key image - include this in the same folder as this file. If you have
# another image, of the same size, that you would like to use as your key then replace
# picture2.jpeg with your key image.
im1 = Image.open("image2.jpg")
im1_gray = im1.convert("L")
key_image = np.array(im1_gray, dtype="int16")

ax2 = fig.add_subplot(222)
ax2.set_title('My Grayscale Key Image', fontsize=9)
plt.imshow(key_image, cmap='gray')

print(">>>> Image 2 is now being used to encrypt Image 1 <<<")
print('')

start = time.time()

# Encryption
# =========== USE FOR LOOPS ================
# Encryption
# =========== USE FOR LOOPS ================
# iterate over the size of the image/matrix
# use the corresponding value in key image as your key for that location in the matrix

for i in range(pix.shape[0]):
    for j in range(pix.shape[1]):
        pix[i, j] = (pix[i, j] + key_image[i, j]) % 256

# Display the encrypted image.
ax3 = fig.add_subplot(223)
ax3.set_title('Encrypted Image', fontsize=9)
plt.imshow(pix, cmap='gray')

print(">>>> Image 2 is now being used to decrypt Image 1 <<<")
print('')
# Decryption
# =========== USE FOR LOOPS ================
# iterate over the size of the image/matrix
# for decryption the formula is (Value -Key) Modulo N
# use the corresponding value in key image as your key for that location in the matrix
for i in range(pix.shape[0]):
    for j in range(pix.shape[1]):
        pix[i, j] = (pix[i, j] - key_image[i, j]) % 256


end = time.time()
timeElapsed = end - start

print('Time elapsed %s seconds' % timeElapsed)

# to illustrate correct decryption, display the decrypted image
ax3 = fig.add_subplot(224)
ax3.set_title('Decrypted Image', fontsize=9)
plt.imshow(pix, cmap='gray')

fig.savefig('enc_dec_key_image2.png')
plt.show()



