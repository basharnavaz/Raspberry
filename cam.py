# This code is to be run in Python 2.7
# Displays video from a webcam for 10 seconds
# Basic code taken form OpenCV documentation
# and tutorials

import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
start = time.time()


while(time.time()-start<10.0):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print gray

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#    time.sleep(1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
