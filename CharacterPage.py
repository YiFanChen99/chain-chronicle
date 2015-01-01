# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *
from Window.CharacterWindow import CharacterInfoWindow
import Utilities

TABLE = CHARACTER_DB_TABLE


class Character(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(34, 29)

        # 新增記錄的按鈕
        button = Button(self, text="新增角色資訊", width=2, height=17, wraplength=1, font=(MS_JH, 12))
        button.place(x=4, y=23)
        button["command"] = self.adding_character

        self.__init_filter_frame()

        self.records_filter = Utilities.RecordsFilter('select * from Character')

        self.updating_table()

    def __init_filter_frame(self):
        basic_y = 3
        basic_x = 55
        Label(self, text='P:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.profession_selector = ttk.Combobox(self, state='readonly', width=7, justify=CENTER)
        self.profession_selector['values'] = insert_with_empty_str(PROFESSIONS)
        self.profession_selector.place(x=basic_x + 18, y=basic_y)
        self.profession_selector.bind('<<ComboboxSelected>>', self.updating_table)

        basic_x += 107
        Label(self, text='R:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.rank_selector = ttk.Combobox(self, state='readonly', width=4, justify=CENTER)
        self.rank_selector['values'] = insert_with_empty_str(RANKS)
        self.rank_selector.place(x=basic_x + 18, y=basic_y)
        self.rank_selector.bind('<<ComboboxSelected>>', self.updating_table)

        basic_x += 86
        Label(self, text='AC:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.active_cost_selector = ttk.Combobox(self, state='readonly', width=4, justify=CENTER)
        self.active_cost_selector['values'] = insert_with_empty_str(ACTIVE_COST)
        self.active_cost_selector.place(x=basic_x + 30, y=basic_y)
        self.active_cost_selector.bind('<<ComboboxSelected>>', self.updating_table)

        basic_x += 98
        Label(self, text='W:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.weapon_selector = ttk.Combobox(self, state='readonly', width=5, justify=CENTER)
        self.weapon_selector['values'] = insert_with_empty_str(WEAPONS)
        self.weapon_selector.place(x=basic_x + 24, y=basic_y)
        self.weapon_selector.bind('<<ComboboxSelected>>', self.updating_table)

        # 角色部分名稱篩選
        basic_x = 470
        Label(self, text='篩選:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y - 1)
        self.queried_name = StringVar()
        entry = Entry(self, width=8, textvariable=self.queried_name, font=(MS_JH, 11))
        entry.place(x=basic_x + 42, y=basic_y + 1)
        entry.bind('<Return>', self.updating_table)

        # 清空進行篩選的條件
        button = Button(self, text="清空條件", width=7, font=(MS_JH, 11))
        button.place(x=640, y=-1)
        button["command"] = self.clearing_filter

    def clearing_filter(self):
        self.profession_selector.set('')
        self.rank_selector.set('')
        self.active_cost_selector.set('')
        self.weapon_selector.set('')
        self.queried_name.set('')
        self.updating_table()

    # noinspection PyUnusedLocal
    def updating_table(self, event=None):
        self.table_model = TableModel()

        # FullName 將不顯示在表格中
        for column in TABLE:
            if column != 'FullName':
                self.table_model.addColumn(column)

        # 取得符合篩選條件與篩選名稱的角色
        self.__update_filters()
        results = [record for record in self.records_filter.filtered_records
                   if is_string_match_query(self.queried_name.get(), convert_to_str(record[1]))]

        if len(results) == 0:
            self.table_model.addRow(Nickname='無任何記錄')
        for row in results:
            data = iter(list(row[1:19]))
            self.table_model.addRow(Nickname=convert_to_str(next(data)),
                                    Profession=convert_to_str(next(data)), Rank=next(data),
                                    Active=convert_to_str(next(data)), ActiveCost=next(data),
                                    Passive1=convert_to_str(next(data)), Passive2=convert_to_str(next(data)),
                                    Attachment=convert_to_str(next(data)), WeaponType=convert_to_str(next(data)),
                                    ExpGrown=convert_to_str(next(data)), AttendanceCost=next(data),
                                    MaxAtk=next(data), MaxHP=next(data), AtkGrown=next(data),
                                    HPGrown=next(data), AtkSpeed=next(data),
                                    CriticalRate=next(data), Note=convert_to_str(next(data)))

        self.table_model.setSortOrder(columnName='Rank', reverse=1)
        self.table_model.setSortOrder(columnName='Profession')

        self.redisplay_table()

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
            self.records_filter.add_filter(5, int(active_cost))
        weapon = self.weapon_selector.get()
        if weapon != '':
            self.records_filter.add_filter(8, weapon)

    def adding_character(self):
        popup = CharacterInfoWindow()
        self.wait_window(popup)
        self.records_filter.update_raw_records()
        self.updating_table()

    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        character = self.table_model.getCellRecord(row, 0)

        popup = CharacterInfoWindow(character)
        self.wait_window(popup)
        self.updating_table()