from Tkinter import *
import Tkinter as tk
import ttk
# from ttk import *

import tkFont


# font  as tkfont # python 3
# import Tkinter as tk     # python 2
# import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        # container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid()
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, tab1, Calibration, Levelling, Diagnostics, Review):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("tab1")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid()
        self.button = Button(self,
                             text="HOME", bg="gainsboro", command=lambda: controller.show_frame("PageOne"))

        self.button.grid(row=6, column=1, sticky=E + W)

        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button2.grid()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page Page One", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid()
        button_list = []
        list_text_pages = ['StartPage', 'PageOne', 'PageTwo', 'tab1', 'Calibration', 'Levelling', 'Diagnostics',
                           'Review']
        button_names_list = ['Home', 'Session Information', 'Drilling', 'Status', 'Calibration', 'Levelling',
                             'Diagnostics', 'Review']

        for i in xrange(8):
            button_list.append(tk.Button(self, text=str(button_names_list[i]),
                                         command=lambda: controller.show_frame(list_text_pages[4])))
            button_list[i].grid(row=6, column=i)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.grid()
        # label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Go to the Status page",
                            command=lambda: controller.show_frame("tab1"))
        button1.grid()
        button2.grid()


class Calibration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Calibration Page", font=controller.title_font)
        label.grid()
        # label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Go to the Status page",
                            command=lambda: controller.show_frame("tab1"))
        button1.grid()
        button2.grid()


class Levelling(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Levelling Page", font=controller.title_font)
        label.grid()
        # label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Go to the Status page",
                            command=lambda: controller.show_frame("tab1"))
        button1.grid()
        button2.grid()


class Diagnostics(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Diagnostics", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid()
        button1 = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Go to Status page",
                            command=lambda: controller.show_frame("tab1"))
        button1.grid()
        button2.grid()


class Review(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Review", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid()
        button1 = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Go to Status page",
                            command=lambda: controller.show_frame("tab1"))
        button1.grid()
        button2.grid()


