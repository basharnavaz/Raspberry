import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Read when the image is in default 640x320 frame
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite('capt_640_gray.png', gray)
cv2.imwrite('capt_640_colo.png', frame)

# Set camera frame size to 320x240 and capture image
ret = cap.set(3,320)
ret = cap.set(4,240)
ret, frame = cap.read()
# Change colour to gray and save image
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite('capt_320_gray.png', gray)
cv2.imwrite('capt_320_colo.png',frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
