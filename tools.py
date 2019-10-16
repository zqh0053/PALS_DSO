import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit
class Wavetools():
    #
    def __init__(self, time0, voltage0, basenum = 800):
        self.time0 = time0
        self.voltage0 = voltage0
        self.basenum = basenum
        self.max_0 = max(self.voltage0)
        self.min_0 = min(self.voltage0)
        self.base = self.find_baseline()
        self.start_c = self.find_startchannel()

    def find_baseline(self):
        if self.basenum > 0:
            max_channel = self.voltage0.index(self.max_0)
            if max_channel == 0:
                max_channel = 5
            if max_channel < self.basenum:
                min_channel = self.voltage0.index(min(self.voltage0[0:max_channel]))
                n = min_channel
                while n > 0:
                    if self.voltage0[n] < 0.01*(self.max_0 - self.min_0):
                        break
                    n = n - 1
                t_num = int(5/(self.time0[1]-self.time0[0]))
                if (n - min_channel) > t_num:
                    self.basenum = n - int(3/(self.time0[1]-self.time0[0]))
                else:
                    self.basenum = n - int((n - min_channel)*0.6)
            total = 0
            if self.basenum == 0:
                self.basenum = self.basenum + 1
            for i in range(0,self.basenum):
                total = total + self.voltage0[i]
            m = total/self.basenum
        if self.basenum == 0:
            m = 0
        return m

    def test1(self):
        a = self.find_baseline() + 10
        return a

    def get_energy(self, bin):
        energy = 0.
        for voltage in self.voltage0:
            energy = energy + bin*(voltage - self.base)
        return energy

    def get_energy_2(self, bin):
        energy = 0.
        max_channel = self.voltage0.index(self.max_0)
        voltage_1 = []
        for k in range(0, len(self.voltage0)):
            voltage_1.append(self.voltage0[k])
            if k > max_channel:
                if self.voltage0[k] < self.base:
                    break
        for voltage in voltage_1:
            energy = energy + bin*(voltage - self.base)
        return energy

    def get_amplitude(self):
        amp = self.max_0 - self.base
        return amp

    def find_startchannel(self):
        max_channel = self.voltage0.index(self.max_0)
        base = self.find_baseline()
        i = max_channel
        while i > 0:
            if self.voltage0[i] < base:
                break
            i = i - 1
        return i

    def get_slope(self):
        max_channel = self.voltage0.index(self.max_0)
        slope = (self.max_0 - self.base)/(self.time0[max_channel] - self.time0[self.start_c])
        return slope

    def get_slope_max(self):
        max_channel = self.voltage0.index(self.max_0)
        slope = 0.
        for i in range(self.start_c, max_channel):
            m = (self.voltage0[i + 1] - self.voltage0[i])/(self.time0[i + 1] - self.time0[i])
            if m > slope:
                slope = m
        return slope

