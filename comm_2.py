import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.171',8089))
while True:
    ret,frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    data = pickle.dumps(gray) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data)

