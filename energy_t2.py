import win32com.client
import dso
import operator
import tools
import matplotlib.pyplot as plt
import threading
import time
import numpy as np

i = 0
wave_test = []
energy = []
amp = []
energy1 = []
amp1 = []
waveloop = []
wave1 = []
para_0 = {'SEQ': 'ON', 'SEQ_N': 10, 'polarity': 'negative'}
dos_0 = dso.Dso(para_0)

def loop_e_t1():
    while 1:
        global dos_0
        global wave1
        global waveloop
        if len(waveloop) < 20:
            waveform0 = dos_0.get_wave_1()
        if operator.eq(wave1, waveform0['c1'][1]) == False:
            # print(len(self.waveloop))
            if len(waveloop) < 20:
                waveloop.append(waveform0)
        wave1 = waveform0['c1'][1]

def loop_e_t2():
    global energy
    global amp
    global energy1
    global amp1
    global waveloop
    global para_0
    # plt.ion()
    # plt.figure(1)
    f = open("energy_1030c3_1.txt", "a")
    k = 0
    while k < 100000:
        if len(waveloop) > 0:
            if para_0['SEQ'] == 'ON':
                for i in range(0, para_0['SEQ_N']):
                    # c1
                    t1 = tools.Wavetools(waveloop[0]['c1'][0][i], waveloop[0]['c1'][1][i])
                    e_1 = t1.get_energy(0.2)
                    amp_1 = t1.get_amplitude()

                    # c2
                    # t2 = tools.Wavetools(waveloop[0]['c2'][0][i], waveloop[0]['c2'][1][i])
                    # e_2 = t2.get_energy(0.2)
                    # amp_2 = t2.get_amplitude()

                    energy.append(e_1)
                    amp.append(amp_1)
                    # energy1.append(e_2)
                    # amp1.append(amp_2)
                    f.write(str(e_1) + ' ' + str(amp_1) + '\n')
                    k = k + 1
                    if k % 200 == 0:
                        print(k)
                        # plt.clf()
                        # plt.hist(energy, 100, range=(0, 15))
                        # plt.pause(0.001)
                waveloop.pop(0)
    # for m in range(0, len(energy)):
        # f.write(str(energy[m]) + ' ' + str(amp[m]) + ' ' + str(energy1[m]) + ' ' + str(amp1[m]) + '\n')
        # f.write(str(energy[m]) + ' ' + str(amp[m]) + '\n')
    print(len(energy))

th3 = threading.Thread(target=loop_e_t1)
th3.start()
th4 = threading.Thread(target=loop_e_t2)
th4.start()