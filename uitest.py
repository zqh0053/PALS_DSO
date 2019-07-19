import numpy as np
import tkinter as tk
import matplotlib
import time
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
def loop_graph():
    #global a
    #global drawHistF
    #global drawHistCanvas
    loop_graph.drawHistF = Figure(figsize=(5, 5), dpi=100)
    a = loop_graph.drawHistF.add_subplot(111)
    t = np.arange(0.0, 3.0, 0.1)
    s = np.sin(2 * np.pi * t)
    a.plot(t, s)
    loop_graph.drawHistCanvas = FigureCanvasTkAgg(loop_graph.drawHistF, master=Information)
    loop_graph.drawHistCanvas.draw()
    loop_graph.drawHistCanvas.get_tk_widget().grid(row=0, columnspan=3)
    loop_graph.m = 3.0
    while True:
        loop_graph.drawHistF.clf()
        a = loop_graph.drawHistF.add_subplot(111)
        t = np.arange(0.0,loop_graph.m, 0.1)
        s = np.sin(2 * np.pi * t)
        a.plot(t, s)
        #drawHistCanvas = FigureCanvasTkAgg(drawHistF, master=Information)
        loop_graph.drawHistCanvas.draw()
        if loop_graph.m > 10:
            loop_graph.m = loop_graph.m - 8
        loop_graph.m = loop_graph.m + 0.1
        print(loop_graph.m)
def loop_test():
    t = threading.Thread(target=loop_graph)
    print('asd')
    t.setDaemon(True)
    t.start()
if __name__ == '__main__':
    matplotlib.use('TkAgg')
    window = tk.Tk()
    window.title('test_window')
    window.geometry('1200x800')

    Information = tk.LabelFrame(window, text="energy",padx=10,pady=10)
    Information.place(x=200, y=20)







    tk.Button( window, text = "开始采集", command = loop_test).pack( side = "left", padx = 13 )



    window.mainloop()