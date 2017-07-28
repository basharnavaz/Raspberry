from Tkinter import *
import time


def tick():
    s = time.strftime('%H:%M:%S')
    if s != clock["text"]:
        clock["text"] = s
    clock.after(100, tick)


if __name__ == '__main__':
    root = Tk()
    clock = Label(root, font=('helvetica', 20, 'bold'))
    clock2 = Label(root, text='sdfrf', font=('times', 20, 'bold'))
    clock.grid(row=0, column=0)
    clock2.grid(row=1, column=0)
    t_0 = time.time()

    tick()
    root.mainloop()
