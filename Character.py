# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import UpdateCharacterWindow

# Character 表格中的各欄位
COLUMNS = ['Character', 'FullName', 'Profession', 'Rank', 'Note',
           'Active', 'ActiveCost', 'Passive1', 'Passive2', 'WeaponType',
           'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown',
           'HPGrown', 'AtkSpeed', 'WalkSpeed', 'CriticalRate']


class Character(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

        # 新增記錄的按鈕
        button = Button(self, text="新增角色資訊", width=2, height=22, wraplength=1, font=("", 12))
        button.place(x=5, y=13)
        button["command"] = self.do_add_character

        # 呈現資料的表格
        self.table_model = None
        self.__init_table()

    # noinspection PyAttributeOutsideInit
    def __init_table(self):
        self.table = Frame(self)
        self.table.place(x=35, y=7)
        self.table_view = TableCanvas(self.table, rowheaderwidth=0, cellwidth=50, editable=False)
        self.table_view.bind("<Double-Button-1>", self.do_double_click)
        # noinspection PyPep8Naming
        self.table_view.deleteCells = do_nothing  # 按下 Delete 鍵時不做反應

        self.update_table()

    def update_table(self):
        self.table_model = TableModel()

        for column in COLUMNS:
            if column != 'FullName':
                self.table_model.addColumn(column)

        result = DATABASE.execute('select * from Character')
        for row in result:
            self.table_model.addRow(Character=convert_to_str(row[0]),
                                    Profession=convert_to_str(row[2]), Rank=row[3],
                                    Note=convert_to_str(row[4]),
                                    Active=convert_to_str(row[5]), ActiveCost=row[6],
                                    Passive1=convert_to_str(row[7]), Passive2=convert_to_str(row[8]),
                                    WeaponType=convert_to_str(row[9]),
                                    ExpGrown=convert_to_str(row[10]), AttendanceCost=row[11],
                                    MaxAtk=row[12], MaxHP=row[13], AtkGrown=row[14], HPGrown=row[15],
                                    AtkSpeed=row[16], WalkSpeed=row[17], CriticalRate=row[18])

        self.table_model.setSortOrder(columnName=COLUMNS[3], reverse=1)
        self.table_model.setSortOrder(columnName=COLUMNS[2])

        self.table_view.setModel(self.table_model)
        self.table_view.createTableFrame()
        self.table_view.redrawTable()
        self.table_view.adjustColumnWidths()

    def do_add_character(self):
        popup = UpdateCharacterWindow.UpdateCharacterWindow(self)
        self.wait_window(popup)
        self.update_table()

    def do_double_click(self, event):
        row = self.table_view.get_row_clicked(event)
        character = self.table_model.getCellRecord(row, 0)

        popup = UpdateCharacterWindow.UpdateCharacterWindow(self, character)
        self.wait_window(popup)
        self.update_table()

    def adjust_view(self, width, height):
        self.table_view['width'] = width - 59
        self.table_view['height'] = height - 51
