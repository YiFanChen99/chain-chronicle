# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from ModelUtility.CommonString import *


class MainFrame(Frame):
    def __init__(self, master, width=MIN_WIDTH, height=MIN_HEIGHT, **kwargs):
        Frame.__init__(self, master, width=width, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)

    def adjust_size(self, width, height):
        self['width'] = width
        self['height'] = height


class MainFrameWithTable(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

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

    def redisplay_table(self, is_reset_model=False):
        if is_reset_model:
            self.table_view.setModel(self.table_model)
        self.table_view.createTableFrame()
        self.table_view.redrawTable()
        self.table_view.adjustColumnWidths()

    def adjust_size(self, width, height):
        MainFrame.adjust_size(self, width, height)
        self.table_view['width'] = width - self.table_x - 25
        self.table_view['height'] = height - self.table_y - 45


class TableView(TableCanvas):
    def __init__(self, master, **kwargs):
        TableCanvas.__init__(self, master, editable=False, rowheaderwidth=0, cellwidth=60, **kwargs)
        # 取消其預設的事件
        self.unbind_all("<Delete>")
        self.unbind_all('<Return>')
        self.unbind_all('<Control-x>')
        self.unbind_all('<Control-c>')
        self.unbind_all('<Control-v>')

    # 選中的 cells 不需要黃色高亮
    def drawSelectedRect(self, row, col, color=None):
        pass

    # 判斷 Mouse Releasing 時是否為 drag-along right
    def handle_left_release(self, event):
        self.endrow = self.get_row_clicked(event)
        self.endcol = self.get_col_clicked(event)

        if self.startrow == self.endrow and self.startcol < self.endcol:
            self.handle_drag_along_right(self.endrow)

    # For overriding
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


class TableModelAdvance(TableModel):
    def __init__(self, **kwargs):
        TableModel.__init__(self, **kwargs)
        self.main_column = ''

    # 清空原有的欄位，並依據給予的欄位重新設定。並設定無資料時提示文字顯示在哪欄
    def set_columns(self, columns, main_column=None):
        self.deleteColumns()
        for col in columns:
            TableModel.addColumn(self, col)

        self.main_column = columns[0] if main_column is None else main_column

    # 清空原有的記錄，並依據給予的記錄重新設定
    def set_rows(self, rows):
        self.deleteRows()

        if len(rows) == 0:
            self.addRow(**{self.main_column: '無任何記錄'})
            return

        row_number = 0
        for i in range(len(rows)):
            row_number += 1
            self.data[row_number] = dict(zip(self.columnNames, rows[i]))
            self.reclist.append(row_number)
