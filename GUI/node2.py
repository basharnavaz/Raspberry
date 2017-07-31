import numpy as np
import matplotlib.pyplot as plt
import socket
import time
from pickle import loads, dumps
from Tkinter import *
import threading


UDP_IP = "192.168.1.185"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def transmission():
    start_time = 0  # in seconds
    duration = 4   # in seconds
    sim_frequency = 1000
    sampling_frequency = 10

    if sim_frequency % sampling_frequency != 0:
        print "######################## WARNING ########################"
        print "Simulation Frequency not a Multiple of Sampling Frequency"
        print "Numerical assumptions will be made"
        print "######################## WARNING ########################"

    factor = int(sim_frequency/sampling_frequency)
    sim_time = 1./sim_frequency   # Simulation Time Period
    sample_time = 1./sampling_frequency   # Sampling Time Period
    n_sim = duration*sim_frequency + 1
    n_sampling = duration*sampling_frequency + 1


    A = np.array([(1.997992008668995, -0.998001998667333), (1, 0)])
    B = np.array([0.0625, 0])
    C = np.array([(0.015991978684004, -0.015975994686662)])
    D = np.array([0])
    u = 0
    global x, y
    x = np.array([6300.0, 6300.0])
    y = 0

    global x_trajectory_sim, y_trajectory_sim, t_array_sim
    global t_array_sample, x_trajectory_sample, y_trajectory_sample
    global end_transmission
    
    x_trajectory_sim = np.zeros((2, n_sim))
    y_trajectory_sim = np.zeros((1, n_sim))
    t_array_sim = np.linspace(start_time, start_time + duration, n_sim)
    t_array_sample = np.linspace(start_time, start_time + duration, n_sampling)
    x_trajectory_sample = np.zeros((2, int(n_sampling)))
    y_trajectory_sample = np.zeros(int(n_sampling))
    k = 0


    global UDP_IP, UDP_PORT, sock
#    global start_time, duration, sim_frequency, sampling_frequency, factor
#    global sim_time, sample_time, n_sim, n_sampling
#    global A, B, C, D, u, x, x_trajectory_sim, y_trajectory_sim, t_array_sim
#    global t_array_sample, x_trajectory_sample, y_trajectory_sample, k

    
    for i in range(0, 3):
        sock.sendto("Sample Frequency 2: " + str(sampling_frequency), (UDP_IP, UDP_PORT))
        time.sleep(0.05)
    i = 0
    t_0 = time.time()
    global count
    count = 0
    
    while True:
        if (time.time() - t_0 - 0.1) - t_array_sim[i]  > 0.000:
            x = A.dot(x) + B*u
            y = C.dot(x)
            
            x_trajectory_sim[:, i] = x
            y_trajectory_sim[:, i] = y
            if abs(t_array_sim[i] - t_array_sample[k]) < sim_time:
                x_trajectory_sample[:, k] = x
                y_trajectory_sample[k] = y
                t_array_sample[k] = t_array_sim[i]
                vector = np.array([t_array_sim[i], x_trajectory_sample[0, k],
                                   x_trajectory_sample[1, k], y_trajectory_sample[k], 2])
                sock.sendto(dumps(vector), (UDP_IP, UDP_PORT))
                time.sleep(0.00001)
                k += 1
            
                if k >= n_sampling:  # Reset parameters
                    t_s = time.time()
                    count += 1
                    if count >= 2:
                        break
                    i = -1
                    k = 0
                    u = 1 - u
                    x_trajectory_sim = np.zeros((2, n_sim))
                    y_trajectory_sim = np.zeros((1, n_sim))
                    start_time = start_time + duration
                    t_array_sim = np.linspace(start_time, start_time + duration, n_sim)
                    t_array_sample = np.linspace(start_time, start_time + duration, n_sampling)
                    x_trajectory_sample = np.zeros((2, int(n_sampling)))
                    y_trajectory_sample = np.zeros(int(n_sampling))
                    t_0 = t_0 - (time.time()-t_s)
                
            i = i + 1

    for i in range(0, 3):
        sock.sendto("Terminate", (UDP_IP, UDP_PORT))
        endtransmission = True
        time.sleep(0.05)
    # plotting()



def plotting():
    plt.subplot(3, 1, 1)
    plt.plot(t_array_sim, x_trajectory_sim[0, :], t_array_sample, x_trajectory_sample[0, :])
                
    plt.subplot(3, 1, 2)
    plt.plot(t_array_sim, x_trajectory_sim[1, :], t_array_sample, x_trajectory_sample[1, :])

    plt.subplot(3, 1, 3)
    plt.plot(t_array_sim, y_trajectory_sim[0, :], t_array_sample, y_trajectory_sample)

    plt.show()



transmit = threading.Thread(name='Transmit',
                            target=transmission)
transmit.start()

root = Tk()

root.minsize(width=320, height=240)
x_gui = Label(root, font=('helvetica', 20, 'bold'))
x_gui.pack(fill=BOTH, expand=1)

def tick():
    s = str(y)
    x_gui['text'] = s
    x_gui.after(500, tick)

tick()
root.mainloop()
