# This code is to be run in Python 2.7
# Displays video from a webcam for 10 seconds
# Basic code taken form OpenCV documentation
# and tutorials

import numpy as np
import cv2
import time

img = cv2.imread('capt.png',0)

while True:
    cv2.imshow('fig', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows
