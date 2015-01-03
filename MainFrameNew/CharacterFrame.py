# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from BaseFrame import *
from Window.CharacterWindow import CharacterInfoWindow
from ModelUtility.FilterManager import FilterManager
from ModelUtility.DBAccessor import *
from ModelUtility.Comparator import *
from UIUtility.Selector import ProfessionSelector, RankSelector


class Character(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(34, 38)

        # 新增記錄的按鈕
        button = Button(self, text="新增角色資訊", width=2, height=17, wraplength=1, font=(MS_JH, 12))
        button.place(x=4, y=23)
        button["command"] = self.adding_character

        self.__init_filter_frame()

        self.records = DBAccessor.execute('select * from Character').fetchall()
        self.filter_manager = FilterManager()
        self.__init_filter_manager()

        self.updating_table()

    def __init_filter_frame(self):
        filter_frame = Frame(self, width=self['width'], height=40)
        filter_frame.place(x=0, y=0)

        current_x = 50
        self.profession_selector = ProfessionSelector(filter_frame, self.updating_profession)
        self.profession_selector.place(x=current_x, y=-4)

        current_x += 195
        self.rank_selector = RankSelector(filter_frame, self.updating_rank)
        self.rank_selector.place(x=current_x, y=-4)

        # 角色部分名稱篩選
        current_x += 220
        Label(filter_frame, text='篩選:', font=(MS_JH, 12)).place(x=current_x, y=8)
        self.request = StringVar()
        entry = Entry(filter_frame, width=9, textvariable=self.request, font=(MS_JH, 11))
        entry.place(x=current_x + 42, y=10)
        entry.bind('<Return>', self.updating_table)

        # 清空進行篩選的條件
        button = Button(filter_frame, text="清空條件", width=7, font=(MS_JH, 11))
        button.place(x=640, y=3)
        button["command"] = self.clearing_filters

    # noinspection PyUnusedLocal
    def updating_table(self, event=None):
        self.table_model = TableModel()

        # FullName 將不顯示在表格中
        for column in CHARACTER_DB_TABLE:
            if column != 'FullName':
                self.table_model.addColumn(column)

        # 取得符合篩選條件與篩選名稱的角色
        results = self.filter_manager.filter(self.records, convert_to_str(self.request.get()))

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

    def __init_filter_manager(self):
        self.filter_manager.add_comparison_rule(0)
        self.filter_manager.add_comparison_rule(1)
        self.filter_manager.add_comparison_rule(4)
        self.filter_manager.add_comparison_rule(6)
        self.filter_manager.add_comparison_rule(7)
        self.filter_manager.add_comparison_rule(8)

    def updating_profession(self, request):
        self.filter_manager.add_specific_condition(2, request)
        self.updating_table()

    def updating_rank(self, request):
        self.filter_manager.add_specific_condition(3, request, match_requested_rank)
        self.updating_table()

    def clearing_filters(self):
        self.profession_selector.clean_current_selection()
        self.rank_selector.clean_current_selection()
        self.filter_manager.clean_specific_condition()
        self.request.set('')
        self.updating_table()

    def adding_character(self):
        popup = CharacterInfoWindow()
        self.wait_window(popup)
        self.records = DBAccessor.execute('select * from Character').fetchall()
        self.updating_table()

    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        character = self.table_model.getCellRecord(row, 0)

        popup = CharacterInfoWindow(character)
        self.wait_window(popup)
        self.updating_table()