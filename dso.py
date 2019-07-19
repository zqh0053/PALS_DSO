import win32com.client
import numpy as np
import tools as tl1

class Dso():
    def __init__(self,parameters):
        self.parameters = parameters
        self.switch0 = 0
        self.dso = win32com.client.Dispatch('LeCroy.ActiveDSOCtrl.1')
        # self.dso.MakeConnection("IP:192.168.0.101")
        # #self.dso.WriteString("C1:ASET", 1)
        # #self.dso.WriteString("C2:ASET", 1)
        # self.dso.WriteString("C1:VDIV .60", 1)
        # self.dso.WriteString("C2:VDIV .60", 1)
        # self.dso.WriteString("C1:TRLV " + str(self.parameters['C1_TRLV']), 1)
        # self.dso.WriteString("C2:TRLV " + str(self.parameters['C2_TRLV']), 1)
        # self.dso.WriteString("C1:TRSL NEG", 1)
        # self.dso.WriteString("C2:TRSL NEG", 1)
        # self.dso.WriteString("C1:OFST 1.2", 1)
        # self.dso.WriteString("C2:OFST 1.2", 1)
        # if self.parameters['SEQ'] == 'ON':
        #     self.dso.WriteString("C1:SEQ ON," + str(self.parameters['SEQ_N']), True)
        # else:
        #     self.dso.WriteString("SEQ OFF", 1)
        # self.dso.WriteString("C1:TIME_DIV 20NS", 1)
        # self.dso.WriteString("C2:TIME_DIV 20NS", 1)
        # self.dso.WriteString("TRSE TEQ,SR,C2,QL,C1,HT,TL,HV,50E-9 S", 1)
        # self.dso.WriteString("C1:TRMD?", True)
        # str1 = self.dso.ReadString(80)
        # print(str1)
        # self.dso.WriteString("TRDL 30NS", 1)

    def get_wave(self):
        # c1_waveform_0 = self.dso.GetScaledWaveformWithTimes("C1", 200000, 0)
        # c1_waveform_time = list(c1_waveform_0[0])
        # c1_waveform_v = list(c1_waveform_0[1])
        # c2_waveform_0 = self.dso.GetScaledWaveformWithTimes("C2", 200000, 0)
        # c2_waveform_time = list(c2_waveform_0[0])
        # c2_waveform_v = list(c2_waveform_0[1])
        c1_waveform_0 = self.dso.GetScaledWaveformWithTimes("C1", 200000, 0)
        c1_waveform_time = np.array(c1_waveform_0[0])
        c1_waveform_v = np.array(c1_waveform_0[1])
        c2_waveform_0 = self.dso.GetScaledWaveformWithTimes("C2", 200000, 0)
        c2_waveform_time = np.array(c2_waveform_0[0])
        c2_waveform_v = np.array(c2_waveform_0[1])
        if self.parameters['polarity'] == 'negative':
            # for i in range(0,len(c1_waveform_v)):
            #     c1_waveform_v[i] = -1 * c1_waveform_v[i]
            #     c1_waveform_time[i] = 1000000000 * c1_waveform_time[i]
            #     c2_waveform_v[i] = -1 * c2_waveform_v[i]
            #     c2_waveform_time[i] = 1000000000 * c2_waveform_time[i]
            c1_waveform_v = c1_waveform_v * -1.
            c1_waveform_time = c1_waveform_time * 1000000000
            c2_waveform_v = c2_waveform_v * -1.
            c2_waveform_time = c2_waveform_time * 1000000000
        waveform = {}
        c1_waveform = [c1_waveform_time.tolist(), c1_waveform_v.tolist()]
        c2_waveform = [c2_waveform_time.tolist(), c2_waveform_v.tolist()]
        if self.parameters['SEQ'] == 'ON':
            n = int(len(c1_waveform[0])/self.parameters['SEQ_N'])
            c1_waveform[0] = [c1_waveform[0][i:i + n] for i in range(0, len(c1_waveform[0]), n)]
            c1_waveform[1] = [c1_waveform[1][i:i + n] for i in range(0, len(c1_waveform[1]), n)]
            c2_waveform[0] = [c2_waveform[0][i:i + n] for i in range(0, len(c2_waveform[0]), n)]
            c2_waveform[1] = [c2_waveform[1][i:i + n] for i in range(0, len(c2_waveform[1]), n)]
        waveform['c1'] = c1_waveform
        waveform['c2'] = c2_waveform
        #waveform['c3'] = c3_waveform
        return waveform

    def close(self):
        self.switch0 = 0

    def open(self):
        self.switch0 = 1

    def isOpen(self):
        if self.switch0 == 1:
            return True
        else:
            return False

    def setDSO(self, str):
        a = 0
        self.dso.WriteString(str, 1)
