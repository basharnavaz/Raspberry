import numpy as np
import math
import matplotlib.pyplot as plt
from Tkinter import *
import threading
import time
from pickle import dumps
import socket

def drill_simulation():
    global drill_status, hole_counter, Xdrill, Ydrill, D, W, pause_status
    global sim_termination, t_elap, message
    movement_case = 0  # 0 for simulated movement, 1 for controlled movement
    # ======
    # Parameters
    N_ref = 130  # Rotary speed set-point (RPM = rev/min)
    RN_set = 0.5  # penetration per rotation (inch/rev)
    RN_max = 0.6
    Pr_set = 2800  # Rotation pressure (psi)
    Pr_max = 3200
    Wmax = 3200
    Wmin = 0

    Vhaul = 10
    Vholeclean = 2
    proximity_measure = 0.1
    desired_depth = 1.5

    Ts = 1. / 400
    num_rad = np.array([0.02156, -0.00348, -0.009276, -0.007357])
    den_rad = np.array([1, -0.9237, -0.1182, -0.3697, 0.4134, 0, 0])

    num_fad = np.array([-0.07299, 0.1531, -0.00874, -0.0692, 0])
    den_fad = np.array([1, -1.766, 0.428, 0.6901, -0.3488])
    len_fad = np.size(den_fad) - 1
    W_hist = np.zeros((1, len_fad))
    Wcom_hist = np.zeros((1, len_fad))
    # == Rock type data
    # Each row contains A1, A2, A3, A4, (A5 = 0), A6, A7, respectively.
    Ageo = np.array([[0.001178, 0.9, 1.085, 2.35e-4, 0, 5.046, 0.791],  # Bankstone Fork Limestone
                     [0.029, 0.614, 1.028, 0.0058, 0, 11.756, 0.707],  # Anvil Rock Sandstone
                     [0.335, 0.5053, 0.6796, 0.067, 0, 16.418, 0.645],  # Lawson Shale
                     [0.49012, 0.4889, 0.6191, 0.098, 0, 14.525, 0.664],  # Sandy Shale
                     [0.0004696, 1.08, 0.982, 9.392e-5, 0, 6.098, 0.779]])  # Brereton Limestone
    rock_index = 9
    # Controller gains (page 116)

    # Tuned (page 151)
    # Kp_pr = 0.5 Ki_pr = 2.5 Kv_pr = 0
    # Kp_rn = 400 Ki_rn = 5000 Kv_rn = 100

    # My own tuning
    Kp_pr, Ki_pr, Kv_pr = 0.5, 2.5, 0
    Kp_rn, Ki_rn, Kv_rn = 10, 600, 10

    regulate_rn = 1
    no_filter_piv = 1

    eold = RN_set  # Assuming start at RN mode and RN(1) = 0
    uold = 0
    efold = 0
    yfold = 0
    K_depth = 0.5
    yold = 0
    u_windup = 0
    # =====
    # Hole sequence for each machine, one row for each machine
    drill_dimensions = np.array([[2], [4]])
    Planned_hole_seq = np.array([range(1, 21)]).T

    control_method = 2

    # Bench Definition
    Hole_location = np.array([[45, 59],
                              [45, 53],
                              [45, 47],
                              [45, 41],
                              [45, 35],
                              [45, 29],
                              [45, 23],
                              [45, 17],
                              [45, 11],
                              [45, 5],
                              [37, 59],
                              [37, 53],
                              [37, 47],
                              [37, 41],
                              [37, 35],
                              [37, 29],
                              [37, 23],
                              [37, 17],
                              [37, 11],
                              [37, 5]])

    first_hole = Planned_hole_seq[0]
    hole_counter = 0
    Xdrill = [Hole_location[hole_counter, 0]]
    Ydrill = [Hole_location[hole_counter, 1] + 1.0]

    tramming_counter = 1000  # means it will take 1000 sample times
    tramming_counter_init = 1000
    levelling_counter = 1200  # means it will take 1200 sample times
    levelling_counter_init = 1200

    drill_status = 'Moving'  # moving to the next hole status
    drill_status_number = 1
    sim_termination = False
    
    # Initialization
    W = [0.0]
    R = [0.0]
    RN = [0.0]
    Pdist = [0.0]
    Pr = [0.0]
    D = [0.0]

    y_k, yref_k = 0.0, 0.0
    Kp, Ki, Kv = 0.0, 0.0, 0.0
    t_previous = time.time()
    t_0 = time.time()
    s = 0.0
    while not sim_termination:
        if pause_status or (time.time()-t_previous < 0.0025):
            continue
        message = [drill_status_number, hole_counter+1, Xdrill[-1], Ydrill[-1], D[-1], W[-1], t_elap]
        # print message
        s = s + 0.0025
        t_elap = time.time() - t_0
        # print str(time.time()-t_previous)[0:8], str(t_elap)[0:8], s
        t_previous = time.time()
        if drill_status == 'Not Started':
            Xdrill.append(Xdrill[-1])
            Ydrill.append(Ydrill[-1])
            W.append(0.0)  # Feed pressure
            R.append(0.0)  # Penetration rate in feet / hour
            RN.append(0.0)  # Penetration per revolotion in inch per revolution
            Pdist.append(0.0)  # Disturbance pressure
            Pr.append(0.0)  # RotationPressure, Page 243
            D.append(0.0)  # Depth
            drill_status_number = 0
            
        elif drill_status == 'Moving':
            if movement_case == 0:
                theta = math.atan2(Hole_location[hole_counter, 1] - Ydrill[-1],
                                   Hole_location[hole_counter, 0] - Xdrill[-1])

                Xdrill.append(Xdrill[-1] + Vhaul * Ts * math.cos(theta))
                Ydrill.append(Ydrill[-1] + Vhaul * Ts * math.sin(theta))
    
            W.append(0.0)  # Feed pressure
            R.append(0.0)  # Penetration rate in feet / hour
            RN.append(0.0)  # Penetration per revolotion in inch per revolution
            Pdist.append(0.0)  # Disturbance pressure
            Pr.append(0.0)  # RotationPressure, Page 243
            D.append(0.0)  # Depth
            if np.linalg.norm(Hole_location[hole_counter, :] - [Xdrill[-1], Ydrill[-1]]) < proximity_measure:
                drill_status = 'Tramming'
                drill_status_number = 2
                tramming_counter = tramming_counter_init

        elif drill_status == 'Tramming':
            Xdrill.append(Hole_location[hole_counter, 0])
            Ydrill.append(Hole_location[hole_counter, 1])
            W.append(W[-1])  # Feed pressure
            R.append(R[-1])  # Penetration rate in feet / hour
            RN.append(RN[-1])  # Penetration per revolotion in inch per revolution
            Pdist.append(Pdist[-1])  # Disturbance pressure
            Pr.append(Pr[-1])  # RotationPressure, Page 243
            D.append(D[-1])  # Depth

            tramming_counter -= 1  # How many samples does it take
            if tramming_counter < 0:
                drill_status = 'Levelling'
                drill_status_number = 3
                levelling_counter = levelling_counter_init

        elif drill_status == 'Levelling':
            Xdrill.append(Xdrill[-1])
            Ydrill.append(Ydrill[-1])
            W.append(W[-1])  # Feed pressure
            R.append(R[-1])  # Penetration rate in feet / hour
            RN.append(RN[-1])  # Penetration per revolotion in inch per revolution
            Pdist.append(Pdist[-1])  # Disturbance pressure
            Pr.append(Pr[-1])  # RotationPressure, Page 243
            D.append(D[-1])  # Depth

            levelling_counter -= 1
            if levelling_counter < 0:
                drill_status = 'Drilling'
                drill_status_number = 4
                W_hist = np.zeros((1, len_fad))
                Wcom_hist = np.zeros((1, len_fad))
                eold = RN_set
                uold = 0
                efold = 0
                yfold = 0
                yold = 0
                u_windup = 0

        elif drill_status == 'Drilling':
            Xdrill.append(Xdrill[-1])
            Ydrill.append(Ydrill[-1])

            current_state = [W[-1], R[-1], RN[-1], Pdist[-1], Pr[-1], D[-1]]

            W_k = current_state[0]
            R_k = current_state[1]
            RN_k = current_state[2]
            Pdist_k = current_state[3]
            Pr_k = current_state[4]
            D_k = current_state[5]

            # One step ahead Simulation of Drill dynamics
            if control_method == 1:  # RN Control
                y_k, yref_k = RN_k, RN_set
                Kp, Ki, Kv = Kp_rn, Ki_rn, Kv_rn

            elif control_method == 2:  # Rotation Pressure Control
                y_k, yref_k = Pr_k, Pr_set
                Kp, Ki, Kv = Kp_pr, Ki_pr, Kv_pr

            elif control_method == 3:  # Switching control (RN + Rotation Pressure)
                if regulate_rn == 1:
                    y_k, yref_k = RN_k, RN_set
                    Kp, Ki, Kv = Kp_rn, Ki_rn, Kv_rn
                    if (float(RN_k) <= RN_max) and (Pr_k >= Pr_max):
                        regulate_rn = 0
                        eold = Pr_set - Pr_k
                        uold, efold, yfold = 0, 0, 0
                    else:
                        y_k = Pr_k
                        yref_k = Pr_set
                        Kp, Ki, Kv = Kp_pr, Ki_pr, Kv_pr
                        if float(RN_k) > RN_max:
                            regulate_rn = 1
                            eold = RN_set - RN_k
                            uold, efold, yfold = 0, 0, 0

            # PIV Control
            e_k = yref_k - y_k

            if no_filter_piv:
                ef_k = e_k
                yf_k = y_k
            else:
                ef_k = e_k - 0.5 * eold
                yf_k = -0.5 * yfold + (Kv / Ts) * y_k - (Kv / Ts) * yold

            ui_k = Ki * Ts * efold + uold + u_windup
            u_k = Kp * ef_k + ui_k

            eold = e_k
            uold = u_k
            efold = ef_k
            yfold = yf_k
            yold = y_k

            # Feed Pressure Command
            Win_k = u_k - yf_k
            if Win_k > Wmax:
                Wcom_k = Wmax
            elif Win_k > Wmin:
                Wcom_k = Win_k
            else:
                Wcom_k = Wmin
            u_windup = (Wcom_k - Win_k) * 0.1

            # ====================================
            # Drilling Dynamics
            if float(D_k) <= 0.3048:  # 1 ft
                rock_index = 1
            elif float(D_k) <= 0.6096:  # 2 ft
                rock_index = 4
            elif float(D_k) <= 0.9144:  # 3 ft
                rock_index = 2
            elif float(D_k) <= 1.2192:  # 4 ft
                rock_index = 3
            elif float(D_k) <= 1.524:  # 5 ft
                rock_index = 5

            A = Ageo[rock_index - 1, :]

            # =Rotary actuator dynamics, Input: N_com (constant or from the controller), Output: N
            N_kplus = N_ref - 1. * 0.005 * Pr_k

            # =Feed actuator dynamics, Input: Wcom (from controller), Output: W (feed pressure)
            W_hist[0: 4] = [W_k, W_hist[0, 0], W_hist[0, 1], W_hist[0, 2]]
            Wcom_hist[0: 4] = [Wcom_k, Wcom_hist[0, 0], Wcom_hist[0, 1], Wcom_hist[0, 2]]
            W_kplus = (np.dot(-den_fad[1:], W_hist.T) + np.dot(num_fad[1:], Wcom_hist.T))[0]

            # Penetration Rate
            R_kplus = A[0] * math.pow(W_kplus, float(A[1])) * math.pow(N_kplus, A[2])

            # Penetration per revolution
            RN_kplus = A[3] * math.pow(W_kplus, A[1]) * math.pow(N_kplus, (A[2] - 1))

            # Disturbance Pressure
            Pdist_kplus = A[5] * math.pow(W_kplus, A[6])

            # Rotation Pressure
            Pr_kplus = 325 + Pdist_kplus + 1.8443 * N_kplus  # Page 243

            # Drill bit depth
            D_kplus = D_k + K_depth * Ts * R_kplus * 8.46667/100000  # transform feet / hour to m / sec

            # ====

            W.append(W_kplus)  # Feed pressure
            R.append(R_kplus)  # Penetration rate in feet / hour
            RN.append(RN_kplus)  # Penetration per revolution in inch per revolution
            Pdist.append(Pdist_kplus)  # Disturbance pressure
            Pr.append(Pr_kplus)  # Rotation Pressure, Page 243
            D.append(D_kplus)  # Drill bit depth, transform feet / hour to m / sec

            if D[-1] > desired_depth:
                drill_status = 'Clearing'
                drill_status_number = 5

        elif drill_status == 'Clearing':
            Xdrill.append(Xdrill[-1])
            Ydrill.append(Ydrill[-1])
            W.append(0)  # Feed pressure
            R.append(0)  # Penetration rate in feet / hour
            RN.append(0)  # Penetration per revolotion in inch per revolution
            Pdist.append(0)  # Disturbance pressure
            Pr.append(0)  # Rotation Pressure, Page 243

            if D[-1] >= 0:
                D.append(D[-1] - Vholeclean * Ts)
            else:  # we need to move to the next hole, if any
                if hole_counter == np.shape(Planned_hole_seq)[0] - 1:
                    drill_status = 'Not Started'
                    drill_status_number = 0
                    sim_termination = 1
                else:
                    hole_counter = hole_counter + 1
                    drill_status = 'Moving'
                    drill_status_number = 1



