class Wavetools():
    #
    def __init__(self, time0, voltage0):
        self.time0 = time0
        self.voltage0 = voltage0
        self.max_0 = max(self.voltage0)
        self.min_0 = min(self.voltage0)

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
        a = self.find_baseline(20) + 10
        return a

    def get_energy(self, bin, basenum):
        base = self.find_baseline(basenum)
        energy = 0.
        for voltage in self.voltage0:
            energy = energy + bin*(voltage - base)
        return energy

    def get_amplitude(self, basenum):
        base = self.find_baseline(basenum)
        amp = self.max_0 - base
        return amp

    def find_startchannel(self, basenum):
        max_channel = self.voltage0.index(self.max_0)
        base = self.find_baseline(basenum)
        i = max_channel
        while i > 0:
            if self.voltage0[i] < base:
                break
            i = i - 1
        return i

#time0000oooooooooooooooo0000000000000000000ooooooooooooo

    def get_time_led_linear(self, basenum, thr):
        start_c = self.find_startchannel(basenum)
        base = self.find_baseline(basenum)
        for i in range(start_c, len(self.voltage0)):
            if self.voltage0[i] > (thr + base):
                break
        t_0 = (thr + base - self.voltage0[i-1]) * (self.time0[i] - self.time0[i-1])/(self.voltage0[i] - self.voltage0[i-1]) + self.time0[i-1]
        return t_0

    def get_time_cfd_linear(self, basenum, fraction):
        start_c = self.find_startchannel(basenum)
        base = self.find_baseline(basenum)
        for i in range(start_c, len(self.voltage0)):
            if self.voltage0[i] > (fraction*(self.max_0 - base) + base):
                break
        t_0 = (fraction*(self.max_0 - base) + base - self.voltage0[i-1]) * (self.time0[i] - self.time0[i-1])/(self.voltage0[i] - self.voltage0[i-1]) + self.time0[i-1]
        return t_0

    def get_time_cfd_poln(self, basenum, fraction, poln, range):
        base = self.find_baseline(basenum)
        start_c = self.find_startchannel(basenum)
        t_0 = self.time0[start_c]