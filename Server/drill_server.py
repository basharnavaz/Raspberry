import socket
import time
import pickle
from Tkinter import *
import threading
import numpy as np


def transmission():
    global vector
    ip = '192.168.1.185'
    port = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    t_0 = time.time()

    while time.time() - t_0 < 100:
        data, addr = sock.recvfrom(512)
        try:
            vector = pickle.loads(data)
        except pickle.UnpicklingError:
            print 'Error: ', data


def gui_update():
    global vector
    label_vals[0]['text'] = str(drill_status_names[int(vector[0])])
    for k in xrange(1, 7):
        label_vals[k]['text'] = str(vector[k])[0:5]
    label_vals[0].after(100, gui_update)


if __name__ == '__main__':
    vector = np.zeros(7)
    receive = threading.Thread(name='Socket', target=transmission)
    receive.start()

    drill_status_names = ['Not Started,', 'Moving', 'Tramming', 'Levelling', 'Drilling', 'Clearing']
    names = ['Drill Status', 'Hole Number', 'X Pos', 'Y Pos', 'Depth', 'Feed Pressure', 'Time Elapsed']
    root = Tk()
    label_names = []
    label_vals = []
    for i in xrange(7):
        label_names.append(Label(root, text=names[i], font=20))
        label_vals.append(Label(root, font=20))

        label_names[i].grid(row=0, column=i)
        label_vals[i].grid(row=1, column=i)

    gui_update()
    root.mainloop()