def transmit():
    global sim_termination, message, pause_status
    ip = "192.168.1.185"
    port = 5005
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    
    while not sim_termination:
        if pause_status:
            continue
        sock.sendto(dumps(message), (ip, port))
    sock.sendto('Terminate', (ip, port))
    return
    


def gui_tick():
    global drill_status, hole_counter, Xdrill, Ydrill, D, W
    global root
    Label(root, text='Drill Status').grid(row=0, column=0)
    Label(root, text=drill_status).grid(row=1, column=0)
    Label(root, text='Hole Number').grid(row=0, column=1)
    Label(root, text=str(hole_counter)).grid(row=1, column=1)
    Label(root, text='X Pos').grid(row=0, column=2)
    Label(root, text=str(Xdrill)).grid(row=1, column=2)
    Label(root, text='Y Pos').grid(row=0, column=3)
    Label(root, text=str(Ydrill)).grid(row=1, column=3)
    Label(root, text='Depth').grid(row=0, column=4)
    Label(root, text=str(D)).grid(row=1, column=4)
    Label(root, text='Feed Pressure').grid(row=0, column=5)
    Label(root, text=str(W)).grid(row=1, column=5)
    gui_update()
    print "GUI ROot"
    root.mainloop()


def gui_update():
    label_drill_val['text'] = drill_status
    label_hole_val['text'] = str(hole_counter+1)
    label_x_pos_val['text'] = str(Xdrill[-1])
    label_y_pos_val['text'] = str(Ydrill[-1])
    label_depth_val['text'] = str(D[-1])[0:4]
    label_feed_val['text'] = str(W[-1])[0:5]
    label_time_val['text'] = str(t_elap)[0:5]
    label_drill_val.after(1000, gui_update)           # 100 is the display delay