# time0000oooooooooooooooo0000000000000000000ooooooooooooo

    def get_time_led_linear(self, thr):
        # start_c = self.find_startchannel()
        for i in range(self.start_c, len(self.voltage0)):
            if self.voltage0[i] > (thr + self.base):
                break
        t_0 = (thr + self.base - self.voltage0[i-1]) * (self.time0[i] - self.time0[i-1])/(self.voltage0[i] - self.voltage0[i-1]) + self.time0[i-1]
        return t_0

    def get_time_cfd_linear(self, fraction):
        # start_c = self.find_startchannel()
        for i in range(self.start_c, len(self.voltage0)):
            if self.voltage0[i] > (fraction*(self.max_0 - self.base) + self.base):
                break
        t_0 = (fraction*(self.max_0 - self.base) + self.base - self.voltage0[i-1]) * (self.time0[i] - self.time0[i-1])/(self.voltage0[i] - self.voltage0[i-1]) + self.time0[i-1]
        return t_0

    def get_time_cfd_poln(self, fraction, poln, range0):
        #start_c = self.find_startchannel()
        t_0 = self.time0[self.start_c]
        n = self.start_c
        x1 = []
        y1 = []
        linear_0 = 1
        num_p = 0
        t_1 = 0
        for i in range(0, len(self.voltage0)):
            x1.append(self.time0[n])
            y1.append(self.voltage0[n])
            if self.voltage0[n] > (range0*(self.max_0 - self.base) + self.base):
                num_p = i
                break
            n = n+1
        if (num_p + 1) > poln:
            f1 = np.polyfit(x1, y1, poln)
            p1 = np.poly1d(f1)
            k = p1(3.5)
            if k == 0:
                linear_0 = 0
        else:
            linear_0 = 0
        if linear_0 == 0:
            for i in range(self.start_c, len(self.voltage0)):
                if self.voltage0[i] > (fraction*(self.max_0 - self.base) + self.base):
                    t_1 = (fraction*(self.max_0 - self.base) + self.base - self.voltage0[i-1]) * (self.time0[i] - self.time0[i-1])/(self.voltage0[i] - self.voltage0[i-1]) + self.time0[i-1]
                    break
        else:
            x2 = t_0
            while x2 < 500:
                y2 = p1(x2)
                if y2 > (fraction * (self.max_0 - self.base) + self.base):
                    y2_0 = p1(x2 - 0.005)
                    t_1 = (fraction * (self.max_0 - self.base) + self.base - y2_0) * 0.005 / (y2 - y2_0) + \
                          x2 - 0.005
                    break
                x2 = x2 + 0.005
        return t_1

    # def gaussian(self, x, *param):
    #     return param[0] * np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.))) + param[1] * np.exp(
    #         -np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))
    def gaussian(self, x, p0, p1, p2, p3, p4, p5):
        return p0 * np.exp(-np.power(x - p2, 2.) / (2 * np.power(p4, 2.))) + p1 * np.exp(
            -np.power(x - p3, 2.) / (2 * np.power(p5, 2.)))

    def get_time_cfd_gaus(self, fraction, range0):
        #start_c = self.find_startchannel()
        t_0 = self.time0[self.start_c]
        n = self.start_c
        x1 = []
        y1 = []
        linear_0 = 1
        num_p = 0
        t_1 = 0
        for i in range(0, len(self.voltage0)):
            x1.append(self.time0[n])
            y1.append(self.voltage0[n])
            if self.voltage0[n] > (range0*(self.max_0 - self.base) + self.base):
                num_p = i
                break
            n = n+1

        popt,pcov = curve_fit(self.gaussian, x1, y1)
        k = self.gaussian(3.5, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
        if k == 0:
            linear_0 = 0
        else:
            linear_0 = 0
        if linear_0 == 0:
            for i in range(self.start_c, len(self.voltage0)):
                if self.voltage0[i] > (fraction*(self.max_0 - self.base) + self.base):
                    t_1 = (fraction*(self.max_0 - self.base) + self.base - self.voltage0[i-1]) * (self.time0[i] - self.time0[i-1])/(self.voltage0[i] - self.voltage0[i-1]) + self.time0[i-1]
                    break
        else:
            x2 = t_0
            while x2 < 500:
                y2 = self.gaussian(x2, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
                if y2 > (fraction * (self.max_0 - self.base) + self.base):
                    y2_0 = self.gaussian(x2, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
                    t_1 = (fraction * (self.max_0 - self.base) + self.base - y2_0) * 0.005 / (y2 - y2_0) + \
                          x2 - 0.005
                    break
                x2 = x2 + 0.005
        return t_1

    def get_time_led_poln(self, thr, poln, range0): # threshold
        #start_c = self.find_startchannel()
        t_0 = self.time0[self.start_c]
        n = self.start_c
        x1 = []
        y1 = []
        linear_0 = 1
        num_p = 0
        t_1 = 0
        for i in range(0, len(self.voltage0)):
            x1.append(self.time0[n])
            y1.append(self.voltage0[n])
            if self.voltage0[n] > (range0*(self.max_0 - self.base) + self.base):
                num_p = i
                break
            n = n+1
        if (num_p + 1) > poln:
            f1 = np.polyfit(x1, y1, poln)
            p1 = np.poly1d(f1)
            k = p1(3.5)
            if k == 0:
                linear_0 = 0
        else:
            linear_0 = 0
        if linear_0 == 0:
            for i in range(self.start_c, len(self.voltage0)):
                if self.voltage0[i] > (thr*(self.max_0 - self.base) + self.base):
                    t_1 = (thr + self.base - self.voltage0[i - 1]) * (
                                self.time0[i] - self.time0[i - 1]) / (self.voltage0[i] - self.voltage0[i - 1]) + \
                          self.time0[i - 1]
                    break
        else:
            x2 = t_0
            while x2 < 500:
                y2 = p1(x2)
                if y2 > (thr * (self.max_0 - self.base) + self.base):
                    y2_0 = p1(x2 - 0.005)
                    t_1 = (thr + self.base - y2_0) * 0.005 / (y2 - y2_0) + \
                          x2 - 0.005
                    break
                x2 = x2 + 0.005
        return t_1

    def get_time_cfd_interpolation(self, fraction, kind='cubic'):
        n = self.start_c
        f = interpolate.interp1d(self.time0, self.voltage0, kind=kind)
        t_new = np.linspace(self.time0[0], self.time0[-1], 5*(len(self.time0) - 1) + 1)
        v_new = f(t_new)
        for i in range(5 * n, len(v_new)):
            if v_new[i] > (fraction * (self.max_0 - self.base) + self.base):
                break
        t_0 = (fraction * (self.max_0 - self.base) + self.base - v_new[i - 1]) * (t_new[i] - t_new[i - 1]) / (
                    v_new[i] - v_new[i - 1]) + t_new[i - 1]
        return t_0
