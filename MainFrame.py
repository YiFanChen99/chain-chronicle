# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import tkMessageBox
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel


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
        MainFrame.__init__(self, master, db_suffix, **kwargs)

        # init table
        self.table = Frame(self)
        self.table.place(x=34, y=29)
        self.table_view = TableView(self.table)
        self.table_view.bind("<Double-Button-1>", self.do_double_clicking)  # 雙擊事件註冊
        self.table_view.handle_drag_along_right = self.do_dragging_along_right  # Mouse Release 事件註冊
        self.table_model = None

    # Template Method
    def do_double_clicking(self, event):
        pass

    # Template Method
    def do_dragging_along_right(self, row_number):
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
        MainFrame.destroy(self)


class TableView(TableCanvas):
    def __init__(self, master, **kwargs):
        TableCanvas.__init__(self, master, editable=False, rowheaderwidth=0, cellwidth=50, **kwargs)
        self.unbind_all("<Delete>")  # 刪除
        self.unbind_all('<Return>')  # Enter

    # 選中的 cells 不需要黃色高亮
    def drawSelectedRect(self, row, col, color=None):
        pass

    # 判斷 Mouse Releasing 時是否為 drag-along right
    def handle_left_release(self, event):
        self.endrow = self.get_row_clicked(event)
        self.endcol = self.get_col_clicked(event)

        if self.startrow == self.endrow and self.startcol < self.endcol:
            self.handle_drag_along_right(self.endrow)

    # For overwriting
    def handle_drag_along_right(self, row_number):
        pass