import socket
import time
UDP_IP = "192.168.1.185"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
t_0 = time.time()
while time.time() - t_0 <10.0:
    sock.sendto("Success??", (UDP_IP, UDP_PORT))
    print sock.recv(1024)
    time.sleep(0.5)

print "End of program!"
