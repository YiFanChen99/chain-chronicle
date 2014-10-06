# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *
from BasicWindow import BasicWindow
import CharacterSelectorWindow
from datetime import timedelta

RECORDED = ''
UNRECORDED = '未登記'
FRIEND_MODIFIED_COLUMN = ['UsedNames', 'Excellence', 'Defect', 'AddedDate']
UPDATED_BY_RECORD_COLUMN = ['UsedCharacters', 'Rank', 'RaisedIn3Weeks', 'RaisedIn2Months',
                            'LastProfession', 'LastCharacter']
FRIEND_CLEAN_UP_COLUMN = FRIEND_MODIFIED_COLUMN + UPDATED_BY_RECORD_COLUMN
FRIEND_DISPLAYED_COLUMN = ['ID', 'UsedNames', 'Excellence', 'Defect', 'UsedCharacters', 'Rank',
                           'RaisedIn3Weeks', 'RaisedIn2Months', 'AddedDate', 'LastProfession']
ORDER_SELECTOR = ['Profession', 'Rank', 'In3Weeks', 'In2Months', 'AddedDate']
RECORD_DB_COLUMN = ['FriendID', 'RecordedDate', 'Character', 'CharacterLevel', 'Rank']
RECORD_DISPLAYED_COLUMN = ['Status', 'FriendID', 'UsedNames', 'LastProfession',
                           'Character', 'CharacterLevel', 'Rank']


