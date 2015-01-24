# -*- coding: utf-8 -*-
from MainFrame import *
from datetime import timedelta
from ModelUtility.CommonString import *
from Window.FriendWindow import FriendInfoUpdaterWindow, FriendRecordUpdaterWindow
from ModelUtility.Utility import bind_check_box_and_label

UPDATED_BY_RECORD_COLUMN = ['UsedCharacters', 'Rank', 'RaisedIn3Weeks', 'RaisedIn2Months',
                            'LastProfession', 'LastCharacter']
FRIEND_CLEAN_UP_COLUMN = FRIEND_MODIFIED_COLUMN + UPDATED_BY_RECORD_COLUMN
ORDER_SELECTOR = ['Profession', 'Rank', 'In3Weeks', 'In2Months', 'AddedDate']
RECORD_DB_COLUMN = ['FriendID', 'RecordedDate', 'Character', 'CharacterLevel', 'Rank']
RECORD_DISPLAYED_COLUMN = ['Status', 'FriendID', 'UsedNames', 'LastProfession',
                           'Character', 'CharacterLevel', 'Rank', 'LastRank']


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
        self.__init_since_last_record()
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

        basic_x = 565
        self.since_last_record_str = StringVar()
        Label(self, textvariable=self.since_last_record_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    def __init_since_last_record(self):
        # 欲取得最後更新全體記錄的時間，但只用了效果類似的手段（抓不特定老朋友最後被更新的時間）
        date = convert_str_to_datetime(
            DATABASE.execute(
                "select max({2}) from {0} where {1} = (select {1} from {0} where {2} = (select min({2}) from {0}))".format(
                    self.compose_table_name('FriendRecord'), 'FriendID', 'RecordedDate')).fetchone()[0])
        if date is not None:
            self.since_last_record_str.set('Since: %d days ago' % (datetime.now() - date).days)

    def updating_page(self):
        # 建立 Friend_List
        self.friends = [list(info) for info in
                        DATABASE.execute('select ' + ','.join(FRIEND_DISPLAYED_COLUMN) + ' from ' +
                                         self.compose_table_name('Friend') + ' where UsedNames!=\'\'').fetchall()]

        self.friend_count_str.set('Friends: %02d' % len(self.friends))  # 好友總數

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

    # 取得未使用的 ID，並將新好友指定到該 ID
    def adding_new_friend(self):
        unused_record = DATABASE.execute('select ID from ' + self.compose_table_name('Friend') +
                                  ' where UsedNames==\'\'').fetchone()

        if unused_record is None:
            tkMessageBox.showwarning("Can not add any friend", '已達好友上限', parent=self)
            return

        popup = FriendInfoUpdaterWindow(self, self.db_suffix, friend_id=unused_record[0])
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
        popup = FriendInfoUpdaterWindow(self, self.db_suffix, friend_info=self.get_info_by_id(friend_id))
        self.wait_window(popup)
        self.updating_table()

    def do_dragging_along_right(self, row_number):
        # 確認是否刪除
        names = self.table_model.getCellRecord(row_number, 1)
        if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete friend 「' + names + '」？', parent=self):
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
        if tkMessageBox.askyesno('Recording these records?', '總計 {0} 筆記錄，\n是否確認送出？'.format(
                str(updated_record_number)), parent=self):
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

        # 更新 FriendTable 中的資訊（RaisedIn3Weeks, LastCharacter 等）
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
        # 這邊取出 LastCharacter 只是為了給 FriendRecordUpdaterWindow 使用，預先讀出
        self.friend_records = []
        friends = DATABASE.execute('select ID, UsedNames, LastProfession, Rank, LastCharacter from ' +
                                   self.compose_table_name('Friend') + ' where UsedNames!=\'\'')
        for infos in friends:
            self.friend_records.append([UNRECORDED, infos[0], convert_to_str(infos[1]),
                                        convert_to_str(infos[2]), '', None, None, infos[3], convert_to_str(infos[4])])

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
                                        Rank=next(data), LastRank=next(data))

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
            popup = FriendInfoUpdaterWindow(self, self.db_suffix, friend_id=friend_id)
            self.wait_window(popup)
        else:
            popup = FriendRecordUpdaterWindow(self, self.get_record_by_friend_id(friend_id))
            self.wait_window(popup)
            self.updating_table()

    def get_record_by_friend_id(self, friend_id):
        for each_record in self.friend_records:
            if each_record[1] == friend_id:
                return each_record


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