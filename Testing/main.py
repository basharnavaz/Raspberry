# Author: Basharnavaz Khan
# basharnavaz.khan@mail.mcgill.ca
#
# This is the main code for estimation
# The main aim of this code is for Real Time Estimation
# It has a dependency on the class Kernel and the noisy input data computed in MATLAB
#
# IN THIS VERSION: Removed dependency on text file for y_noisy
#                  Function system_generator which works with scipy.integrate.odeint()
#                  to give system trajectories.
#                  Noise was added using numpy.random.normal() which requires stddev of noise
#                  stddev(noise) was calculated using SNR = mean(signal)/stddev(noise)
#
# The current version is buggy.
# The estimation is dependent on the latency of the kernel to be computed.
# It has been found that the code works well if the latency is set to zero.
# With an increasing latency, the estimate increases(magnifies) and also
# a visible phase shift.
#
# Future work would include to determine the cause of this drift and develop
# an approximation on the factor of magnification.
#
# Refer to the author's research notes while reviewing this code as
# it contains several insights into the computation code
#
# The viewer is advised to tinker with the values of latency and if the reason
# of the bug is found out then please contact the author
#
# The total run time on the author's machine was found out to be 0.124 seconds


import numpy as np
from Classes.Kernel import Kernel
import time
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Time instant to find total run time
t_0 = time.time()


# Function to evaluate system trajectories
def system_generator(x, t, system_A, fac):
    dx_by_dt = system_A.dot(x) * fac
    return dx_by_dt


# Initialize Kernel and set Kernel variables
kern = Kernel()
kern.parameter = np.array([-1, 10, 0])
kern.WindowLength = 0.5
kern.TimePeriod = 0.001
kern.latency = 0*kern.WindowLength
print("Kernel Initialized")
print("Parameters", kern.parameter,  "  WindowLength:", kern.WindowLength,
      "  TimePeriod:", kern.TimePeriod,  "  Latency:", kern.latency)

# Compute Kernel
kern.compute()
print("Kernel Computed")

SNR = 10
system_A = np.array([(0, 1, 0),
                     (0, 0, 1),
                     (1, -10, 0)])
# Enter Initial Condition of system here and take first component of system trajectory as done in Kumar's work
x_initial = np.array([1, 1, 0])
t_array = np.arange(0, 10, kern.TimePeriod)
time_instant_in_window = int((kern.WindowLength - kern.latency)/kern.TimePeriod)   # Refer to author's notes
x_trajectory = odeint(system_generator, x_initial, t_array, args=(system_A, 1))
y_trajectory = x_trajectory[:, 2]

y_measured = y_trajectory + np.random.normal(0, abs(y_trajectory).max()/SNR, np.size(y_trajectory))
y_estimated = np.zeros(np.size(y_measured))
y_window = np.zeros(kern.number_of_samples)


for window_start_position in range(0, np.size(y_measured) - kern.number_of_samples + 1):
    y_window = y_measured[window_start_position:(window_start_position + kern.number_of_samples)]
    y_m_integrand = np.multiply(kern.KD, y_window)
    area = np.trapz(y_m_integrand, dx=kern.TimePeriod)
    y_estimated[window_start_position + time_instant_in_window] = area*kern.LengthFactor

t_1 = time.time()
print("Total Run time : ", t_1 - t_0)
print("  LengthFactor : ", kern.LengthFactor)
plt.plot(t_array, y_measured, t_array, y_estimated)
plt.show()

