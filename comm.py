# This code is to be run in Python 2.7
# Displays video from a webcam for 10 seconds
# Basic code taken form OpenCV documentation
# and tutorials

import numpy as np
import cv2
import time
import socket
from cPickle import dumps

UDP_IP = "192.168.1.171"
UDP_PORT = 5005
cap = cv2.VideoCapture(0)
start = time.time()
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while(time.time()-start<10.0):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Display the resulting frame
    cv2.imshow('frame',gray)
    

    # Send data
    sock.sendto(dumps(gray), (UDP_IP, UDP_PORT))
#    for i in range(0, 480):
#        for j in range(0,640):
#            msg = str(1) + str(i).zfill(3) + str(j).zfill(3) + str(1) + str(gray[i,j]).zfill(3)
#            sock.sendto(msg, (UDP_IP, UDP_PORT))

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
