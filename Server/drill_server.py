import socket
import time
from pickle import loads
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
            vector = loads(data)
        except:
            print 'Error'


def gui_update():
    global vector
    label_drill_val['text'] = str(drill_status_names[int(vector[0])])
    label_hole_val['text'] = str(vector[1])
    label_x_pos_val['text'] = str(vector[2])
    label_y_pos_val['text'] = str(vector[3])
    label_depth_val['text'] = str(vector[4])[0:4]
    label_feed_val['text'] = str(vector[5])[0:5]
    label_time_val['text'] = str(vector[6])[0:4]
    label_drill_val.after(100, gui_update)


if __name__ == '__main__':
    vector = np.zeros(7)
    receive = threading.Thread(name='Socket', target=transmission)
    receive.start()

    drill_status_names = ['Not Started,', 'Moving', 'Tramming', 'Levelling', 'Drilling', 'Clearing']
    root = Tk()
    label_drill = Label(root, text='Drill Status', font=20)
    label_hole = Label(root, text='Hole Number', font=20)
    label_x_pos = Label(root, text='X Pos', font=20)
    label_y_pos = Label(root, text='Y Pos', font=20)
    label_depth = Label(root, text='Depth', font=20)
    label_feed = Label(root, text='Feed Pressure', font=20)
    label_time = Label(root, text='Time Elapsed', font=20)

    label_drill.grid(row=0, column=0)
    label_hole.grid(row=0, column=1)
    label_x_pos.grid(row=0, column=2)
    label_y_pos.grid(row=0, column=3)
    label_depth.grid(row=0, column=4)
    label_feed.grid(row=0, column=5)
    label_time.grid(row=0, column=6)

    label_drill_val = Label(root, font=20)
    label_hole_val = Label(root, font=20)
    label_x_pos_val = Label(root, font=20)
    label_y_pos_val = Label(root, font=20)
    label_depth_val = Label(root, font=20)
    label_feed_val = Label(root, font=20)
    label_time_val = Label(root, font=20)

    label_drill_val.grid(row=1, column=0)
    label_hole_val.grid(row=1, column=1)
    label_x_pos_val.grid(row=1, column=2)
    label_y_pos_val.grid(row=1, column=3)
    label_depth_val.grid(row=1, column=4)
    label_feed_val.grid(row=1, column=5)
    label_time_val.grid(row=1, column=6)

    gui_update()
    root.mainloop()
