# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from OldStatic import *
import RecordsFilter
import ttk
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import UpdateCharacterWindow

# Character 表格中的各欄位
COLUMNS = ['Character', 'FullName', 'Profession', 'Rank', 'Note',
           'Active', 'ActiveCost', 'Passive1', 'Passive2', 'WeaponType',
           'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown',
           'HPGrown', 'AtkSpeed', 'WalkSpeed', 'CriticalRate']


class Character(Frame):
    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.pack(fill=BOTH, expand=1)

        self.__init_filter_frame()
        # 新增記錄的按鈕
        button = Button(self, text="新增角色資訊", width=2, height=17, wraplength=1, font=(MS_JH, 12))
        button.place(x=5, y=39)
        button["command"] = self.do_add_character

        self.records_filter = RecordsFilter.RecordsFilter('select * from Character')

        # 呈現資料的表格
        self.table_model = None
        self.__init_table()

    def __init_filter_frame(self):
        basic_x = 60
        Label(self, text='P:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.profession_selector = ttk.Combobox(self, state='readonly', width=7, justify=CENTER)
        self.profession_selector['values'] = insert_with_empty_str(PROFESSIONS)
        self.profession_selector.place(x=basic_x + 18, y=5)
        self.profession_selector.bind('<<ComboboxSelected>>', self.do_update_table)

        basic_x = 176
        Label(self, text='R:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.rank_selector = ttk.Combobox(self, state='readonly', width=4, justify=CENTER)
        self.rank_selector['values'] = insert_with_empty_str(RANKS)
        self.rank_selector.place(x=basic_x + 18, y=5)
        self.rank_selector.bind('<<ComboboxSelected>>', self.do_update_table)

        basic_x = 268
        Label(self, text='AC:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.active_cost_selector = ttk.Combobox(self, state='readonly', width=4, justify=CENTER)
        self.active_cost_selector['values'] = insert_with_empty_str(ACTIVE_COST)
        self.active_cost_selector.place(x=basic_x + 30, y=5)
        self.active_cost_selector.bind('<<ComboboxSelected>>', self.do_update_table)

        basic_x = 373
        Label(self, text='W:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.weapon_selector = ttk.Combobox(self, state='readonly', width=5, justify=CENTER)
        self.weapon_selector['values'] = insert_with_empty_str(WEAPONS)
        self.weapon_selector.place(x=basic_x + 24, y=5)
        self.weapon_selector.bind('<<ComboboxSelected>>', self.do_update_table)

        # 清空進行篩選的條件
        button = Button(self, text="清空條件", width=7, font=(MS_JH, 11))
        button.place(x=605, y=0)
        button["command"] = self.do_clear_filter

    def do_clear_filter(self):
        self.profession_selector.set('')
        self.rank_selector.set('')
        self.active_cost_selector.set('')
        self.weapon_selector.set('')
        self.do_update_table()

    # noinspection PyAttributeOutsideInit
    def __init_table(self):
        self.table = Frame(self)
        self.table.place(x=35, y=30)
        self.table_view = TableCanvas(self.table, rowheaderwidth=0, cellwidth=50, editable=False)
        self.table_view.bind("<Double-Button-1>", self.do_double_click)
        # noinspection PyPep8Naming
        self.table_view.deleteCells = do_nothing  # 按下 Delete 鍵時不做反應

        self.do_update_table()

    # noinspection PyUnusedLocal
    def do_update_table(self, event=None):
        self.table_model = TableModel()

        for column in COLUMNS:
            if column != 'FullName' and column != 'Note':
                self.table_model.addColumn(column)

        self.__update_filters()
        results = self.records_filter.filtered_records
        if len(results) == 0:
            self.table_model.addRow(Character='無任何記錄')
        for row in results:
            self.table_model.addRow(Character=convert_to_str(row[0]),
                                    Profession=convert_to_str(row[2]), Rank=row[3],
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

    def __update_filters(self):
        self.records_filter.clear_filters()

        # 依序對職業、等級、技能花費、武器類型進行篩選(if需要)
        profession = self.profession_selector.get()
        if profession != '':
            self.records_filter.add_filter(2, profession)
        rank = self.rank_selector.get()
        if rank != '':
            self.records_filter.add_filter(3, int(rank))
        active_cost = self.active_cost_selector.get()
        if active_cost != '':
            self.records_filter.add_filter(6, int(active_cost))
        weapon = self.weapon_selector.get()
        if weapon != '':
            self.records_filter.add_filter(9, weapon)

    def do_add_character(self):
        popup = UpdateCharacterWindow.UpdateCharacterWindow(self)
        self.wait_window(popup)
        self.records_filter.update_raw_records()
        self.do_update_table()

    def do_double_click(self, event):
        row = self.table_view.get_row_clicked(event)
        character = self.table_model.getCellRecord(row, 0)

        popup = UpdateCharacterWindow.UpdateCharacterWindow(self, character)
        self.wait_window(popup)
        self.do_update_table()

    def adjust_view(self, width, height):
        self.table_view['width'] = width - 59
        self.table_view['height'] = height - 75
