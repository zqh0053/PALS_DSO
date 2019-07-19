import wx
import numpy as np
import matplotlib
import threading
import time
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use("WXAgg")
app = wx.App()
frm = wx.Frame(None, title="Hello World",size=(1200, 800))
#frm.Show()
scorePanel = wx.Panel(frm)
but1 = wx.Button(scorePanel, 0, 'asd', pos=(600,600), size=(100,100))
box1 = wx.ListBox(scorePanel,pos=(0,0),size=(500,500))
drawHistF = Figure(figsize=(5, 5), dpi=100)
m = 3.0
drawHistCanvas = FigureCanvas(box1, -1, drawHistF)
drawHistCanvas.draw()
print('test')
def loop_graph():
    global m
    global drawHistF
    global drawHistCanvas
    while m < 5.0:
        drawHistF.clf()
        a = drawHistF.add_subplot(111)
        t = np.arange(0.0, m, 0.01)
        s = np.sin(2 * np.pi * t)
        a.plot(t, s)
        #drawHistCanvas = FigureCanvas(box1, -1, drawHistF)
        drawHistCanvas.draw()
        m = m + 0.1
        time.sleep(0.01)

def loop_test(event):
    t1 = threading.Thread(target=loop_graph)
    print('asd')
    t1.setDaemon(True)
    t1.start()

but1.Bind(wx.EVT_BUTTON,loop_test)

frm.Show()
app.MainLoop()