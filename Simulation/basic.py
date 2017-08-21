# Send data over socket
# data is of a simple linear state space system
# simulation runs for 10 seconds and sends the x coordinates and
# the y coordinate along with the time
# Plots graphs after teh simulation runs
# The matrices are taken from the c2d function in MATLAB
# Run this code on RPi


import numpy as np
import matplotlib.pyplot as plt
import socket
import time
from pickle import loads, dumps

UDP_IP = "192.168.1.185"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)

end_time = 10
sim_frequency = 1000
sampling_frequency = 60

if sim_frequency % sampling_frequency != 0:
    print "######################## WARNING ########################"
    print "Simulation Frequency not a Multiple of Sampling Frequency"
    print "Numerical assumptions will be made"
    print "######################## WARNING ########################"

factor = int(sim_frequency/sampling_frequency)
sim_time = 1./sim_frequency   # Simulation Time Period
sample_time = 1./sampling_frequency   # Sampling Time Period
n_sim = end_time*sim_frequency + 1
n_sampling = end_time*sampling_frequency + 1


A = np.array([(1.997992008668995, -0.998001998667333), (1, 0)])
B = np.array([0.0625, 0])
C = np.array([(0.015991978684004, -0.015975994686662)])
D = np.array([0])
u = 1
x = np.array([0, 0])
x_trajectory_sim = np.zeros((2, n_sim))
y_trajectory_sim = np.zeros((1, n_sim))
t_array_sim = np.linspace(0, end_time, n_sim)
t_array_sample = np.linspace(0, end_time, n_sampling)
x_trajectory_sample = np.zeros((2, int(n_sampling)))
y_trajectory_sample = np.zeros(int(n_sampling))
k = 0

for i in range(0, 10):
    sock.sendto("Sample Frequency: " + str(sampling_frequency), (UDP_IP, UDP_PORT))
    time.sleep(0.05)
t_0 = time.time()
for i in range(0, n_sim):
    x = A.dot(x) + B
    y = C.dot(x)
    x_trajectory_sim[:, i] = x
    y_trajectory_sim[:, i] = y
    if abs(t_array_sim[i] - t_array_sample[k]) < sim_time:
        x_trajectory_sample[:, k] = x
        y_trajectory_sample[k] = y
        t_array_sample[k] = t_array_sim[i]
        vector = np.array([t_array_sim[i], x_trajectory_sample[0, k],
                           x_trajectory_sample[1, k], y_trajectory_sample[k]])
        sock.sendto(dumps(vector), (UDP_IP, UDP_PORT))
        time.sleep(sample_time)
        k = k + 1
        if k >= n_sampling:
            break

for i in range(0, 10):
    sock.sendto("Terminate", (UDP_IP, UDP_PORT))
    time.sleep(0.05)

sock.close()


# Plotting
plt.subplot(3, 1, 1)
plt.plot(t_array_sim, x_trajectory_sim[0, :], t_array_sample, x_trajectory_sample[0, :])

plt.subplot(3, 1, 2)
plt.plot(t_array_sim, x_trajectory_sim[1, :], t_array_sample, x_trajectory_sample[1, :])

plt.subplot(3, 1, 3)
plt.plot(t_array_sim, y_trajectory_sim[0, :], t_array_sample, y_trajectory_sample)

plt.show()
