#
# import numpy as np
# import json
#
# data_test = []
# for i in range(0, 10000000):
#     data_0 = {'sd': 0.1 * i, 'qw': 'qwe'}
#     data_test.append(data_0)
# # data_json = json.dumps(data_test)
# # with open("../a.json","w") as f:
# #     json.dump(data_json, f)
# print('123')
# prompt = "\nEnter 'quit'\n"
# message = ''
# while message != 'quit':
#     message = input(prompt)
#     print(message)
import win32com.client
import dso
import operator
import tools
import matplotlib.pyplot as plt
import threading
import numpy as np
amp = []
energy = []
for i in range(0, 10000):
    time_1 = []
    volt_1 = []
    filename1 = "ch4/before/C3--200mV-ch4b--"
    m = str(i)
    filename2 = '.txt'
    filename = filename1 + m.zfill(5) + filename2
    k = 0
    with open(filename) as file1_object:
        for lines in file1_object:
            if k < 5:
                k = k + 1
            else:
                line = lines.rstrip().split(',')
                time_1.append(1000000000 * float(line[0]))
                volt_1.append(-1 * float(line[1]))
    file1_object.close()
    t1 = tools.Wavetools(time_1, volt_1, basenum=9000)
    amp_1 = t1.get_amplitude()
    e1 = t1.get_energy_2(2)
    amp.append(amp_1)
    energy.append(e1)
    if i % 100 == 0:
        print(i)
f = open("ch4/amp_b.txt", "a")
for m in range(0, len(amp)):
    f.write(str(amp[m]) + ' ' + str(energy[m]) + '\n')
f.close()
print(len(amp))