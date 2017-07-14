# Author: Basharnavaz Khan
# mail: basharnavaz.khan@mail.mcgill.ca
#
# Code to receive data from 2 Raspberry Pis and plot
# data received in previous five seconds
# When porting code pay attention to the IP address of the server
#




import socket
import time
from pickle import loads
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# IP address of Server and variables to store
# addresses of the nodes
UDP_IP = "192.168.1.185"
UDP_PORT = 5005
address_1 = ('', 0)
address_2 = ('', 0)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
start = time.time()


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x_node_1 = np.array([[0], [0], [0], [0], [0]])
x_node_2 = np.array([[0], [6300], [6300], [0], [0]])
sampling_frequency_1 = 0
sampling_frequency_2 = 0
sample_time_1 = 0.0
sample_time_2 = 0.0
sample_1_set = False
sample_2_set = False
simulation = False    # Flag to check whether simulation is running
miss_1 = 0
miss_2 = 0
x_rec_p_n1 = x_node_1  # Previous received values from node 1
x_rec_p_n2 = x_node_2


def animate(i):
    global x_node_1, x_node_2, sampling_frequency_1, sampling_frequency_2, sample_time_1, sample_time_2
    global miss_1, miss_2, start, x_rec_p_n1, x_rec_p_n2, address_1, address_2, sample_1_set
    global sample_2_set, simulation
    # send Instruction to begin simulation
    if sample_1_set and sample_2_set and not simulation:
        time.sleep(0.2)
        sock.sendto("Begin", address_1)
        sock.sendto("Begin", address_2)
        simulation = True  # Simulation has started is now running

    data, addr = sock.recvfrom(512)  # buffer size is 1024 bytes

    try:
        x_received = loads(data)
        x_received = np.array([[x_received[0], x_received[1], x_received[2],
                                x_received[3], x_received[4]]])
        # Node 1
        if x_received[0, 4] == 1:
            # Check for missing samples
            if x_received[0, 0] - x_rec_p_n1[0, 0] > 1.5 * sample_time_1:
                miss_1 = miss_1 + (x_received[0, 0] - x_rec_p_n1[0, 0]) / sample_time_1 - 1
                print "Miss from Node 1:  ", miss_1, "  at:  ", x_received[0, 0], x_rec_p_n1[0, 0]

            x_rec_p_n1 = x_received
            x_node_1 = np.concatenate((x_node_1, x_received.T), axis=1)

            # Slice array if too long to plot
            if np.shape(x_node_1)[1] > int(round(5. / sample_time_1)):
                x_node_1 = x_node_1[:, -int(round(5. / sample_time_1)):]

        # Node 2
        if x_received[0, 4] == 2:
            # Check for missing samples
            if x_received[0, 0] - x_rec_p_n2[0, 0] > 1.5 * sample_time_2:
                miss_2 = miss_2 + (x_received[0, 0] - x_rec_p_n2[0, 0]) / sample_time_2 - 1
                print "Miss from Node 1:  ", miss_2, "  at:  ", x_received[0, 0], x_rec_p_n2[0, 0]

            x_rec_p_n2 = x_received
            x_node_2 = np.concatenate((x_node_2, x_received.T), axis=1)

            # Slice array if too long to plot
            if np.shape(x_node_2)[1] > int(round(5. / sample_time_2)):
                x_node_2 = x_node_2[:, -int(round(5. / sample_time_2)):]

        ax.clear()
        ax.plot(x_node_1[0, :], x_node_1[1, :], x_node_2[0, :], x_node_2[1, :])
        ax.set_ylim([-2700, 9200])

    except:
        if data == "Terminate":
            print "End of Transmission"
            print "Number of Misses; Node 1:", miss_1, ",  Node 2:", miss_2

        elif data[0:18] == "Sample Frequency 1":
            sampling_frequency_1 = int(data[20:])
            sample_time_1 = 1./sampling_frequency_1
            address_1 = addr
            sample_1_set = True
            print "Sample Freq, Time of Node 1: ", sampling_frequency_1, sample_time_1

        elif data[0:18] == "Sample Frequency 2":
            sampling_frequency_2 = int(data[20:])
            sample_time_2 = 1./sampling_frequency_2
            address_2 = addr
            sample_2_set = True
            print "Sample Freq, Time of Node 2: ", sampling_frequency_2, sample_time_2

        else:
            print "#############"
            print "Unknown Error"
            print "#############"

        ax.clear()
        ax.plot(x_node_1[0, :], x_node_1[1, :], x_node_2[0, :], x_node_2[1, :])
        ax.set_ylim([-2700, 9200])


ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
sock.close()

