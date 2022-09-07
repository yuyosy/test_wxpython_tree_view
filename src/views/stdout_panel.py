import sys

import wx


class StdoutPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        std_field_label = wx.StaticText(self, id=wx.ID_ANY, label='Console output')
        self.std_field = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        sys.stdout = self
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(std_field_label, proportion=0, flag=wx.LEFT | wx.RIGHT, border=10)
        layout.Add(self.std_field, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(layout)

    def write(self, msg):
        self.std_field.AppendText(msg)

    def flush(self):
        pass
