# Basic communication to send message
# via UDP to server


import socket
import time

UDP_IP = "192.168.1.171"
UDP_PORT = 5005
MESSAGE = "01234567890"
start = time.time()

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while (time.time()-start<10):
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	time.sleep(0.5)

sock.close()