def pause():
    global pause_status, button_pause
    pause_status = not pause_status
    if pause_status:
        button_pause['text'] = 'Resume Simulation'
    else:
        button_pause['text'] = 'Pause Simulation'

def end_sim():
    global sim_termination
    sim_termination = True
    button_end['text'] = 'Simulation Terminated'

if __name__ == '__main__':
    drill_status = ''
    hole_counter = 0
    Xdrill, Ydrill = [], []
    D, W = [], []
    pause_status, sim_termination = False, False
    sim_factor = 1.00
    message = np.zeros(7)

    t_elap = 0.0
    root = Tk()
    label_drill = Label(root, text='Drill Status', font=20)
    label_hole = Label(root, text='Hole', font=20)
    label_x_pos = Label(root, text='X', font=20)
    label_y_pos = Label(root, text='Y', font=20)
    label_depth = Label(root, text='Depth', font=20)
    label_feed = Label(root, text='Feed ', font=20)
    label_time = Label(root, text='Time ', font=20)

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

    button_pause = Button(root, text='Pause Simulation', command=pause, font=20)
    button_pause.grid(row=2, column = 0, columnspan=2)

    button_end = Button(root, text='End Simulation', command= end_sim, font=20)
    button_end.grid(row=2, column=5, columnspan=2)
    
    sim = threading.Thread(name='Drill Simulation', target=drill_simulation)
    sim.start()
    trans = threading.Thread(name='Socket', target=transmit)
    trans.start()
    gui_update()
    root.mainloop()

