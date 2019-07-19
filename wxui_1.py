import wx
import dso
import tools
import numpy as np
import matplotlib
import threading
import operator
import time
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class myFrame(wx.Frame):
    def __init__(self):
        self.para_0 = {'SEQ': 'ON', 'SEQ_N': 200, 'polarity': 'negative'}
        #self.dos_0 = dso.Dso(self.para_0)
        super().__init__(None, -1, title='PALS',size = (1200, 800))

        #
        self.para_0['C1_TRLV'] = -0.1
        self.para_0['C2_TRLV'] = -0.1
        self.dos_0 = dso.Dso(self.para_0)
        #
        self.e_rg = {'c1': [0., 100.], 'c2': [0., 100.], 'c1_amp': [0., 5.], 'c2_amp': [0., 5.]}
        self.lt_start_l = 0.
        self.lt_start_r = 300.
        self.start_fraction = 0.15
        self.lt_stop_l = 0.
        self.lt_stop_r = 300.
        self.stop_fraction = 0.2
        self.cps = 0.
        self.lt_bins = 100
        self.lt_l = -10.0
        self.lt_r = 10.0
        self.total_counts = 0
        self.counts_set = 1000000

        self.note1 = wx.Notebook(self)
        #建立page
        self.scorePanel = wx.Panel(self.note1)
        self.scorePanel_lt = wx.Panel(self.note1)
        self.note1.AddPage(self.scorePanel, "Energy")
        self.note1.AddPage(self.scorePanel_lt, "LifeTime")
        #能量显示窗口
        self.e_gridsizer = wx.GridBagSizer(2, 2)
        self.scorePanel.SetSizer(self.e_gridsizer)
        # self.box1 = wx.ListBox(self.scorePanel,size=(800, 500))
        # self.drawHistF = Figure(figsize=(8, 5), dpi=100)
        # self.drawHistCanvas = FigureCanvas(self.box1, -1, self.drawHistF)
        # self.drawHistCanvas.draw()
        self.box1 = wx.ListBox(self.scorePanel,size=(800,500))
        self.e_gridsizer.Add(self.box1, pos=(0, 0), flag=wx.EXPAND)
        self.box2 = wx.Panel(self.scorePanel)
        self.e_gridsizer.Add(self.box2, pos=(0, 1), flag=wx.EXPAND)
        self.box3 = wx.Panel(self.scorePanel)
        self.e_gridsizer.Add(self.box3, span=(1, 2), pos=(1, 0), flag=wx.EXPAND)
        self.scorePanel.Fit()

        self.drawHistF = Figure(figsize=(8, 5), dpi=100)
        self.drawHistCanvas = FigureCanvas(self.box1, -1, self.drawHistF)
        self.drawHistCanvas.draw()
        #右侧区域
        # self.box2 = wx.Panel(self.scorePanel, pos=(810, 0), size=(370, 500))
        # self.but1 = wx.Button(self.box2, 0, 'start', pos=(10, 10), size=(100, 50))
        # self.but2 = wx.Button(self.box2, 0, 'stop', pos=(120, 10), size=(100, 50))
        # self.but3 = wx.Button(self.box2, 0, 'clear', pos=(230, 10), size=(100, 50))
        # self.but1.Bind(wx.EVT_BUTTON, self.start_but)
        # self.but2.Bind(wx.EVT_BUTTON, self.stop_but)
        # self.but3.Bind(wx.EVT_BUTTON, self.energy_clear)
        self.eb2_gridsizer = wx.GridBagSizer(8, 3)
        self.box2.SetSizer(self.eb2_gridsizer)
        self.but1 = wx.Button(self.box2, -1, 'start')
        self.but2 = wx.Button(self.box2, -1, 'stop')
        self.but3 = wx.Button(self.box2, -1, 'clear')
        self.but1.Bind(wx.EVT_BUTTON, self.start_but)
        self.but2.Bind(wx.EVT_BUTTON, self.stop_but)
        self.but3.Bind(wx.EVT_BUTTON, self.energy_clear)
        self.eb2_gridsizer.Add(self.but1, pos=(0, 0), flag=wx.EXPAND)
        self.eb2_gridsizer.Add(self.but2, pos=(0, 1), flag=wx.EXPAND)
        self.eb2_gridsizer.Add(self.but3, pos=(0, 2), flag=wx.EXPAND)

        # 下方区域

        self.eb3_gridsizer = wx.GridBagSizer(1, 4)
        self.box3.SetSizer(self.eb3_gridsizer)
        self.eb3_c1_panel = wx.Panel(self.box3)
        self.eb3_gridsizer.Add(self.eb3_c1_panel, pos=(0, 0), flag=wx.EXPAND)
        self.eb3_c2_panel = wx.Panel(self.box3)
        self.eb3_gridsizer.Add(self.eb3_c2_panel, pos=(0, 1), flag=wx.EXPAND)
        # energy_c1_set
        self.eb3c1_gridsizer = wx.GridBagSizer(6, 4)
        self.eb3_c1_panel.SetSizer(self.eb3c1_gridsizer)
        self.eb3c1_title = wx.StaticText(self.eb3_c1_panel, -1, label='channel 1', style=wx.ALIGN_CENTER)
        self.font1 = wx.Font(15,  wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.eb3c1_title.SetFont(self.font1)
        self.eb3c1_gridsizer.Add(self.eb3c1_title, span=(1, 4), pos=(0, 0), flag=wx.EXPAND)
        #
        self.eb3c1_trlv = wx.TextCtrl(self.eb3_c1_panel, -1, str(self.para_0['C1_TRLV']), style=wx.TE_CENTER)
        self.eb3c1_gridsizer.Add(self.eb3c1_trlv, span=(1, 2), pos=(1, 1), flag=wx.EXPAND)
        self.eb3c1_but1 = wx.Button(self.eb3_c1_panel, -1, 'Set')
        self.eb3c1_gridsizer.Add(self.eb3c1_but1, span=(1, 1), pos=(1, 3), flag=wx.EXPAND)
        self.eb3c1_but1.Bind(wx.EVT_BUTTON, self.e_c1_set_trlv)
        self.eb3c1_trlv_text = wx.StaticText(self.eb3_c1_panel, -1, 'c1_trlv', style=wx.ALIGN_CENTER)
        self.eb3c1_trlv_text.SetFont(self.font1)
        self.eb3c1_gridsizer.Add(self.eb3c1_trlv_text, span=(1, 1), pos=(1, 0), flag=wx.EXPAND)
        #
        self.eb3c1_erg_l_text = wx.StaticText(self.eb3_c1_panel, -1, 'energy_l', style=wx.ALIGN_CENTER)
        self.eb3c1_erg_l_text.SetFont(self.font1)
        self.eb3c1_gridsizer.Add(self.eb3c1_erg_l_text, span=(1, 1), pos=(2, 0), flag=wx.EXPAND)
        self.eb3c1_erg_l = wx.TextCtrl(self.eb3_c1_panel, -1, str(self.e_rg['c1'][0]), style=wx.TE_CENTER)
        self.eb3c1_gridsizer.Add(self.eb3c1_erg_l, span=(1, 1), pos=(2, 1), flag=wx.EXPAND)

        self.eb3c1_erg_r_text = wx.StaticText(self.eb3_c1_panel, -1, 'energy_r', style=wx.ALIGN_CENTER)
        self.eb3c1_erg_r_text.SetFont(self.font1)
        self.eb3c1_gridsizer.Add(self.eb3c1_erg_r_text, span=(1, 1), pos=(2, 2), flag=wx.EXPAND)
        self.eb3c1_erg_r = wx.TextCtrl(self.eb3_c1_panel, -1, str(self.e_rg['c1'][1]), style=wx.TE_CENTER)
        self.eb3c1_gridsizer.Add(self.eb3c1_erg_r, span=(1, 1), pos=(2, 3), flag=wx.EXPAND)

        self.eb3c1_amp_l_text = wx.StaticText(self.eb3_c1_panel, -1, 'amp_l', style=wx.ALIGN_CENTER)
        self.eb3c1_amp_l_text.SetFont(self.font1)
        self.eb3c1_gridsizer.Add(self.eb3c1_amp_l_text, span=(1, 1), pos=(3, 0), flag=wx.EXPAND)
        self.eb3c1_amp_l = wx.TextCtrl(self.eb3_c1_panel, -1, str(self.e_rg['c1_amp'][0]), style=wx.TE_CENTER)
        self.eb3c1_gridsizer.Add(self.eb3c1_amp_l, span=(1, 1), pos=(3, 1), flag=wx.EXPAND)

        self.eb3c1_amp_r_text = wx.StaticText(self.eb3_c1_panel, -1, 'amp_r', style=wx.ALIGN_CENTER)
        self.eb3c1_amp_r_text.SetFont(self.font1)
        self.eb3c1_gridsizer.Add(self.eb3c1_amp_r_text, span=(1, 1), pos=(3, 2), flag=wx.EXPAND)
        self.eb3c1_amp_r = wx.TextCtrl(self.eb3_c1_panel, -1, str(self.e_rg['c1_amp'][1]), style=wx.TE_CENTER)
        self.eb3c1_gridsizer.Add(self.eb3c1_amp_r, span=(1, 1), pos=(3, 3), flag=wx.EXPAND)

        self.eb3c1_but2 = wx.Button(self.eb3_c1_panel, -1, 'Set')
        self.eb3c1_gridsizer.Add(self.eb3c1_but2, span=(1, 4), pos=(4, 0), flag=wx.EXPAND)
        self.eb3c1_but2.Bind(wx.EVT_BUTTON, self.e_c1_set_range)
        # energy_c2_set
        self.eb3c2_gridsizer = wx.GridBagSizer(6, 4)
        self.eb3_c2_panel.SetSizer(self.eb3c2_gridsizer)
        self.eb3c2_title = wx.StaticText(self.eb3_c2_panel, -1, label='channel 1', style=wx.ALIGN_CENTER)
        self.eb3c2_title.SetFont(self.font1)
        self.eb3c2_gridsizer.Add(self.eb3c2_title, span=(1, 4), pos=(0, 0), flag=wx.EXPAND)
        #
        self.eb3c2_trlv = wx.TextCtrl(self.eb3_c2_panel, -1, str(self.para_0['C2_TRLV']), style=wx.TE_CENTER)
        self.eb3c2_gridsizer.Add(self.eb3c2_trlv, span=(1, 2), pos=(1, 1), flag=wx.EXPAND)
        self.eb3c2_but1 = wx.Button(self.eb3_c2_panel, -1, 'Set')
        self.eb3c2_gridsizer.Add(self.eb3c2_but1, span=(1, 1), pos=(1, 3), flag=wx.EXPAND)
        self.eb3c2_but1.Bind(wx.EVT_BUTTON, self.e_c2_set_trlv)
        self.eb3c2_trlv_text = wx.StaticText(self.eb3_c2_panel, -1, 'c2_trlv', style=wx.ALIGN_CENTER)
        self.eb3c2_trlv_text.SetFont(self.font1)
        self.eb3c2_gridsizer.Add(self.eb3c2_trlv_text, span=(1, 1), pos=(1, 0), flag=wx.EXPAND)
        #
        self.eb3c2_erg_l_text = wx.StaticText(self.eb3_c2_panel, -1, 'energy_l', style=wx.ALIGN_CENTER)
        self.eb3c2_erg_l_text.SetFont(self.font1)
        self.eb3c2_gridsizer.Add(self.eb3c2_erg_l_text, span=(1, 1), pos=(2, 0), flag=wx.EXPAND)
        self.eb3c2_erg_l = wx.TextCtrl(self.eb3_c2_panel, -1, str(self.e_rg['c2'][0]), style=wx.TE_CENTER)
        self.eb3c2_gridsizer.Add(self.eb3c2_erg_l, span=(1, 1), pos=(2, 1), flag=wx.EXPAND)

        self.eb3c2_erg_r_text = wx.StaticText(self.eb3_c2_panel, -1, 'energy_r', style=wx.ALIGN_CENTER)
        self.eb3c2_erg_r_text.SetFont(self.font1)
        self.eb3c2_gridsizer.Add(self.eb3c2_erg_r_text, span=(1, 1), pos=(2, 2), flag=wx.EXPAND)
        self.eb3c2_erg_r = wx.TextCtrl(self.eb3_c2_panel, -1, str(self.e_rg['c2'][1]), style=wx.TE_CENTER)
        self.eb3c2_gridsizer.Add(self.eb3c2_erg_r, span=(1, 1), pos=(2, 3), flag=wx.EXPAND)

        self.eb3c2_amp_l_text = wx.StaticText(self.eb3_c2_panel, -1, 'amp_l', style=wx.ALIGN_CENTER)
        self.eb3c2_amp_l_text.SetFont(self.font1)
        self.eb3c2_gridsizer.Add(self.eb3c2_amp_l_text, span=(1, 1), pos=(3, 0), flag=wx.EXPAND)
        self.eb3c2_amp_l = wx.TextCtrl(self.eb3_c2_panel, -1, str(self.e_rg['c2_amp'][0]), style=wx.TE_CENTER)
        self.eb3c2_gridsizer.Add(self.eb3c2_amp_l, span=(1, 1), pos=(3, 1), flag=wx.EXPAND)

        self.eb3c2_amp_r_text = wx.StaticText(self.eb3_c2_panel, -1, 'amp_r', style=wx.ALIGN_CENTER)
        self.eb3c2_amp_r_text.SetFont(self.font1)
        self.eb3c2_gridsizer.Add(self.eb3c2_amp_r_text, span=(1, 1), pos=(3, 2), flag=wx.EXPAND)
        self.eb3c2_amp_r = wx.TextCtrl(self.eb3_c2_panel, -1, str(self.e_rg['c2_amp'][1]), style=wx.TE_CENTER)
        self.eb3c2_gridsizer.Add(self.eb3c2_amp_r, span=(1, 1), pos=(3, 3), flag=wx.EXPAND)

        self.eb3c2_but2 = wx.Button(self.eb3_c2_panel, -1, 'Set')
        self.eb3c2_gridsizer.Add(self.eb3c2_but2, span=(1, 4), pos=(4, 0), flag=wx.EXPAND)
        self.eb3c2_but2.Bind(wx.EVT_BUTTON, self.e_c2_set_range)
        # self.e_panel3_c2 = wx.Panel(self.scorePanel)
        # self.p3c2_gridsizer = wx.GridBagSizer(5, 4)
        # self.buttest3 = wx.Button(self.e_panel3_c2, 0, 'test')
        # self.buttest4 = wx.Button(self.e_panel3_c2, 0, 'test0')
        # self.p3c2_gridsizer.Add(self.buttest3, span=(1, 4), pos=(0, 0), flag=wx.EXPAND)
        # self.p3c2_gridsizer.Add(self.buttest4, pos=(4, 2), flag=wx.EXPAND)
        # self.e_panel3_c2.SetSizer(self.p3c2_gridsizer)
        # self.e_panel3_c2.Fit()

        # lt_page
        self.lt_gridsizer = wx.GridBagSizer(2, 2)
        self.scorePanel_lt.SetSizer(self.lt_gridsizer)
        # self.lt_box1 = wx.ListBox(self.scorePanel_lt,size=(800, 500))
        # self.drawHistF = Figure(figsize=(8, 5), dpi=100)
        # self.drawHistCanvas = FigureCanvas(self.lt_box1, -1, self.drawHistF)
        # self.drawHistCanvas.draw()
        self.lt_box1 = wx.ListBox(self.scorePanel_lt, size=(800, 500))
        self.lt_gridsizer.Add(self.lt_box1, pos=(0, 0), flag=wx.EXPAND)
        self.lt_box2 = wx.Panel(self.scorePanel_lt)
        self.lt_gridsizer.Add(self.lt_box2, pos=(0, 1), flag=wx.EXPAND)
        self.lt_box3 = wx.Panel(self.scorePanel_lt)
        self.lt_gridsizer.Add(self.lt_box3, span=(1, 2), pos=(1, 0), flag=wx.EXPAND)
        self.scorePanel_lt.Fit()

        self.drawHistF_lt = Figure(figsize=(8, 5), dpi=100)
        self.drawHistCanvas_lt = FigureCanvas(self.lt_box1, -1, self.drawHistF_lt)
        self.drawHistCanvas_lt.draw()

        # lt右侧区域
        # self.lt_box2 = wx.Panel(self.scorePanel, pos=(810, 0), size=(370, 500))
        # self.lt_but1 = wx.Button(self.lt_box2, 0, 'start', pos=(10, 10), size=(100, 50))
        # self.lt_but2 = wx.Button(self.lt_box2, 0, 'stop', pos=(120, 10), size=(100, 50))
        # self.lt_but3 = wx.Button(self.lt_box2, 0, 'clear', pos=(230, 10), size=(100, 50))
        # self.lt_but1.Bind(wx.EVT_BUTTON, self.start_but)
        # self.lt_but2.Bind(wx.EVT_BUTTON, self.stop_but)
        # self.lt_but3.Bind(wx.EVT_BUTTON, self.energy_clear)
        self.ltb2_gridsizer = wx.GridBagSizer(8, 3)
        self.lt_box2.SetSizer(self.ltb2_gridsizer)
        self.lt_but1 = wx.Button(self.lt_box2, -1, 'start')
        self.lt_but2 = wx.Button(self.lt_box2, -1, 'stop')
        self.lt_but3 = wx.Button(self.lt_box2, -1, 'clear')
        self.lt_but1.Bind(wx.EVT_BUTTON, self.lt_start_but)
        self.lt_but2.Bind(wx.EVT_BUTTON, self.lt_stop_but)
        self.lt_but3.Bind(wx.EVT_BUTTON, self.lt_clear)
        self.lt_cps_stext = wx.StaticText(self.lt_box2, -1, 'cps', style=wx.ALIGN_CENTER)
        self.lt_cps_stext.SetFont(self.font1)
        self.lt_cps_text = wx.TextCtrl(self.lt_box2, -1, str(self.cps), style=wx.TE_CENTER)
        self.lt_counts_stext = wx.StaticText(self.lt_box2, -1, 'counts', style=wx.ALIGN_CENTER)
        self.lt_counts_stext.SetFont(self.font1)
        self.lt_counts_text = wx.TextCtrl(self.lt_box2, -1, str(self.total_counts), style=wx.TE_CENTER)
        self.lt_but_save = wx.Button(self.lt_box2, -1, 'save')
        self.lt_but_save.Bind(wx.EVT_BUTTON, self.save_file)
        self.ltb2_gridsizer.Add(self.lt_but1, pos=(0, 0), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_but2, pos=(0, 1), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_but3, pos=(0, 2), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_cps_stext, pos=(1, 0), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_cps_text, pos=(1, 1), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_counts_stext, pos=(2, 0), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_counts_text, pos=(2, 1), flag=wx.EXPAND)
        self.ltb2_gridsizer.Add(self.lt_but_save, pos=(3, 0), flag=wx.EXPAND)
        self.lt_box2.Fit()

        # 下方区域
        self.ltb3_gridsizer = wx.GridBagSizer(1, 4)
        self.lt_box3.SetSizer(self.ltb3_gridsizer)
        self.ltb3_c1_panel = wx.Panel(self.lt_box3)
        self.ltb3_gridsizer.Add(self.ltb3_c1_panel, pos=(0, 0), flag=wx.EXPAND)
        self.ltb3_c2_panel = wx.Panel(self.lt_box3)
        self.ltb3_gridsizer.Add(self.ltb3_c2_panel, pos=(0, 1), flag=wx.EXPAND)
        # lt_c1_set
        self.ltb3c1_gridsizer = wx.GridBagSizer(7, 4)
        self.ltb3_c1_panel.SetSizer(self.ltb3c1_gridsizer)

        self.ltb3c1_title = wx.StaticText(self.ltb3_c1_panel, -1, label='start_channel', style=wx.ALIGN_CENTER)
        self.ltb3c1_title.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_title, span=(1, 5), pos=(0, 0), flag=wx.EXPAND)

        self.ltb3c1_startdown_text = wx.StaticText(self.ltb3_c1_panel, -1, 'down', style=wx.ALIGN_CENTER)
        self.ltb3c1_startdown_text.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_startdown_text, span=(1, 1), pos=(1, 0), flag=wx.EXPAND)
        self.ltb3c1_startdown = wx.TextCtrl(self.ltb3_c1_panel, -1, str(self.lt_start_l), style=wx.TE_CENTER)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_startdown, span=(1, 1), pos=(1, 1), flag=wx.EXPAND)
        self.ltb3c1_startup_text = wx.StaticText(self.ltb3_c1_panel, -1, 'up', style=wx.ALIGN_CENTER)
        self.ltb3c1_startup_text.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_startup_text, span=(1, 1), pos=(1, 2), flag=wx.EXPAND)
        self.ltb3c1_startup = wx.TextCtrl(self.ltb3_c1_panel, -1, str(self.lt_start_r), style=wx.TE_CENTER)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_startup, span=(1, 1), pos=(1, 3), flag=wx.EXPAND)
        self.ltb3c1_startfrac_text = wx.StaticText(self.ltb3_c1_panel, -1, 'fraction', style=wx.ALIGN_CENTER)
        self.ltb3c1_startfrac_text.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_startfrac_text, span=(1, 2), pos=(2, 0), flag=wx.EXPAND)
        self.ltb3c1_startfrac = wx.TextCtrl(self.ltb3_c1_panel, -1, str(self.start_fraction), style=wx.TE_CENTER)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_startfrac, span=(1, 2), pos=(2, 2), flag=wx.EXPAND)

        self.ltb3c1_title = wx.StaticText(self.ltb3_c1_panel, -1, label='stop_channel', style=wx.ALIGN_CENTER)
        self.ltb3c1_title.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_title, span=(1, 5), pos=(3, 0), flag=wx.EXPAND)

        self.ltb3c1_stopdown_text = wx.StaticText(self.ltb3_c1_panel, -1, 'down', style=wx.ALIGN_CENTER)
        self.ltb3c1_stopdown_text.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_stopdown_text, span=(1, 1), pos=(4, 0), flag=wx.EXPAND)
        self.ltb3c1_stopdown = wx.TextCtrl(self.ltb3_c1_panel, -1, str(self.lt_stop_l), style=wx.TE_CENTER)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_stopdown, span=(1, 1), pos=(4, 1), flag=wx.EXPAND)
        self.ltb3c1_stopup_text = wx.StaticText(self.ltb3_c1_panel, -1, 'up', style=wx.ALIGN_CENTER)
        self.ltb3c1_stopup_text.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_stopup_text, span=(1, 1), pos=(4, 2), flag=wx.EXPAND)
        self.ltb3c1_stopup = wx.TextCtrl(self.ltb3_c1_panel, -1, str(self.lt_stop_r), style=wx.TE_CENTER)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_stopup, span=(1, 1), pos=(4, 3), flag=wx.EXPAND)
        self.ltb3c1_stopfrac_text = wx.StaticText(self.ltb3_c1_panel, -1, 'fraction', style=wx.ALIGN_CENTER)
        self.ltb3c1_stopfrac_text.SetFont(self.font1)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_stopfrac_text, span=(1, 2), pos=(5, 0), flag=wx.EXPAND)
        self.ltb3c1_stopfrac = wx.TextCtrl(self.ltb3_c1_panel, -1, str(self.stop_fraction), style=wx.TE_CENTER)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_stopfrac, span=(1, 2), pos=(5, 2), flag=wx.EXPAND)

        self.ltb3c1_but1 = wx.Button(self.ltb3_c1_panel, -1, 'set', size=(200, 30))
        self.ltb3c1_but1.Bind(wx.EVT_BUTTON, self.lt_ch_set)
        self.ltb3c1_gridsizer.Add(self.ltb3c1_but1, span=(1, 2), pos=(6, 1), flag=wx.EXPAND)


        # lt_box3_c2
        self.ltb3c2_gridsizer = wx.GridBagSizer(7, 4)
        self.ltb3_c2_panel.SetSizer(self.ltb3c2_gridsizer)

        self.ltb3c2_title = wx.StaticText(self.ltb3_c2_panel, -1, label='lifetime_spectrum', style=wx.ALIGN_CENTER)
        self.ltb3c2_title.SetFont(self.font1)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_title, span=(1, 5), pos=(0, 0), flag=wx.EXPAND)

        self.ltb3c2_sp_left_text = wx.StaticText(self.ltb3_c2_panel, -1, 'sp_left', style=wx.ALIGN_CENTER)
        self.ltb3c2_sp_left_text.SetFont(self.font1)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_sp_left_text, span=(1, 1), pos=(1, 0), flag=wx.EXPAND)
        self.ltb3c2_sp_left = wx.TextCtrl(self.ltb3_c2_panel, -1, str(self.lt_l), style=wx.TE_CENTER)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_sp_left, span=(1, 1), pos=(1, 1), flag=wx.EXPAND)
        self.ltb3c2_sp_right_text = wx.StaticText(self.ltb3_c2_panel, -1, 'sp_right', style=wx.ALIGN_CENTER)
        self.ltb3c2_sp_right_text.SetFont(self.font1)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_sp_right_text, span=(1, 1), pos=(1, 2), flag=wx.EXPAND)
        self.ltb3c2_sp_right = wx.TextCtrl(self.ltb3_c2_panel, -1, str(self.lt_r), style=wx.TE_CENTER)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_sp_right, span=(1, 1), pos=(1, 3), flag=wx.EXPAND)
        self.ltb3c2_bins_text = wx.StaticText(self.ltb3_c2_panel, -1, 'bins', style=wx.ALIGN_CENTER)
        self.ltb3c2_bins_text.SetFont(self.font1)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_bins_text, span=(1, 2), pos=(2, 0), flag=wx.EXPAND)
        self.ltb3c2_bins = wx.TextCtrl(self.ltb3_c2_panel, -1, str(self.lt_bins), style=wx.TE_CENTER)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_bins, span=(1, 2), pos=(2, 2), flag=wx.EXPAND)
        self.ltb3c2_counts_text = wx.StaticText(self.ltb3_c2_panel, -1, 'counts', style=wx.ALIGN_CENTER)
        self.ltb3c2_counts_text.SetFont(self.font1)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_counts_text, span=(1, 2), pos=(3, 0), flag=wx.EXPAND)
        self.ltb3c2_counts = wx.TextCtrl(self.ltb3_c2_panel, -1, str(self.counts_set), style=wx.TE_CENTER)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_counts, span=(1, 2), pos=(3, 2), flag=wx.EXPAND)

        self.ltb3c2_but1 = wx.Button(self.ltb3_c2_panel, -1, 'set', size=(200, 30))
        self.ltb3c2_but1.Bind(wx.EVT_BUTTON, self.lt_sp_set)
        self.ltb3c2_gridsizer.Add(self.ltb3c2_but1, span=(1, 2), pos=(4, 1), flag=wx.EXPAND)

        # 参数
        self.m = 3.0
        self.energy_c1 = []
        self.amp_c1 = []
        self.energy_c2 = []
        self.amp_c2 = []
        self.lifetime = []
        self.wave0 = []
        self.wave1 = []
        self.lt_spe = []
        self.e_start_but = 0
        self.lt_start_but_switch = 0

    def start_but(self,event):
        if self.e_start_but == 0:
            self.dos_0.open()
            self.run_loop()
            self.e_start_but = 1

    def stop_but(self,event):
        self.dos_0.close()
        self.e_start_but = 0

    def energy_clear(self,event):
        e_c_box = wx.MessageDialog(None, u"是否真的要清除显示能谱？", u"请确认", style=wx.OK|wx.CANCEL)
        if e_c_box.ShowModal() == wx.ID_OK:
            self.energy_c1 = []
            self.amp_c1 = []
            self.energy_c2 = []
            self.amp_c2 = []
            self.drawHistF.clf()
            self.drawHistCanvas.draw()

    def lt_start_but(self, event):
        if self.e_start_but == 0:
            self.dos_0.open()
            self.run_loop_lt()
            self.e_start_but = 1

    def lt_stop_but(self, event):
        self.dos_0.close()
        self.e_start_but = 0

    def lt_clear(self, event):
        e_c_box = wx.MessageDialog(None, u"是否真的要清除显示寿命谱？", u"请确认", style=wx.OK|wx.CANCEL)
        if e_c_box.ShowModal() == wx.ID_OK:
            self.lifetime = []
            self.drawHistF_lt.clf()
            self.drawHistCanvas_lt.draw()
            self.total_counts = 0

    def e_c1_set_trlv(self,event):
        str0 = self.eb3c1_trlv.GetValue()
        self.para_0['C1_TRLV'] = float(str0)
        self.dos_0.setDSO('C1:TRLV ' + str(self.para_0['C1_TRLV']))

    def e_c1_set_range(self,event):
        str0 = float(self.eb3c1_erg_l.GetValue())
        str1 = float(self.eb3c1_erg_r.GetValue())
        str2 = float(self.eb3c1_amp_l.GetValue())
        str3 = float(self.eb3c1_amp_r.GetValue())
        if str0 >= str1 or str2 >= str3:
            e_c_box = wx.MessageBox("能谱范围左侧应小于右侧", "Error")
        else:
            self.e_rg['c1'][0] = str0
            self.e_rg['c1'][1] = str1
            self.e_rg['c1_amp'][0] = str2
            self.e_rg['c1_amp'][1] = str3

    def e_c2_set_trlv(self, event):
        str0 = self.eb3c2_trlv.GetValue()
        self.para_0['C2_TRLV'] = float(str0)
        self.dos_0.setDSO('C2:TRLV ' + str(self.para_0['C2_TRLV']))

    def e_c2_set_range(self, event):
        str0 = float(self.eb3c2_erg_l.GetValue())
        str1 = float(self.eb3c2_erg_r.GetValue())
        str2 = float(self.eb3c2_amp_l.GetValue())
        str3 = float(self.eb3c2_amp_r.GetValue())
        if str0 >= str1 or str2 >= str3:
            e_c_box = wx.MessageBox("能谱范围左侧应小于右侧", "Error")
        else:
            self.e_rg['c2'][0] = str0
            self.e_rg['c2'][1] = str1
            self.e_rg['c2_amp'][0] = str2
            self.e_rg['c2_amp'][1] = str3

    def lt_ch_set(self, event):
        str0 = float(self.ltb3c1_startdown.GetValue())
        str1 = float(self.ltb3c1_startup.GetValue())
        str2 = float(self.ltb3c1_stopdown.GetValue())
        str3 = float(self.ltb3c1_stopup.GetValue())
        str4 = float(self.ltb3c1_startfrac.GetValue())
        str5 = float(self.ltb3c1_stopfrac.GetValue())
        if str0 >= str1 or str2 >= str3 or str4 >= 1 or str4 <= 0 or str5 >= 1 or str5 <= 0:
            e_c_box = wx.MessageBox("下阈应小于上阈", "Error")
        else:
            self.lt_start_l = str0
            self.lt_start_r = str1
            self.lt_stop_l = str2
            self.lt_stop_r = str3
            self.start_fraction = str4
            self.stop_fraction = str5

    def lt_sp_set(self, event):
        str0 = float(self.ltb3c2_sp_left.GetValue())
        str1 = float(self.ltb3c2_sp_right.GetValue())
        str2 = int(self.ltb3c2_bins.GetValue())
        str3 = int(self.ltb3c2_counts.GetValue())
        if str0 >= str1 or str2 <= 0 or str3 <=0:
            e_c_box = wx.MessageBox("下阈应小于上阈", "Error")
        else:
            self.lt_l = str0
            self.lt_r = str1
            self.lt_bins = str2
            self.counts_set = str3

    def run_loop(self):
        self.th1 = threading.Thread(target=self.loop_energy_test)
        self.th1.start()

    def run_loop_lt(self):
        self.th2 = threading.Thread(target=self.loop_lifetime_test)
        self.th2.start()

    def loop_test(self):
        while self.dos_0.isOpen():
            self.drawHistF.clf()
            self.a = self.drawHistF.add_subplot(111)
            self.t = np.arange(0.0, self.m, 0.01)
            self.s = np.sin(2 * np.pi * self.t)
            self.a.plot(self.t, self.s)
            self.a.semilogy()
            self.a.set_xlim((-1.5, 10.3))
            self.a.set_xlabel('asd')
            # drawHistCanvas = FigureCanvas(box1, -1, drawHistF)
            self.drawHistCanvas.draw()
            if self.m > 10.0:
                self.m = self.m - 7
            self.m = self.m + 0.1
            time.sleep(0.01)

    def loop_energy_test(self):
        self.c_num = 0
        while self.dos_0.isOpen():
            waveform0 = self.dos_0.get_wave()
            if operator.eq(self.wave0, waveform0['c1'][1]) == False:
                if self.para_0['SEQ'] == 'ON':
                    for i in range(0,self.para_0['SEQ_N']):
                        #c1
                        t1 = tools.Wavetools(waveform0['c1'][0][i],waveform0['c1'][1][i], 800)
                        e_1 = t1.get_energy(0.2)
                        amp_1 = t1.get_amplitude()
                        self.energy_c1.append(e_1)
                        self.amp_c1.append(amp_1)
                        #c2
                        t2 = tools.Wavetools(waveform0['c2'][0][i], waveform0['c2'][1][i], 800)
                        e_2 = t2.get_energy(0.2)
                        amp_2 = t2.get_amplitude()
                        self.energy_c2.append(e_2)
                        self.amp_c2.append(amp_2)

                        self.c_num = self.c_num + 1
                else:
                    #c1
                    t1 = tools.Wavetools(waveform0['c1'][0], waveform0['c1'][1])
                    e_1 = t1.get_energy(0.2)
                    amp_1 = t1.get_amplitude()
                    self.energy_c1.append(e_1)
                    self.amp_c1.append(amp_1)
                    #c2
                    t2 = tools.Wavetools(waveform0['c2'][0][i], waveform0['c2'][1][i])
                    e_2 = t2.get_energy(0.2)
                    amp_2 = t2.get_amplitude()
                    self.energy_c2.append(e_2)
                    self.amp_c2.append(amp_2)
                    self.c_num = self.c_num + 1
                if self.c_num % 100 == 0:
                    self.drawHistF.clf()
                    #c1
                    self.a = self.drawHistF.add_subplot(221)
                    self.h_energy_c1 = self.a.hist(self.energy_c1, 150, range=(self.e_rg['c1'][0], self.e_rg['c1'][1]))
                    #self.a.set_xlabel('energy')
                    self.b = self.drawHistF.add_subplot(222)
                    self.h_amp_c1 = self.b.hist(self.amp_c1, 150,
                                                range=(self.e_rg['c1_amp'][0], self.e_rg['c1_amp'][1]))
                    #self.b.set_xlabel('amp')
                    #c2
                    self.a_c2 = self.drawHistF.add_subplot(223)
                    self.h_energy_c2 = self.a_c2.hist(self.energy_c2, 150,
                                                      range=(self.e_rg['c2'][0], self.e_rg['c2'][1]))
                    self.a_c2.set_xlabel('energy')
                    self.b_c2 = self.drawHistF.add_subplot(224)
                    self.h_amp_c2 = self.b_c2.hist(self.amp_c2, 150,
                                                   range=(self.e_rg['c2_amp'][0], self.e_rg['c2_amp'][1]))
                    self.b_c2.set_xlabel('amp')
                    #self.a.semilogy()
                    self.drawHistCanvas.draw()
            self.wave0 = waveform0['c1'][1]

    def loop_lifetime_test(self):
        self.c_num_1 = 0
        t_01 = time.time()
        while self.dos_0.isOpen():
            c_num_2 = 0
            waveform0 = self.dos_0.get_wave()
            if operator.eq(self.wave1, waveform0['c1'][1]) == False:
                if self.para_0['SEQ'] == 'ON':
                    for i in range(0, self.para_0['SEQ_N']):
                        # c1
                        t1 = tools.Wavetools(waveform0['c1'][0][i], waveform0['c1'][1][i])
                        e_1 = t1.get_energy(0.2)
                        amp_1 = t1.get_amplitude()

                        # c2
                        t2 = tools.Wavetools(waveform0['c2'][0][i], waveform0['c2'][1][i])
                        e_2 = t2.get_energy(0.2)
                        amp_2 = t2.get_amplitude()
                        self.c_num_1 = self.c_num_1 + 1

                        if e_1 > self.lt_start_l and e_1 < self.lt_start_r \
                                and e_2 > self.lt_stop_l and e_2 < self.lt_stop_r :
                            t_start = t1.get_time_cfd_linear(self.start_fraction)
                            t_stop = t2.get_time_cfd_linear(self.stop_fraction)
                            self.lifetime.append(t_stop - t_start)
                            #print(t_stop - t_start)
                            c_num_2 = c_num_2 + 1
                            self.total_counts = self.total_counts + 1

                else:
                    # c1
                    t1 = tools.Wavetools(waveform0['c1'][0], waveform0['c1'][1])
                    e_1 = t1.get_energy(0.2)
                    amp_1 = t1.get_amplitude()

                    # c2
                    t2 = tools.Wavetools(waveform0['c2'][0], waveform0['c2'][1])
                    e_2 = t2.get_energy(0.2)
                    amp_2 = t2.get_amplitude()

                    self.c_num_1 = self.c_num_1 + 1
                    if e_1 > self.lt_start_l and e_1 < self.lt_start_r and e_2 > self.lt_stop_l \
                            and e_2 < self.lt_stop_r:
                        t_start = t1.get_time_cfd_linear(self.start_fraction)
                        t_stop = t2.get_time_cfd_linear(self.stop_fraction)
                        self.lifetime.append(t_stop - t_start)
                        c_num_2 = c_num_2 + 1
                        self.total_counts = self.total_counts + 1
                if self.c_num_1 % 1000 == 0:
                    self.drawHistF_lt.clf()
                    self.a_lt = self.drawHistF_lt.add_subplot(111)
                    self.h_lifetime = self.a_lt.hist(self.lifetime, self.lt_bins, range=(self.lt_l, self.lt_r))
                    self.a_lt.semilogy()
                    self.drawHistCanvas_lt.draw()
                t_02 = time.time()
                self.cps = c_num_2/(t_02 - t_01)
                self.lt_cps_text.SetValue(str(int(self.cps)))
                self.lt_counts_text.SetValue(str(self.total_counts))
                t_01 = time.time()

            self.wave1 = waveform0['c1'][1]
            if self.total_counts > self.counts_set:
                break

    def save_file(self, event):
        '''
        保存文件内容
        与菜单中的保存选项绑定
        '''
        self.dir_name = ''
        fd = wx.FileDialog(self, '把文件保存到何处', self.dir_name,
                'out1.txt', 'TEXT file(*.txt)|*.txt', wx.FD_SAVE)
        if fd.ShowModal() == wx.ID_OK:
            self.file_name = fd.GetFilename()
            self.dir_name = fd.GetDirectory()
            try:
                with open(os.path.join(self.dir_name, self.file_name), 'w', encoding='utf-8') as f:
                    text = plt.hist(self.lifetime, self.lt_bins, range=(self.lt_l, self.lt_r))
                    f.write('bin_width: ' + str((self.lt_r - self.lt_l)/self.lt_bins) + '\n')
                    for i in range(0, len(text[0])):
                        f.write(str(int(text[0][i])) + '\n')
                    save_msg = wx.MessageDialog(self, '文件已保存', '提示')
            except FileNotFoundError:
                save_msg = wx.MessageDialog(self, '保存失败,无效的保存路径', '提示')
        else:
            save_msg = wx.MessageDialog(self, '未选择保存路径', '错误')

        save_msg.ShowModal()
        save_msg.Destroy()


if __name__ == '__main__':
    matplotlib.use("WXAgg")
    app = wx.App()
    myframe = myFrame()
    myframe.Show()
    app.MainLoop()