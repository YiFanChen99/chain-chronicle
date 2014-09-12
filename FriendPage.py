# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *

UNRECORDED = '未登記'
RECORD_DB_TABLE = ['FriendID', 'RecordedDate', 'Character', 'CharacterLevel', 'Rank']
RECORD_DISPLAY_TABLE = ['State', 'FriendID', 'UsedNames', 'LastProfession', 'Character', 'CharacterLevel', 'Rank']
FRIEND_TABLE = ['ID', 'UsedNames', 'Excellence', 'Defect', 'UsedCharacters', 'RaisedIn3Weeks',
                'RaisedIn2Months', 'AddedDate', 'LastProfession', 'LastCharacter']  # TODO


# TODO 實作
class FriendInfo(MainFrameWithTable):
    def __init__(self, master, db_suffix):
        MainFrameWithTable.__init__(self, master, db_suffix)
        self.set_table_place(34, 29)

        # 切換到記錄好友現況的按鈕
        button = Button(self, text="記錄好友現況", width=2, height=17, wraplength=1, font=(MS_JH, 12))
        button.place(x=4, y=23)
        button["command"] = self.switching_to_friend_record

    def switching_to_friend_record(self):
        self.master.update_main_frame(FriendRecord(self.master, self.db_suffix))


class FriendRecord(MainFrameWithTable):
    def __init__(self, master, db_suffix):
        MainFrameWithTable.__init__(self, master, db_suffix=db_suffix)
        self.set_table_place(34, 29)
        self.table_view.cellwidth = 85

        self.__init_left_frame()
        self.__init_upper_frame()

        self.friend_count = 0
        self.friend_records = []
        self.updating_page()

    def __init_left_frame(self):
        button = Button(self, text="送出並返回", width=2, height=8, wraplength=1, font=(MS_JH, 12), borderwidth=2)
        button.place(x=4, y=23)
        button["command"] = self.submitting

        button = Button(self, text="取消並返回", width=2, height=8, wraplength=1, font=(MS_JH, 12), borderwidth=2)
        button.place(x=4, y=203)
        button["command"] = self.switching_to_friend_info

    def submitting(self):
        for data in self.friend_records:
            DATABASE.execute('insert into ' + self.compose_table_name('FriendRecord') +
                             ' (' + ','.join(RECORD_DB_TABLE) + ')' +
                             convert_data_to_insert_command(data[1], self.date.get(),
                                                            data[4], data[5], data[6]))
        DATABASE.commit()

        self.master.update_main_frame(FriendInfo(self.master, self.db_suffix))

    def switching_to_friend_info(self):
        self.master.update_main_frame(FriendInfo(self.master, self.db_suffix))

    def __init_upper_frame(self):
        basic_y = 3

        basic_x = 65
        Label(self, text='Date:', font=(MS_JH, 11)).place(x=basic_x, y=basic_y)
        self.date = StringVar(value='')
        Entry(self, width=11, textvariable=self.date, font=(MS_JH, 11)).place(x=basic_x + 41, y=basic_y + 2)

        # 選擇是否顯示已登記的好友
        basic_x = 240
        self.is_show_recorded_friends = BooleanVar()
        self.is_show_recorded_friends.trace("w", self.updating_table)
        check_button = Checkbutton(self, variable=self.is_show_recorded_friends)
        check_button.place(x=basic_x, y=basic_y)
        label = Label(self, text='顯示已登記', font=(MS_JH, 11))
        label.place(x=basic_x + 17, y=basic_y)

        # noinspection PyUnusedLocal
        def switching(*args):
            check_button.toggle()
        label.bind('<ButtonPress-1>', switching)

        basic_x = 550
        self.friend_count_str = StringVar()
        Label(self, textvariable=self.friend_count_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    # TODO 資料重撈重算
    def updating_page(self):
        self.date.set(datetime.now().date())

        self.friend_records = [['', 2, '豆腐，出堡米', '戰士', '喵喵', 20, 10],
                               [UNRECORDED, 3, 'loming', '騎士', '索喵', 40, 12]]
        self.friend_count = len(self.friend_records)
        self.friend_count_str.set('Friends: %02d' % self.friend_count)

        self.updating_table()

    # noinspection PyUnusedLocal
    def updating_table(self, event=None, *args):
        self.table_model = TableModel()

        for column in RECORD_DISPLAY_TABLE:
            self.table_model.addColumn(column)

        records = [each for each in self.friend_records if each[0] == UNRECORDED or self.is_show_recorded_friends.get()]

        if len(records) == 0:
            self.table_model.addRow(UsedNames='無任何記錄')
        else:
            for row in records:
                data = iter(row)
                self.table_model.addRow(State=next(data), FriendID=next(data), UsedNames=next(data),
                                        LastProfession=next(data), Character=next(data), CharacterLevel=next(data),
                                        Rank=next(data))
        self.table_model.setSortOrder(columnName='LastProfession')

        self.redisplay_table()
        self.table_view.hide_column('FriendID')
        self.table_view.hide_column('LastProfession')

    # TODO
    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        friend_id = self.table_model.getCellRecord(row, 1)

        column = self.table_view.get_col_clicked(event)
        if column <= 2:
            print column, '-->', 9
        else:
            print column, '-->', 3
        # self.wait_window(popup)
        # self.updating_table()