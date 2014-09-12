# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *
from BasicWindow import BasicWindow
import CharacterSelectorWindow

RECORDED = ''
UNRECORDED = '未登記'
RECORD_DB_TABLE = ['FriendID', 'RecordedDate', 'Character', 'CharacterLevel', 'Rank']
RECORD_DISPLAY_TABLE = ['State', 'FriendID', 'UsedNames', 'LastProfession',
                        'Character', 'CharacterLevel', 'Rank']
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
        def switching(obj=self, *args):
            check_button.toggle()
        label.bind('<Button-1>', switching)

        basic_x = 550
        self.friend_count_str = StringVar()
        Label(self, textvariable=self.friend_count_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    def updating_page(self):
        self.date.set(datetime.now().date())  # 此次記錄的日期

        # 建立 Friend_Record_List
        self.friend_records = []
        friends = DATABASE.execute('select ID, UsedNames, LastProfession, LastCharacter from ' +
                                   self.compose_table_name('Friend'))
        for infos in friends:
            self.friend_records.append([UNRECORDED, infos[0], convert_to_str(infos[1]),
                                        convert_to_str(infos[2]), '', 0, 0, convert_to_str(infos[3])])

        self.friend_count_str.set('Friends: %02d' % len(self.friend_records))  # 好友總數

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

    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        the_record = self.get_record_by_friend_id(int(self.table_model.getCellRecord(row, 1)))

        column = self.table_view.get_col_clicked(event)
        popup = (None if column <= 2 else UpdateFriendRecordWindow(the_record))  # TODO
        self.wait_window(popup)
        self.updating_table()

    def get_record_by_friend_id(self, friend_id):
        for each_record in self.friend_records:
            if each_record[1] == friend_id:
                return each_record


# TODO
class UpdateFriendWindow(BasicWindow):
    def __init__(self, infos, **kwargs):
        BasicWindow.__init__(self, **kwargs)
        self.infos = infos


class UpdateFriendRecordWindow(BasicWindow):
    def __init__(self, the_record, **kwargs):
        BasicWindow.__init__(self, **kwargs)
        self.window = Toplevel(width=284, height=183)
        self.window.title('Friend Record')
        self.window.geometry('+700+210')
        self.record = the_record

        label_space = 24  # Label 與 輸入元件的距離

        current_y = 8
        Label(self.window, width=12, text='UsedNames :', font=(MS_JH, 12)).place(x=5, y=current_y)
        Label(self.window, width=16, text=the_record[2], font=(MS_JH, 12),
              justify=LEFT).place(x=30, y=current_y + label_space)

        current_y = 70
        label = Label(self.window, width=10, text='Character', font=("", 12))
        label.place(x=6, y=current_y)
        self.character_var = StringVar()
        entry = self.create_entry(width=11, textvariable=self.character_var, state='readonly')
        entry.place(x=9, y=current_y + label_space)

        # noinspection PyUnusedLocal
        def selecting_character(obj=self, character_selected=self.character_var, *args):
            popup = CharacterSelectorWindow.CharacterSelectorWindow(character_selected)
            self.wait_window(popup)
            self.character_level_entry.focus_set()
        label.bind('<ButtonRelease-1>', selecting_character)
        entry.bind('<ButtonRelease-1>', selecting_character)

        Label(self.window, width=13, text='CharacterLevel', font=("", 12)).place(x=95, y=current_y)
        self.character_level_var = IntVar()
        self.character_level_entry = self.create_entry(width=6, textvariable=self.character_level_var)
        self.character_level_entry.place(x=130, y=current_y + label_space)

        # noinspection PyUnusedLocal
        def move_focus_to_rank(*args):
            self.rank_entry.focus_set()
        self.character_level_entry.bind('<Return>', move_focus_to_rank)

        Label(self.window, width=6, text='Rank', font=("", 12)).place(x=213, y=current_y)
        self.rank_var = IntVar()
        self.rank_entry = self.create_entry(width=6, textvariable=self.rank_var)
        self.rank_entry.place(x=218, y=current_y + label_space)
        self.rank_entry.bind('<Return>', self.submitting)

        # 取消的按鈕
        Button(self.window, text="Cancel", command=self.destroy, width=25, borderwidth=3,
               font=("", 12)).place(x=24, y=135)

        self.__init_record()

    def __init_record(self):
        record = self.record

        # 未選擇時套用前記錄，已選擇便用已選擇
        self.character_var.set(record[7] if record[4] == '' else record[4])

        self.character_level_var.set(record[5])

        self.rank_var.set(record[6])

    def create_entry(self, **kwargs):
        return Entry(self.window, font=("", 12), justify=CENTER, **kwargs)

    # noinspection PyUnusedLocal
    def submitting(self, *args):
        self.record[0] = RECORDED
        self.record[4] = convert_to_str(self.character_var.get())
        self.record[5] = self.character_level_var.get()
        self.record[6] = self.rank_var.get()
        self.destroy()


if __name__ == "__main__":
    root = Tk()
    init_size = str(MIN_WIDTH) + 'x' + str(MIN_HEIGHT)
    root.geometry(init_size + '+510+265')
    app = FriendRecord(master=root, db_suffix='JP')

    # ['State', 'FriendID', 'UsedNames', 'LastProfession', 'Character', 'CharacterLevel', 'Rank']
    # record = [RECORDED, 3, 'pig，亞馬卅那度', '戰士', '山貓', 60, 109]
    # app = UpdateFriendRecordWindow(record)
    app.mainloop()
    # for ele in record:
    #     print ele,