# Basic communication to send message
# via UDP to server


import socket
import time
import numpy as np
from scipy.integrate import odeint
import math
from pickle import dumps, loads

UDP_IP = "192.168.1.185"
UDP_PORT = 5005
t_0 = time.time()
n = 100
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

A = np.array([(1.0, 0.001, 0), (0, 1, 0.001), (0.001, -0.001, 1)])
B = np.array([0, 0, 0.001])
x = np.array([1, 1, 0])
u = np.array([0, 0, 0])



while (time.time()-t_0<10):
        #print time.time()-t_0
    for j in range(0, 100):
        x = A.dot(x) + B.dot(u)
        

    message = 10
    if ((time.time() - t_0) %2)<0.1:
        i = math.ceil(time.time() - t_0)
        sock.sendto("##################START###############", (UDP_IP, UDP_PORT))
        sock.sendto(message, (UDP_IP, UDP_PORT))
        sock.sendto("##################STOP###############", (UDP_IP, UDP_PORT))
        #print("##################START###############")
        #print(message)
        #print("##################STOP###############")
	time.sleep(0.02)
sock.close()
