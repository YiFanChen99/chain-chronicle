# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from BaseTab import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import UpdateCharacterWindow

# Character 表格中的各欄位
COLUMNS = ['Character', 'FullName', 'Profession', 'Rank', 'Note',
           'Active', 'ActiveCost', 'Passive1', 'Passive2', 'WeaponType',
           'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown',
           'HPGrown', 'AtkSpeed', 'WalkSpeed', 'CriticalRate']


class Character(BaseTab):
    def __init__(self, parent=None):
        BaseTab.__init__(self, parent)

        # 新增記錄的按鈕
        button = Button(self, text="新增角色資訊", width=2, height=21, wraplength=1, font=14)
        button.place(x=5, y=5)
        button["command"] = self.do_add_character

        # 呈現資料的表格
        self.update_table()

    # TODO 未完成
    def do_add_character(self):
        print 'add character'
        popup = UpdateCharacterWindow.UpdateCharacterWindow(self)
        self.wait_window(popup)

    # noinspection PyAttributeOutsideInit
    def update_table(self):
        self.table = Frame(self)
        self.table.place(x=35, y=7)
        self.table_model = TableModel()
        self.table_view = TableCanvas(self.table, model=self.table_model, width=655,
                                      height=303, rowheaderwidth=0, cellwidth=50, editable=False)
        self.table_view.createTableFrame()

        for column in COLUMNS:
            self.table_model.addColumn(column)

        result = self.execute('select * from Character')
        for row in result:
            self.table_model.addRow(Character=BaseTab.convert_to_str(row[0]),
                                    Profession=BaseTab.convert_to_str(row[2]), Rank=row[3],
                                    Note=BaseTab.convert_to_str(row[4]),
                                    Active=BaseTab.convert_to_str(row[5]), ActiveCost=row[6],
                                    Passive1=BaseTab.convert_to_str(row[7]),
                                    WeaponType=BaseTab.convert_to_str(row[9]),
                                    ExpGrown=BaseTab.convert_to_str(row[10]), AttendanceCost=row[11],
                                    MaxAtk=row[12], MaxHP=row[13], AtkGrown=row[14], HPGrown=row[15],
                                    AtkSpeed=row[16], WalkSpeed=row[17], CriticalRate=row[18])

        self.table_model.setSortOrder(columnName=COLUMNS[3], reverse=1)
        self.table_model.setSortOrder(columnName=COLUMNS[2])
        self.table_view.adjustColumnWidths()
        self.table_view.redrawTable()