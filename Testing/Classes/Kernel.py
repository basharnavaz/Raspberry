# Author: Basharnavaz Khan
# basharnavaz.khan@mail.mcgill.ca
#
# Python file to create a Kernel Class
# Pass parameters as an array [a_0, a_1, a_2]
# Latency: time difference between end of window and instant at which estimation is desired
# Set instance Variables: parameter, WindowLength, latency, TimePeriod
# Run the function Kernel.compute to compute the Double Sided Kernel
#
# The kernel is in the instance variable: KD
#
#
#
import numpy as np
import math


class Kernel(object):

    def __init__(self):
        self.parameter = np.zeros(3)
        self.WindowLength = 1.000
        self.latency = 0.100
        self.TimePeriod = 0.001

        self.a_0, self.a_1, self.a_2 = self.parameter
        self.A = np.zeros((3, 4))
        self.number_of_samples = 1001
        self.a = np.zeros((4, self.number_of_samples))
        self.t = np.zeros((self.number_of_samples, 3))
        self.KD = np.zeros(self.number_of_samples)
        self.LengthFactor = 1/(math.pow((self.WindowLength - self.latency), 3) + math.pow(self.latency, 3))

    def compute(self):
        if (self.WindowLength % self.TimePeriod) > 0.001:
            print("Warning: Window Length not a Multiple of Time Period")
            print("Numerical assumptions will be made \n")
            print(self.WindowLength % self.TimePeriod)

        if (self.latency % self.TimePeriod) > 0.001:
            print("Warning: Latency not a multiple of Time Period")
            print("Numerical assumptions will be made\n")
            print(self.latency % self.TimePeriod)

        self.a_0, self.a_1, self.a_2 = self.parameter
        self.A = np.array([(0, 0, 9, self.a_2),
                           (0, 18, 6*self.a_2, self.a_1),
                           (6, 6*self.a_2, 3*self.a_1, self.a_0)])
        self.number_of_samples = int(math.ceil(self.WindowLength/self.TimePeriod)) + 1
        self.a = np.zeros((4, self.number_of_samples))
        self.t = np.zeros((self.number_of_samples, 3))
        self.KD = np.zeros(self.number_of_samples)
        self.LengthFactor = 1 / (math.pow((self.WindowLength - self.latency), 3) + math.pow(self.latency, 3))
        for i in range(0, self.number_of_samples):
            if i < int(math.ceil(self.WindowLength - self.latency)/self.TimePeriod):
                self.a[(0, 1, 2, 3), i] = [1,
                                           -i*self.TimePeriod,
                                           math.pow((i*self.TimePeriod), 2),
                                           -math.pow((i*self.TimePeriod), 3)]
            else:
                self.a[(0, 1, 2, 3), i] = [1,
                                           i * self.TimePeriod,
                                           math.pow(((self.number_of_samples-i) * self.TimePeriod), 2),
                                           math.pow(((self.number_of_samples-i) * self.TimePeriod), 3)]
            self.t[i, (0, 1, 2)] = [1,
                                    (self.WindowLength - self.latency - (i*self.TimePeriod)),
                                    0.5*math.pow((self.WindowLength - self.latency - (i*self.TimePeriod)), 2)]
            self.KD[i] = (self.A.dot(self.a[(0, 1, 2, 3), i]).dot(self.t[i, (0, 1, 2)]))


'''
# Code to test Kernel Class
# Uncomment this block to run test
kern = Kernel()
kern.WindowLength = 5
kern.TimePeriod = 0.8
kern.latency = 1
kern.parameter = np.ones(3)
kern.compute()

print("A    : \n", kern.A, "\n\n\n")
print("a    : \n", kern.a, "\n\n\n")
print("t    : \n", kern.t, "\n\n\n")
print("KD_1 : \n", kern.KD_1, "\n\n\n")
print("KD   : \n", kern.KD, "\n\n\n")
'''
