import win32com.client
import dso
import operator
import tools
import matplotlib.pyplot as plt
import threading
import numpy as np

# dso = win32com.client.Dispatch('LeCroy.ActiveDSOCtrl.1')
# dso.MakeConnection("IP:211.86.148.140")
# i = 0
# wave_test = []
# energy = []
# amp = []
# energy1 = []
# amp1 = []
# para_0 = {'SEQ': 'ON', 'SEQ_N': 200, 'polarity': '1'}
# dos_0 = dso.Dso(para_0)
# plt.ion()
# plt.figure(1)
# f = open("energy_2.txt", "a")
# print(i)
# f2 = open('qwe.txt', 'r')
# while i < 100000:
#     waveform = dso.GetScaledWaveformWithTimes("C1", 200000, 0)
#     waveform1 = dso.GetScaledWaveformWithTimes("C3", 200000, 0)
#     if operator.eq(waveform[1], wave_test) == False:
#         t1 = tools.Wavetools(waveform[0], waveform[1])
#         t2 = tools.Wavetools(waveform1[0], waveform1[1])
#         energy_0 = t1.get_energy_2(0.2)
#         amp_0 = t1.get_amplitude()
#         energy.append(energy_0)
#         amp.append(amp_0)
#         energy_1 = t2.get_energy_2(0.2)
#         amp_1 = t2.get_amplitude()
#         energy1.append(energy_1)
#         amp1.append(amp_1)
#         i = i + 1
#         wave_test = waveform[1]
#         f.write(str(energy_0) + ' ' + str(amp_0) + ' ' + str(energy_1) + ' ' + str(amp_1) + '\n')
#         if i % 50 == 0:
#             print(i)
#             plt.clf()
#             plt.hist(energy, 100, range=(0, 30))
#             plt.pause(0.001)
#         # if i % 500 == 0:
#         #     a = f2.read()
#         #     if a == 'stop':
#         #         break
#         #     f2.seek(0, 0)
# print(amp)
# for k in range(0, len(energy)):
#     f.write(str(energy[k]) + ' ' + str(amp[k]) + ' ' + str(energy1[k]) + ' ' + str(amp1[k]) + '\n')
# k = 0
# while k < 100000:
#     waveform0 = dos_0.get_wave()
#     if operator.eq(waveform0['c1'][1], wave_test) == False:
#         if para_0['SEQ'] == 'ON':
#             wave_test = waveform0['c1'][1]
#             for i in range(0, para_0['SEQ_N']):
#                 # c1
#                 t1 = tools.Wavetools(waveform0['c1'][0][i], waveform0['c1'][1][i])
#                 e_1 = t1.get_energy_2(0.2)
#                 amp_1 = t1.get_amplitude()
#
#                 # c2
#                 t2 = tools.Wavetools(waveform0['c2'][0][i], waveform0['c2'][1][i])
#                 e_2 = t2.get_energy_2(0.2)
#                 amp_2 = t2.get_amplitude()
#
#                 energy.append(e_1)
#                 amp.append(amp_1)
#                 energy1.append(e_2)
#                 amp1.append(amp_2)
#
#                 # f.write(str(e_1) + ' ' + str(amp_1) + ' ' + str(e_2) + ' ' + str(amp_2) + '\n')
#                 k = k + 1
#                 if k % 200 == 0:
#                     print(k)
#                     plt.clf()
#                     plt.hist(energy, 100, range=(0, 30))
#                     plt.pause(0.001)
#
# for m in range(0, len(energy)):
#     f.write(str(energy[m]) + ' ' + str(amp[m]) + ' ' + str(energy1[m]) + ' ' + str(amp1[m]) + '\n')
# print(len(energy))

i = 0
wave_test = []
energy = []
amp = []
energy1 = []
amp1 = []
waveloop = []
wave1 = []
para_0 = {'SEQ': 'ON', 'SEQ_N': 200, 'polarity': '1'}
dos_0 = dso.Dso(para_0)

def loop_e_t1():
    while 1:
        global dos_0
        global wave1
        global waveloop
        waveform0 = dos_0.get_wave()
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
    plt.ion()
    plt.figure(1)
    k = 0
    while k < 10000:
        if len(waveloop) > 0:
            if para_0['SEQ'] == 'ON':
                for i in range(0, para_0['SEQ_N']):
                    # c1


                    # c2
                    name0 = 'wavefile/'
                    name1 = 'standard--'
                    name2 = '.txt'
                    filename = name0 + name1 + str(k) + name2
                    f2 = open(filename, 'a')
                    for m in range(0, len(waveloop[0]['c2'][0][i])):
                        f2.write(str(waveloop[0]['c2'][0][i][m]) + ' ' + str(waveloop[0]['c2'][1][i][m]) + '\n')
                    f2.close()
                    print(k)
                    k = k + 1
                waveloop.pop(0)

th3 = threading.Thread(target=loop_e_t1)
th3.start()
th4 = threading.Thread(target=loop_e_t2)
th4.start()