# import numpy as np
# from numpy.linalg import cholesky
# import tools as tl1
# import matplotlib.pyplot as plt
# import time
# sampleNo = 1000000
# mu = 85
# sigma = 4
# np.random.seed(0)
# s = np.random.normal(mu, sigma, sampleNo)
# t0_1 = time.time()
# #h1 = plt.hist(s, 300,range=(0, 300))
# c = [-10,-5,0,5,3,10,15,-20,25]
# b = [10,23,20]
# d = [c,b]
# print(d)
# print(c.index(-10))
# print(d[1][1])
# t0_2 = time.time()
# print(t0_2 - t0_1)
# tm1 = (0.01, 0.02)
# tm5 = tuple(c)
# print(tm5)
# tm2 = np.array(tm1)
# tm3 = -1. * tm2
# print(tm3)
# # = h1[0].tolist()
# filename1 = 'C2--C1C2_1200M--00000.csv'
# k = 0
# time_1 = []
# volt_1 = []
# with open(filename1) as file1_object:
#     for lines in file1_object:
#         if k < 5:
#             k = k + 1
#         else:
#             line = lines.rstrip().split(',')
#             time_1.append(1000000000 * float(line[0]))
#             volt_1.append(float(line[1]))
# # print(time_1)
#
# tr1 = tl1.Wavetools(time_1, volt_1, basenum=9000)
# print(tr1.find_baseline())
# t_0 = time.time()
# print(tr1.get_time_cfd_linear(0.2))
#
# print(tr1.get_time_cfd_poln(0.2, 4, 0.4))
# t_1 = time.time()
# print(t_1 - t_0)
# print(tr1.get_slope())
# l1 = plt.plot(time_1, volt_1)
# plt.show()
#
# str1 = 'asd'
# str2 = 1
# str3 = "asd " + str(str2)
# print(str3)

import wx
import os

# class MainWindow(wx.Frame):
#     def __init__(self, parent, title, size=(600, 400)):
#         wx.Frame.__init__(self, parent=parent, title=title, size=size)
#
#         # 文本编辑框
#         self.text_control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#
#         # 菜单
#         file_menu = wx.Menu()
#         file_menu_save = file_menu.Append(wx.ID_SAVE, '保存', '保存文件内容')
#         menu_bar = wx.MenuBar()
#         menu_bar.Append(file_menu, '文件')
#         self.SetMenuBar(menu_bar)
#
#         # 状态栏
#         self.CreateStatusBar()
#
#         # 新内容
#         # 新内容添加了事件处理功能
#         # Bind()把事件与时间处理方法绑定
#         self.Bind(wx.EVT_MENU, self.save_file, file_menu_save)
#
#         self.Show()
#
#     def save_file(self, event):
#         '''
#         保存文件内容
#         与菜单中的保存选项绑定
#         '''
#         self.dir_name = ''
#         fd = wx.FileDialog(self, '把文件保存到何处', self.dir_name,
#                 '.txt', 'TEXT file(*.txt)|*.txt', wx.FD_SAVE)
#         if fd.ShowModal() == wx.ID_OK:
#             self.file_name = fd.GetFilename()
#             self.dir_name = fd.GetDirectory()
#             try:
#                 with open(os.path.join(self.dir_name, self.file_name), 'w', encoding='utf-8') as f:
#                     text = self.text_control.GetValue()
#                     f.write(text)
#                     save_msg = wx.MessageDialog(self, '文件已保存', '提示')
#             except FileNotFoundError:
#                 save_msg = wx.MessageDialog(self, '保存失败,无效的保存路径', '提示')
#         else:
#             save_msg = wx.MessageDialog(self, '未选择保存路径', '错误')
#
#         save_msg.ShowModal()
#         save_msg.Destroy()
#
#
# app = wx.App()
# main_window = MainWindow(None, '文本编辑器')
# app.MainLoop()

###拟合年龄

# import numpy as np
# import matplotlib.pyplot as plt
# import time
#
# #定义x、y散点坐标
# x = [10,20,30]
# x = np.array(x)
# print('x is :\n',x)
# num = [174,236,305]
# y = np.array(num)
# print('y is :\n',y)
# t_0 = time.time()
# #用3次多项式拟合
# f1 = np.polyfit(x, num, 4)
# print('f1 is :\n',f1)
# print(f1[0])
#
# p1 = np.poly1d(f1)
# print('p1 is :\n',p1)
# #也可使用yvals=np.polyval(f1, x)
# yvals = p1(x)  #拟合y值
# t_1 = time.time()
# print(t_1 - t_0)
# y33 = p1(x[0])
# print('yvals is :\n',yvals)
# print(y33)
# #绘图
# plot1 = plt.plot(x, y, 's',label='original values')
# plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend(loc=4) #指定legend的位置右下角
# plt.title('polyfitting')
# plt.show()

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19601)
data = np.random.randn(2, 100)

fig, axs = plt.subplots(2, 2, figsize=(5, 5))
axs[0, 0].hist(data[0])
axs[1, 0].scatter(data[0], data[1])
axs[0, 1].plot(data[0], data[1])
axs[1, 1].hist2d(data[0], data[1])

plt.show()