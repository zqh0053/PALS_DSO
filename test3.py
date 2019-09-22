# import wx
# class cjlists(wx.Panel):
#     def __init__(self,parent):
#         wx.Panel.__init__(self, parent)
#         wx.StaticText(self,label='Absolute Positioning1')
#         pass
#
# class cjview(wx.Panel):
#     def __init__(self,parent):
#         wx.Panel.__init__(self, parent)
#         wx.StaticText(self,label='Page Two2')
#         pass
#
# class cjsave(wx.Panel):
#     def __init__(self,parent):
#         wx.Panel.__init__(self, parent)
#         wx.StaticText(self,label='Page Three3')
#         pass
#
# if __name__ == '__main__':
#     app = wx.App(False)
#     frame = wx.Frame(None, title="Demo with Notebook")
#     nb = wx.Notebook(frame)
#     nb.AddPage(cjlists(nb), "Absolute Positioning")
#     nb.AddPage(cjview(nb), "Page Two")
#     nb.AddPage(cjsave(nb), "Page Three")
#     frame.Show()
#     app.MainLoop()
#     pass

import numpy as np
import json

data_test = []
for i in range(0, 10000000):
    data_0 = {'sd': 0.1 * i, 'qw': 'qwe'}
    data_test.append(data_0)
# data_json = json.dumps(data_test)
# with open("../a.json","w") as f:
#     json.dump(data_json, f)
print('123')
prompt = "\nEnter 'quit'\n"
message = ''
while message != 'quit':
    message = input(prompt)
    print(message)