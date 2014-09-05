# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
from tkintertable.Tables import TableCanvas


class MainFrame(Frame):
    def __init__(self, master, db_suffix=None, **kwargs):
        self.db_suffix = db_suffix
        Frame.__init__(self, master, **kwargs)
        self.pack(fill=BOTH, expand=1)

    def adjust_size(self, width, height):
        self['width'] = width
        self['height'] = height

    def compose_table_name(self, table_name):
        return table_name + self.db_suffix


class MainFrameWithTable(MainFrame):
    def __init__(self, master, db_suffix=None, **kwargs):
        MainFrame.__init__(self, master, db_suffix , **kwargs)

        # init table
        self.table = Frame(self)
        self.table.place(x=34, y=29)
        self.table_view = TableCanvas(self.table, rowheaderwidth=0, cellwidth=50, editable=False)
        self.table_view.bind("<Double-Button-1>", self.do_double_clicking)  # 雙擊事件註冊
        # noinspection PyPep8Naming
        self.table_view.deleteCells = doing_nothing  # 按下 Delete 鍵時不做反應
        self.table_model = None

    # Template Method
    def do_double_clicking(self, event):
        pass

    def redisplay_table(self):
        self.table_view.setModel(self.table_model)
        self.table_view.createTableFrame()
        self.table_view.redrawTable()
        self.table_view.adjustColumnWidths()

    def adjust_size(self, width, height):
        MainFrame.adjust_size(self, width, height)
        self.table_view['width'] = width - 59
        self.table_view['height'] = height - 75

    def destroy(self):
        self.table_view.unbind_all('<Return>')  # 不知為何靠 destroy 無法清除，手動解除
        MainFrame.destroy(self)
