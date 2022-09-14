
import ctypes
import sys

import wx
import wx.lib.agw.customtreectrl as CT

from views.tree_panel import TreePanel
from views.stdout_panel import StdoutPanel

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="ApplicationTitle", size=(900, 600))
        self.__set_layout()

    def __set_layout(self):
        root_layout = wx.SplitterWindow(self)
        notebook = wx.Notebook(root_layout, wx.ID_ANY)
        tree_panel = TreePanel(notebook)
        notebook.InsertPage(0, tree_panel, 'Tree')
        stdout_panel = StdoutPanel(root_layout)
        root_layout.SplitHorizontally(notebook, stdout_panel, 400)  # ウィンドウを左右に分割
        root_layout.SetMinimumPaneSize(1)


class Application(wx.App):
    def OnInit(self):
        frame = MainFrame()
        print('init')
        frame.SetBackgroundColour(wx.NullColour)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


if __name__ == '__main__':
    print('Main')
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass
    app = Application()
    app.MainLoop()