class FriendInfo(MainFrameWithTable):
    def __init__(self, master, db_suffix):
        MainFrameWithTable.__init__(self, master, db_suffix)
        self.set_table_place(34, 29)

        # Left frame: 切換到記錄好友現況的按鈕
        button = Button(self, text="記錄好友現況", width=2, height=17, wraplength=1, font=(MS_JH, 12))
        button.place(x=4, y=23)
        button["command"] = self.switching_to_friend_record

        self.__init_upper_frame()

        self.friends = []
        self.updating_page()

    def switching_to_friend_record(self):
        self.master.update_main_frame(FriendRecord(self.master, self.db_suffix))

    def __init_upper_frame(self):
        basic_y = 3

        basic_x = 52
        button = Button(self, text="新增好友", width=8, font=(MS_JH, 11))
        button.place(x=basic_x, y=-1)
        button["command"] = self.adding_new_friend

        basic_x = 153
        Label(self, text='Order:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.order_selector = ttk.Combobox(self, state='readonly', width=10, justify=CENTER)
        self.order_selector.set(ORDER_SELECTOR[0])
        self.order_selector['values'] = ORDER_SELECTOR
        self.order_selector.place(x=basic_x + 55, y=basic_y + 1)
        self.order_selector.bind('<<ComboboxSelected>>', self.updating_table)

        # 角色部分名稱篩選
        basic_x = 322
        Label(self, text='篩選:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.queried_name = StringVar()
        entry = Entry(self, width=8, textvariable=self.queried_name, font=(MS_JH, 11))
        entry.place(x=basic_x + 42, y=basic_y + 2)
        entry.bind('<Return>', self.updating_table)

        basic_x = 460
        self.friend_count_str = StringVar()
        Label(self, textvariable=self.friend_count_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

        basic_x = 555
        self.last_recorded_str = StringVar()
        Label(self, textvariable=self.last_recorded_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    def updating_page(self):
        # 建立 Friend_List
        self.friends = [list(info) for info in
                        DATABASE.execute('select ' + ','.join(FRIEND_DISPLAYED_COLUMN) + ' from ' +
                                         self.compose_table_name('Friend') + ' where UsedNames!=\'\'').fetchall()]

        self.friend_count_str.set('Friends: %02d' % len(self.friends))  # 好友總數

        # 最後更新記錄時間
        date = convert_str_to_datetime(
            DATABASE.execute('select max(RecordedDate) from ' + self.compose_table_name('FriendRecord')).fetchone()[0])
        if date is not None:
            self.last_recorded_str.set('Last Recorded: %02d/%02d' % (date.month, date.day))

        self.updating_table()

    # noinspection PyUnusedLocal
    def updating_table(self, event=None, *args):
        self.table_model = TableModel()

        for column in FRIEND_DISPLAYED_COLUMN:
            self.table_model.addColumn(column)

        # 將符合名稱篩選的好友加入欲呈現表格中
        records = [each for each in self.friends if
                   is_string_match_query(self.queried_name.get(), convert_to_str(each[1]))]

        if len(records) == 0:
            self.table_model.addRow(UsedNames='無任何記錄')
        else:
            for row in records:
                data = iter(row)
                self.table_model.addRow(ID=next(data), UsedNames=convert_to_str(next(data)),
                                        Excellence=convert_to_str(next(data)), Defect=convert_to_str(next(data)),
                                        UsedCharacters=convert_to_str(next(data)), Rank=next(data),
                                        RaisedIn3Weeks=next(data), RaisedIn2Months=next(data),
                                        AddedDate=next(data), LastProfession=convert_to_str(next(data)))

        self.set_order_in_table_model()
        self.redisplay_table()
        self.table_view.hide_column('ID')
        self.table_view.hide_column('LastProfession')

        # 不限制會太寬，難以瀏覽全部資訊
        self.table_view.resizeColumn(1, 125)
        self.table_view.resizeColumn(2, 160)
        self.table_view.resizeColumn(3, 145)
        self.table_view.resizeColumn(4, 155)

    # 取得未使用的 ID，並將新資訊更新到該記錄上
    def adding_new_friend(self):
        new_id = DATABASE.execute('select ID from ' + self.compose_table_name('Friend') +
                                  ' where UsedNames==\'\'').fetchone()

        if new_id is None:
            tkMessageBox.showwarning("Can not add any friend", '已達好友上限')
            return

        popup = UpdateFriendWindow(self.db_suffix, friend_id=new_id[0])
        self.wait_window(popup)
        self.updating_page()

    def set_order_in_table_model(self):
        column_names = dict(zip(ORDER_SELECTOR, ['LastProfession', 'Rank', 'RaisedIn3Weeks',
                                                 'RaisedIn2Months', 'AddedDate']))
        self.table_model.setSortOrder(columnName=column_names[self.order_selector.get()])

    # 更改好友資訊
    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        friend_id = int(self.table_model.getCellRecord(row, 0))
        popup = UpdateFriendWindow(self.db_suffix, friend_info=self.get_info_by_id(friend_id))
        self.wait_window(popup)
        self.updating_table()

    def do_dragging_along_right(self, row_number):
        # 確認是否刪除
        names = self.table_model.getCellRecord(row_number, 1)
        if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete friend 「' + names + '」？'):
            friend_id = int(self.table_model.getCellRecord(row_number, 0))
            # 將該 ID 的資料全數清空，並將其對應的 Records 刪除
            DATABASE.execute('update ' + self.compose_table_name('Friend') +
                             convert_data_to_update_command(FRIEND_CLEAN_UP_COLUMN, [''] * 10) +
                             ' where ID=' + str(friend_id))
            DATABASE.execute('delete from ' + self.compose_table_name('FriendRecord') +
                             ' where FriendID=' + str(friend_id))
            DATABASE.commit()

            self.updating_page()

    def get_info_by_id(self, the_id):
        for info in self.friends:
            if info[0] == the_id:
                return info


class FriendRecord(MainFrameWithTable):
    def __init__(self, master, db_suffix):
        MainFrameWithTable.__init__(self, master, db_suffix=db_suffix)
        self.set_table_place(34, 29)
        self.table_view.cellwidth = 85

        self.__init_left_frame()
        self.__init_upper_frame()

        self.__init_page()

    def __init_left_frame(self):
        button = Button(self, text="送出並返回", width=2, height=8, wraplength=1, font=(MS_JH, 12), borderwidth=2)
        button.place(x=4, y=23)
        button["command"] = self.submitting

        button = Button(self, text="取消並返回", width=2, height=8, wraplength=1, font=(MS_JH, 12), borderwidth=2)
        button.place(x=4, y=203)
        button["command"] = self.switching_to_friend_info

    def submitting(self):
        # 數量計算並要求確認，確認時才真正送出
        updated_record_number = len([data for data in self.friend_records if data[0] == RECORDED])
        if tkMessageBox.askyesno('Recording these records?', '總計 ' + str(updated_record_number) +
                                 ' 筆記錄，\n是否確認送出？'):
            # 將已經登記的 record 更新到 DB 內
            for data in self.friend_records:
                if data[0] == RECORDED:
                    DATABASE.execute('insert into ' + self.compose_table_name('FriendRecord') +
                                     ' (' + ','.join(RECORD_DB_COLUMN) + ')' +
                                     convert_data_to_insert_command(data[1], self.date.get(),
                                                                    data[4], data[5], data[6]))
                    updated_record_number += 1
            DATABASE.commit()
        else:
            return

        # 確認是否更新 FriendTable 中的資訊（RaisedIn3Weeks, LastCharacter等）
        if tkMessageBox.askyesno('Updating Friend by records?', '記錄完成，\n是否要更新 Friend Info？'):
            update_friend_info_table(self.db_suffix)

        self.master.update_main_frame(FriendInfo(self.master, self.db_suffix))

    def switching_to_friend_info(self):
        self.master.update_main_frame(FriendInfo(self.master, self.db_suffix))

    def __init_upper_frame(self):
        basic_y = 3

        basic_x = 60
        Label(self, text='Date:', font=(MS_JH, 11)).place(x=basic_x, y=basic_y)
        self.date = StringVar(value='')
        Entry(self, width=11, textvariable=self.date, font=(MS_JH, 11)).place(x=basic_x + 41, y=basic_y + 2)

        # 選擇是否顯示已登記的好友
        basic_x = 256
        self.is_show_recorded_friends = BooleanVar()
        self.is_show_recorded_friends.trace("w", self.updating_table)
        check_button = Checkbutton(self, variable=self.is_show_recorded_friends)
        check_button.place(x=basic_x, y=basic_y)
        label = Label(self, text='顯示已登記', font=(MS_JH, 11))
        label.place(x=basic_x + 18, y=basic_y)
        bind_check_box_and_label(check_button, label)

        # 角色部分名稱篩選
        basic_x = 366
        Label(self, text='篩選:', font=(MS_JH, 11)).place(x=basic_x, y=basic_y)
        self.queried_name = StringVar()
        entry = Entry(self, width=11, textvariable=self.queried_name, font=(MS_JH, 11))
        entry.place(x=basic_x + 40, y=basic_y + 2)
        entry.bind('<Return>', self.updating_table)

        basic_x = 550
        self.friend_count_str = StringVar()
        Label(self, textvariable=self.friend_count_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    def __init_page(self):
        self.date.set(datetime.now().date())  # 此次記錄的日期

        # 建立 Friend_Record_List
        # 這邊取出 LastCharacter 只是為了給 UpdateFriendRecordWindow 使用，預先讀出
        self.friend_records = []
        friends = DATABASE.execute('select ID, UsedNames, LastProfession, LastCharacter from ' +
                                   self.compose_table_name('Friend') + ' where UsedNames!=\'\'')
        for infos in friends:
            self.friend_records.append([UNRECORDED, infos[0], convert_to_str(infos[1]),
                                        convert_to_str(infos[2]), '', None, None, convert_to_str(infos[3])])

        self.friend_count_str.set('Friends: %02d' % len(self.friend_records))  # 好友總數

        self.updating_table()

    # noinspection PyUnusedLocal
    def updating_table(self, event=None, *args):
        self.table_model = TableModel()

        for column in RECORD_DISPLAYED_COLUMN:
            self.table_model.addColumn(column)

        records = [each for each in self.friend_records if self.is_should_display_in_table(each)]

        if len(records) == 0:
            self.table_model.addRow(UsedNames='無任何記錄')
        else:
            for row in records:
                data = iter(row)
                self.table_model.addRow(Status=next(data), FriendID=next(data), UsedNames=next(data),
                                        LastProfession=next(data), Character=next(data), CharacterLevel=next(data),
                                        Rank=next(data))

        self.table_model.setSortOrder(columnName='LastProfession')

        self.redisplay_table()
        self.table_view.hide_column('FriendID')
        self.table_view.hide_column('LastProfession')

    # 將符合設定的已登記/未登記紀錄回傳為 True，並根據名稱要求篩選
    def is_should_display_in_table(self, record):
        is_match_recorded_setting = self.is_show_recorded_friends.get() == (record[0] == RECORDED)
        return is_match_recorded_setting and is_string_match_query(self.queried_name.get(), record[2])

    # 若雙擊右側，則欲輸入好友記錄，若雙擊左側，則為更改好友資訊
    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        friend_id = int(self.table_model.getCellRecord(row, 1))

        column = self.table_view.get_col_clicked(event)
        if column <= 2:
            popup = UpdateFriendWindow(self.db_suffix, friend_id=friend_id)
            self.wait_window(popup)
        else:
            popup = UpdateFriendRecordWindow(self.get_record_by_friend_id(friend_id))
            self.wait_window(popup)
            self.updating_table()

    def get_record_by_friend_id(self, friend_id):
        for each_record in self.friend_records:
            if each_record[1] == friend_id:
                return each_record


class UpdateFriendWindow(BasicWindow):
    def __init__(self, db_suffix, friend_info=None, friend_id=None):
        BasicWindow.__init__(self, width=306, height=272)
        self.window.title('Friend Info')
        self.window.geometry('+720+260')
        self.db_suffix = db_suffix

        self.friend_info = []
        self.init_friend_info(friend_info, friend_id)

        self.__init_widget()

    def init_friend_info(self, friend_info, friend_id):
        if friend_info is None:
            self.friend_info = list(DATABASE.execute('select ' + ','.join(FRIEND_DISPLAYED_COLUMN) + ' from ' +
                                                     self.get_db_table_name() + ' where ID=' +
                                                     str(friend_id)).fetchone())
        else:
            self.friend_info = friend_info

    def __init_widget(self):
        label_space = 24  # Label 與 輸入元件的距離

        current_y = 8
        Label(self.window, width=12, text='UsedNames :', font=(MS_JH, 12)).place(x=5, y=current_y)
        self.used_names = StringVar(value=self.friend_info[1])
        Entry(self.window, width=16, textvariable=self.used_names, font=(MS_JH, 12), justify=LEFT)\
            .place(x=30, y=current_y + label_space)

        Label(self.window, width=11, text='AddedDate', font=(MS_JH, 10), justify=CENTER)\
            .place(x=197, y=current_y + 1)
        self.added_date = StringVar(value=self.init_added_date())
        Entry(self.window, width=11, textvariable=self.added_date, font=(MS_JH, 10), justify=CENTER)\
            .place(x=196, y=current_y + label_space + 1)

        current_y += 55
        Label(self.window, width=25, text='Excellence', font=(MS_JH, 12), justify=CENTER)\
            .place(x=29, y=current_y)
        self.excellence = StringVar(value=self.friend_info[2])
        Entry(self.window, width=28, textvariable=self.excellence, font=(MS_JH, 12), justify=CENTER)\
            .place(x=27, y=current_y + label_space)

        current_y += 55
        Label(self.window, width=25, text='Defect', font=(MS_JH, 12), justify=CENTER).place(x=29, y=current_y)
        self.defect = StringVar(value=self.friend_info[3])
        Entry(self.window, width=28, textvariable=self.defect, font=(MS_JH, 12), justify=CENTER)\
            .place(x=27, y=current_y + label_space)

        # 送出的按鈕
        current_y += 66
        Button(self.window, text="Submit", command=self.submitting, width=26, borderwidth=3,
               font=("", 12)).place(x=29, y=current_y)

        # 取消的按鈕
        current_y += 39
        Button(self.window, text="Cancel", command=self.destroy, width=26, borderwidth=3,
               font=("", 12)).place(x=29, y=current_y)

    # noinspection PyUnusedLocal
    def submitting(self, *args):
        # 進行檢查，不允許 UsedNames 為空
        if self.used_names.get() == '':
            tkMessageBox.showwarning("Can not submit", '不允許 UsedNames 為空')
            return

        # 更新回原記錄
        self.friend_info[1] = self.used_names.get()
        self.friend_info[2] = self.excellence.get()
        self.friend_info[3] = self.defect.get()
        self.friend_info[8] = self.added_date.get()

        # 更新到資料庫
        values = [self.friend_info[1], self.friend_info[2], self.friend_info[3], self.friend_info[8]]
        DATABASE.execute('update ' + self.get_db_table_name() +
                         convert_data_to_update_command(FRIEND_MODIFIED_COLUMN, values) +
                         ' where ID=' + str(self.friend_info[0]))
        DATABASE.commit()

        self.destroy()

    # 好友已存在時使用原記錄，若好友不存在時使用當天日期
    def init_added_date(self):
        return self.friend_info[8] if self.used_names.get() != '' else datetime.now().date()

    def get_db_table_name(self):
        return 'Friend' + self.db_suffix


class UpdateFriendRecordWindow(BasicWindow):
    def __init__(self, the_record):
        BasicWindow.__init__(self, width=284, height=183)
        self.window.title('Friend Record')
        self.window.geometry('+740+230')
        self.record = the_record

        self.__init_widget()

        self.__init_record()

    def __init_widget(self):
        label_space = 24  # Label 與 輸入元件的距離

        current_y = 8
        Label(self.window, width=12, text='UsedNames :', font=(MS_JH, 12)).place(x=5, y=current_y)
        Label(self.window, width=20, text=self.record[2], font=(MS_JH, 12),
              justify=LEFT).place(x=22, y=current_y + label_space)

        current_y = 70
        label = Label(self.window, width=10, text='Character', font=("", 12))
        label.place(x=6, y=current_y)
        self.character_var = StringVar()
        entry = self.create_entry(width=11, textvariable=self.character_var, state='readonly')
        entry.place(x=9, y=current_y + label_space)

        # noinspection PyUnusedLocal
        def selecting_character(obj=self, character_selected=self.character_var, *args):
            popup = CharacterSelectorWindow.CharacterSelectorWindow(character_selected)
            popup.window.geometry('+732+270')
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

    def __init_record(self):
        record = self.record

        # 角色未選擇時套用前記錄，已選擇便用已選擇
        self.character_var.set(record[7] if record[4] == '' else record[4])

        # 角色等級/Rank等級未選擇時為空，已選擇便用已選擇
        self.character_level_var.set('' if record[5] is None else record[5])
        self.rank_var.set('' if record[6] is None else record[6])

    def create_entry(self, **kwargs):
        return Entry(self.window, font=("", 12), justify=CENTER, **kwargs)

    # noinspection PyUnusedLocal
    def submitting(self, *args):
        self.record[0] = RECORDED
        self.record[4] = convert_to_str(self.character_var.get())
        self.record[5] = self.character_level_var.get()
        self.record[6] = self.rank_var.get()
        self.destroy()


# 重新統計 FriendRecord 並寫入 Friend Table 內
def update_friend_info_table(db_suffix):
    updater = FriendInfoUpdater(db_suffix)
    # 對每個好友進行處理
    for info in DATABASE.execute('select ID from Friend' + db_suffix + ' where UsedNames!=\'\'').fetchall():
        updater.update_friend(info[0])
    DATABASE.commit()


class FriendInfoUpdater:
    def __init__(self, db_suffix):
        self.db_suffix = db_suffix

    # 更新該好友的資訊到記憶體的 DB 中，尚未 commit
    # noinspection PyAttributeOutsideInit
    def update_friend(self, friend_id):
        # 取出該 ID 對應的所有記錄，從最近排序到最久以前
        records = DATABASE.execute('select ' + ','.join(RECORD_DB_COLUMN[1:5]) + ' from FriendRecord' + self.db_suffix +
                                   ' where FriendID=' + str(friend_id) + ' order by RecordedDate DESC').fetchall()

        # 新好友可能會尚無記錄可供更新，則不必處理
        if len(records) == 0:
            return

        # 最新一筆資料即可得到 LastProfession LastCharacter Rank
        self.last_character = records[0][1]
        self.last_profession = DATABASE.execute('select Profession from Character where Nickname=' +
                                                convert_datum_to_command(self.last_character)).fetchone()[0]
        self.rank = records[0][3]

        # 找出 UsedCharacters RaisedIn3Weeks RaisedIn2Months
        self.raised_recorder = RaisedRecorder()
        self.character_recorder = CharacterRecorder()
        for record in records:
            # 更新範圍內日期的 Rank，以取得範圍內的改變量
            self.raised_recorder.record_if_in_duration(record)
            # 將有使用的角色彙整
            self.character_recorder.record_if_not_existed(record)
        self.raised_in_3_weeks = self.raised_recorder.get_raised_in_3_weeks()
        self.raised_in_2_months = self.raised_recorder.get_raised_in_2_months()
        self.used_characters = self.character_recorder.get_used_characters()

        DATABASE.execute('update Friend' + self.db_suffix + convert_data_to_update_command(
            UPDATED_BY_RECORD_COLUMN, [self.used_characters, self.rank, self.raised_in_3_weeks,
                                       self.raised_in_2_months, self.last_profession, self.last_character]) +
                         ' where ID=' + str(friend_id))


class RaisedRecorder:
    def __init__(self):
        self.date_of_3_weeks = datetime.now() - timedelta(weeks=2)
        self.date_of_2_months = datetime.now() - timedelta(days=61)
        self.newest_rank = 0

    # 此方法被呼叫時必須保持由新到舊的順序傳入記錄，才可取得真正的區間內變化
    # noinspection PyAttributeOutsideInit
    def record_if_in_duration(self, record):
        # 記錄最新的 Rank，結算時使用
        if self.newest_rank == 0:
            self.newest_rank = record[3]

        recorded_date = convert_str_to_datetime(record[0])
        if self.date_of_3_weeks <= recorded_date:
            self.rank_3_weeks_ago = record[3]
        if self.date_of_2_months <= recorded_date:
            self.rank_2_months_ago = record[3]

    def get_raised_in_3_weeks(self):
        return self.newest_rank - self.rank_3_weeks_ago

    def get_raised_in_2_months(self):
        return self.newest_rank - self.rank_2_months_ago


class CharacterRecorder:
    def __init__(self):
        self.used_characters = {}

    # 此方法被呼叫時必須保持由新到舊的順序傳入記錄，才可取得各角色的最高等級
    def record_if_not_existed(self, record):
        nickname = convert_to_str(record[1])
        if not nickname in self.used_characters:
            self.used_characters[nickname] = record[2]

    def get_used_characters(self):
        result = ''
        for name, level in self.used_characters.iteritems():
            result += name + str(level) + '、'
        return result