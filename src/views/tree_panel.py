import wx
import wx.lib.agw.customtreectrl as CT


class NodeTreeCtrl(CT.CustomTreeCtrl):
    def __init__(self, parent, *args, **kw):
        style = (CT.TR_DEFAULT_STYLE | CT.TR_MULTIPLE | CT.TR_FULL_ROW_HIGHLIGHT |
                 CT.TR_AUTO_CHECK_CHILD | CT.TR_AUTO_CHECK_PARENT | CT.TR_AUTO_TOGGLE_CHILD)
        super().__init__(parent, wx.ID_ANY, size=wx.Size(900, 350), agwStyle=style)
        root = self.AddRoot("Root", ct_type=1)

        image_list = wx.ImageList(16, 16)
        img_folder = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        img_folder_open = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(16, 16)))
        img_file = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))

        self.SetImageList(image_list)

        self.SetItemImage(root, img_folder, wx.TreeItemIcon_Normal)
        self.SetItemImage(root, img_folder_open, wx.TreeItemIcon_Expanded)

        for x in range(15):
            child = self.AppendItem(root, "Item %d" % x, ct_type=1)
            self.SetItemImage(child, img_folder, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, img_folder_open, wx.TreeItemIcon_Expanded)

            for y in range(5):
                last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=1)
                self.SetItemImage(last, img_folder, wx.TreeItemIcon_Normal)
                self.SetItemImage(last, img_folder_open, wx.TreeItemIcon_Expanded)

                for z in range(5):
                    item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
                    self.SetItemImage(item, img_file, wx.TreeItemIcon_Normal)

    def get_checked_items(self, parent=None, checked_items=None):
        if parent is None:
            parent = self.GetRootItem()
        if checked_items is None:
            checked_items = []
        child, _ = self.GetFirstChild(parent)
        while child:
            if self.IsItemChecked(child):
                checked_items.append(child)
            checked_items = self.get_checked_items(child, checked_items)
            child, _ = self.GetNextChild(parent, _)
        return checked_items

    def get_selected_items(self, parent=None, selected_items=None):
        if parent is None:
            parent = self.GetRootItem()
        if selected_items is None:
            selected_items = []
        child, _ = self.GetFirstChild(parent)
        while child:
            if self.IsSelected(child):
                selected_items.append(child)
            selected_items = self.get_checked_items(child, selected_items)
            child, _ = self.GetNextChild(parent, _)
        return selected_items

    def check_selected_items(self, parent=None):
        if parent is None:
            parent = self.GetRootItem()
        child, _ = self.GetFirstChild(parent)
        while child:
            if self.IsSelected(child):
                self.SetItem3StateValue(child, wx.CHK_CHECKED)
                self.SelectAllChildren(child)
            self.check_selected_items(child)
            child, _ = self.GetNextChild(parent, _)

    def uncheck_selected_items(self, parent=None):
        if parent is None:
            parent = self.GetRootItem()
        child, _ = self.GetFirstChild(parent)
        while child:
            if self.IsSelected(child):
                self.SetItem3StateValue(child, wx.CHK_UNCHECKED)
                self.SelectAllChildren(child)
            self.uncheck_selected_items(child)
            child, _ = self.GetNextChild(parent, _)


class TreePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.custom_tree = NodeTreeCtrl(self)

        btn_show_checked = wx.Button(self, label="Show Checked Items")
        btn_show_checked.Bind(wx.EVT_BUTTON, self.get_checked_items)
        btn_check = wx.Button(self, label="[+] Check selected Items")
        btn_check.Bind(wx.EVT_BUTTON, self.check_selected_items)
        btn_uncheck = wx.Button(self, label="[-] Uncheck selected Items")
        btn_uncheck.Bind(wx.EVT_BUTTON, self.uncheck_selected_items)

        btn_layout = wx.BoxSizer(wx.HORIZONTAL)
        btn_layout.Add(btn_show_checked, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        btn_layout.Add(btn_check, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        btn_layout.Add(btn_uncheck, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(btn_layout, proportion=0, flag=wx.ALL | wx.EXPAND, border=5)
        layout.Add(self.custom_tree, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        self.SetSizer(layout)

    def get_checked_items(self, event):
        checked_items = self.custom_tree.get_checked_items()
        for item in checked_items:
            print(item.GetText())

    def check_selected_items(self, event):
        self.custom_tree.check_selected_items()
        self.custom_tree.UnselectAll()

    def uncheck_selected_items(self, event):
        self.custom_tree.uncheck_selected_items()
        self.custom_tree.UnselectAll()
