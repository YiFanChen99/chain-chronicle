# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
import ttk
import tkMessageBox
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from ModelUtility.CommonString import *

MIN_WIDTH = 760
MIN_HEIGHT = 460


class MainFrame(Frame):
    def __init__(self, master, db_suffix=None, width=MIN_WIDTH, height=MIN_HEIGHT, **kwargs):
        self.db_suffix = db_suffix
        Frame.__init__(self, master, width=width, height=height, **kwargs)
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
        self.table_x = None
        self.table_y = None
        self.table = Frame(self)
        self.table_view = TableView(self.table)
        self.table_view.bind("<Double-Button-1>", self.do_double_clicking)  # 雙擊事件註冊
        self.table_view.handle_drag_along_right = self.do_dragging_along_right  # Mouse Release 事件註冊
        self.table_model = None

    # set table place, and record it for adjusting frame size
    def set_table_place(self, x, y):
        self.table.place(x=x, y=y)
        self.table_x = x
        self.table_y = y

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
        self.table_view['width'] = width - 93 + self.table_x
        self.table_view['height'] = height - 104 + self.table_y


class TableView(TableCanvas):
    def __init__(self, master, **kwargs):
        TableCanvas.__init__(self, master, editable=False, rowheaderwidth=0, cellwidth=60, **kwargs)
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

    # 不知為何該 method 有更新 cols 的程式碼卻被註解掉，
    # 此會造成預設 cols 與 model 行數不同的錯誤，以此修正
    def adjustColumnWidths(self):
        self.cols = self.model.getColumnCount()
        TableCanvas.adjustColumnWidths(self)

    def hide_column(self, col_name):
        # 這邊為了隱藏欲把寬度設為 0, 但會影響 get_clicked 事件的正確性, 故調成極小的寬度
        tiny_width = 0.05

        # 底下照抄 TableCanvas.resizeColumn 的內容
        self.model.columnwidths[col_name] = tiny_width
        self.setColPositions()
        self.redrawTable()
        self.drawSelectedCol(self.currentcol)