class tab1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid()

        # frame 1 holds status label
        Frame1 = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=1)
        Frame1.grid(row=0, column=0, rowspan=1, columnspan=5, sticky=W + E + N + S)
        # label for drilling stage
        self.label = Label(Frame1,
                           text="Hole selection -> NAVIGATION/Leveling -> COLLARING -> Drilling -> Bit Retraction -> Dust Collection",
                           relief=RAISED)
        # Consider using individual labels, so you can highlight each stage as they occur
        self.label.grid()
        # self.label.grid_propagate(0) #want to fit to frame size

        Frame2 = Frame(self, bg="blue")
        Frame2.grid(row=1, column=0, sticky=W + E)
        self.button = Button(Frame2,
                             text=" 1 ", bg="gainsboro", fg="black")
        self.button.grid(row=3, column=0, sticky=E + W)
        self.button = Button(Frame2,
                             text=" 2 ", bg="gainsboro", fg="black")
        self.button.grid(row=4, column=0, sticky=E + W)
        self.button = Button(Frame2,
                             text=" 3 ", bg="gainsboro", fg="black")
        self.button.grid(row=5, column=0, sticky=E + W)

        self.button = Button(Frame2,
                             text=" 4 ", bg="gainsboro", fg="black")
        self.button.grid(row=6, column=0, sticky=E + W)
        self.button = Button(Frame2,
                             text=" 5 ", bg="gainsboro", fg="black")
        self.button.grid(row=7, column=0, sticky=E + W)
        self.button = Button(Frame2,
                             text=" MAP ", bg="gainsboro", fg="black")
        self.button.grid(row=8, column=0, sticky=E + W)

        # self.button.grid_propagate(0)

        Frame3 = Frame(self, bg="white")
        Frame3.grid(row=1, column=1, columnspan=4, sticky=W + E + N + S)

        self.button = Button(Frame3,
                             text="CONTROL ENABLE OFF", bg="white")
        # command=self.write_slogan)
        self.button.grid(row=2, column=1, sticky=E + W)

        self.button = Button(Frame3,
                             text="BRAKE RELEASED", bg="white")
        # command=self.write_slogan)
        self.button.grid(row=2, column=2, sticky=E + W)
        self.button = Button(Frame3,
                             text="MAIN MOTOR OFF", bg="white")
        # command=self.write_slogan)
        self.button.grid(row=2, column=3, sticky=E + W)

        mpb = ttk.Progressbar(Frame3, orient="vertical", length=50, mode="determinate")
        mpb.grid(row=3, column=0)
        mpb["maximum"] = 100
        mpb["value"] = 60  # write method for determining value
        # print "%s%%" % int(float(self.bytes) / float(self.maxbytes) * 100)

        self.label = Label(Frame3,
                           text="FORCE ON DRILL BIT (IN KN)")
        self.label.grid(row=3, column=1)
        self.label.config(font=("Courier", 7))

        self.label = Label(Frame3,
                           text="FORCE ON DRILL BIT (IN KN)")
        self.label.grid(row=3, column=1)
        self.label.config(font=("Courier", 7))

        Frame5 = Frame(self, bg="gainsboro")
        Frame5.grid(row=0, column=5, rowspan=4, sticky=W + E)

        mpb = ttk.Progressbar(Frame5, orient="vertical", length=50, mode="determinate")
        mpb.grid(row=0, sticky=W)
        mpb["maximum"] = 100
        mpb["value"] = 80  # write method for determining value

        mpb = ttk.Progressbar(Frame5, orient="vertical", length=50, mode="determinate")
        mpb.grid(row=1, sticky=W)
        mpb["maximum"] = 100
        mpb["value"] = 60  # write method for determining value

        mpb = ttk.Progressbar(Frame5, orient="vertical", length=50, mode="determinate")
        mpb.grid(row=2, sticky=W)
        mpb["maximum"] = 100
        mpb["value"] = 60  # write method for determining value
        self.label = Label(Frame5,
                           text="DRILLING DEPTH")

        self.label.grid(row=0, column=1, sticky=W)
        w = Entry(Frame5, bg="white", width=5)  # include command that updates value
        w.grid(row=0, column=2)

        self.label = Label(Frame5,
                           text="TORQUE")
        self.label.grid(row=1, column=1, sticky=W)
        w = Entry(Frame5, bg="white", width=5)  # include command that updates value
        w.grid(row=1, column=2)

        self.label = Label(Frame5,
                           text="BAILING AIR PRESSURE")
        self.label.grid(row=2, column=1, sticky=W)
        w = Entry(Frame5, bg="white", width=5)  # include command that updates value
        w.grid(row=2, column=2)

        Frame6 = Frame(self, bg="gainsboro")
        Frame6.grid(row=2, column=5, rowspan=4, sticky=N + W + E)
        self.label = Label(Frame6,
                           text="Remote Transmitter On")
        self.label.grid(row=0, column=0, sticky=W)

        self.label = Label(Frame6,
                           text="Jacks Retracted")
        self.label.grid(row=1, column=0, sticky=W)

        self.label = Label(Frame6,
                           text="Hole Clogged")
        self.label.grid(row=2, column=0, sticky=W)

        self.label = Label(Frame6,
                           text="Water Level")
        self.label.grid(row=3, column=0, sticky=W)

        # Buttons for the different tabs
        self.button_list = []
        self.list_text_pages = ['StartPage', 'PageOne', 'PageTwo', 'tab1',
                                'Calibration', 'Levelling', 'Diagnostics', 'Review']
        self.button_names_list = ['Home', 'Session Information', 'Drilling', 'Status',
                                  'Calibration', 'Levelling', 'Diagnostics', 'Review']

        for i in range(6):
            self.button_list.append(tk.Button(self, text=str(self.button_names_list[i])))
            self.button_list[i].grid(row=6, column=i)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()