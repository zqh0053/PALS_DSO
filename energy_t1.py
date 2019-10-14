import win32com.client
import operator
import tools
import matplotlib.pyplot as plt
import numpy as np

dso = win32com.client.Dispatch('LeCroy.ActiveDSOCtrl.1')
dso.MakeConnection("IP:211.86.148.140")
i = 0
wave_test = []
energy = []
amp = []
plt.ion()
plt.figure(1)
print(i)
while i < 1000:
    waveform = dso.GetScaledWaveformWithTimes("C1", 200000, 0)
    if operator.eq(waveform[1], wave_test) == False:
        t1 = tools.Wavetools(waveform[0], waveform[1])
        energy_0 = t1.get_energy(0.2)
        amp_0 = t1.get_amplitude()
        energy.append(energy_0)
        amp.append(amp_0)
        i = i + 1
        if i % 500 == 0:
            plt.clf()
            plt.hist(amp, 0.01, range=(0, 2))
            plt.draw()
print(amp)
f = open("energy_1.txt", "a")
for k in range(0, len(energy)):
    f.write(str(energy[k]) + ' ' + str(amp[k]) + '\n')