import numpy as np
from scipy.integrate import odeint
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def system_generator(x, t, A, fac):
    dx_by_dt = A.dot(x)
    return dx_by_dt*fac


t_array = np.arange(0, 10, 1)
A = np.array([(0, 1, 0),
              (0, 0, 1),
              (1, -10, 0)])
x_initial = np.array([1, 1, 0])
t_0 = time.time()
x_trajectory = odeint(system_generator,
                      x_initial,
                      t_array,
                      args = (A, 1))
t_1 = time.time()
print("ODEINT TIME : ", t_1-t_0)

plt.plot(t_array, x_trajectory[:, 0],
         t_array, x_trajectory[:, 1],
         t_array, x_trajectory[:, 2])
plt.show()
