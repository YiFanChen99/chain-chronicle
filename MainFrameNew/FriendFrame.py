# -*- coding: utf-8 -*-
from MainFrameNew.BaseFrame import *
from ModelUtility.Filter import FilterRuleManager
from ModelUtility.DBAccessor import *
from ModelUtility.Utility import bind_check_box_and_label, convert_str_to_date
from ModelUtility.Comparator import sub_match_request_or_japanese_character
from ModelUtility.CommonState import *
from Window.FriendWindow import FriendInfoUpdaterWindow, FriendRecordUpdaterWindow
from Model.FriendModel import take_statistic_to_update_friend_info


class FriendInfoFrame(MainFrameWithTable):
    ORDER_OPTIONS = ['Profession', 'Rank', 'In3Weeks', 'In2Months', 'AddedDate']

    def __init__(self, master):
        MainFrameWithTable.__init__(self, master)
        self.set_table_place(34, 29)
        self.table_model = TableModelAdvance()
        self.table_model.set_columns(FriendInfo.DISPLAYED_COLUMNS, main_column='UsedNames')
        self.table_view.setModel(self.table_model)
        self.filter_manager = FilterRuleManager()
        self.filter_manager.set_comparison_rule('used_names', rule=sub_match_request_or_japanese_character)
        self.filter_manager.set_comparison_rule('relation')
        self.filter_manager.set_comparison_rule('used_characters')

        # Left frame: 切換到記錄好友現況的按鈕
        button = Button(self, text="記錄好友現況", width=2, height=17, wraplength=1, font=(MS_JH, 12))
        button.place(x=4, y=23)
        button["command"] = self.switching_to_friend_record

        self._init_upper_frame()

        self.friend_infos = []
        self._init_since_last_record()
        self.update_all()

    def _init_upper_frame(self):
        basic_y = 3

        basic_x = 52
        button = Button(self, text="新增好友", width=8, font=(MS_JH, 11))
        button.place(x=basic_x, y=-1)
        button["command"] = self.adding_new_friend

        basic_x = 153
        Label(self, text='Order:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.order_selector = ttk.Combobox(self, state='readonly', width=10, justify=CENTER)
        self.order_selector.set(self.ORDER_OPTIONS[0])
        self.order_selector['values'] = self.ORDER_OPTIONS
        self.order_selector.place(x=basic_x + 55, y=basic_y + 1)
        self.order_selector.bind('<<ComboboxSelected>>', lambda x: self.redisplay_table_by_order_rule())

        # 角色部分名稱篩選
        basic_x = 322
        Label(self, text='篩選:', font=(MS_JH, 12)).place(x=basic_x, y=basic_y)
        self.queried_name = StringVar()
        entry = Entry(self, width=8, textvariable=self.queried_name, font=(MS_JH, 11))
        entry.place(x=basic_x + 42, y=basic_y + 2)
        entry.bind('<Return>', lambda x: self.update_table())

        basic_x = 460
        self.friend_count_var = StringVar()
        Label(self, textvariable=self.friend_count_var, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

        basic_x = 565
        self.since_last_record_var = StringVar()
        Label(self, textvariable=self.since_last_record_var, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    def _init_since_last_record(self):
        # 欲取得最後更新全體記錄的時間，但只用了效果類似的手段（抓不特定老朋友最後被更新的時間）
        that_date = convert_str_to_date(
            DBAccessor.execute(
                'select max({2}) from {0} where {1} = (select {1} from {0} where {2} = (select min({2}) from {0}))'.format(
                    'FriendRecord' + get_db_suffix(), 'FriendID', 'RecordedDate')).fetchone()[0])
        if that_date is not None:
            self.since_last_record_var.set('Since: %d days ago' % (date.today() - that_date).days)

    def update_all(self):
        # 建立 FriendInfoObjects
        self.friend_infos = DBAccessor.select_friend_info_list()

        self.friend_count_var.set('Friends: %02d' % len(self.friend_infos))  # 好友總數

        self.update_table()

    def update_table(self):
        # 將符合名稱篩選的好友加入欲呈現表格中
        self.table_model.set_rows([info.get_displayed_info()
                                   for info in self.filter_manager.filter(self.friend_infos, self.queried_name.get())])

        self.redisplay_table_by_order_rule()

    def redisplay_table_by_order_rule(self):
        # 先根據目前的選擇設定排序方法
        corresponding_column_names = \
            dict(zip(self.ORDER_OPTIONS, ['LastProfession', 'Rank', 'RaisedIn3Weeks', 'RaisedIn2Months', 'AddedDate']))
        self.table_model.setSortOrder(columnName=corresponding_column_names[self.order_selector.get()])

        self.redisplay_table()

        self.table_view.hide_column('ID')
        self.table_view.hide_column('LastProfession')

        # 不限制會太寬，難以瀏覽全部資訊
        self.table_view.resizeColumn(1, 125)  # UsedNames
        self.table_view.resizeColumn(2, 100)  # Excellence
        self.table_view.resizeColumn(3, 85)  # Defect
        self.table_view.resizeColumn(4, 65)  # Relation
        self.table_view.resizeColumn(5, 70)  # Offline
        self.table_view.resizeColumn(6, 155)  # UsedCharacters

    def switching_to_friend_record(self):
        self.master.update_main_frame(FriendRecordFrame(self.master))

    # 取得未使用的 ID，並將新好友指定到該 ID
    def adding_new_friend(self):
        try:
            friend_info = DBAccessor.select_unused_friend_info()
        except ValueError:
            tkMessageBox.showwarning("Can not add any friend", '已達好友上限', parent=self)
            return

        FriendInfoUpdaterWindow(self, friend_info, callback=lambda: (
            self.update_friend_info_into_db(friend_info), self.update_all()))

    # 更改好友資訊
    def do_double_clicking(self, event):
        friend_info = self.get_corresponding_friend_info_in_row(self.table_view.get_row_clicked(event))
        FriendInfoUpdaterWindow(self, friend_info, callback=lambda: (
            self.update_friend_info_into_db(friend_info), self.update_table()))

    @staticmethod
    def update_friend_info_into_db(friend_info):
        DBAccessor.update_friend_info_into_db(friend_info, commit_followed=True)

    def do_dragging_along_right(self, row_number):
        friend_info = self.get_corresponding_friend_info_in_row(row_number)
        # 確認是否刪除
        if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete friend 「{0}」？'.format(
                friend_info.used_names.encode('utf-8')), parent=self):
            self.remove_friend(friend_info)
            self.friend_infos.remove(friend_info)  # 直接從 list 中拿掉，不用重撈
            self.friend_count_var.set('Friends: %02d' % len(self.friend_infos))  # 好友總數更新
            self.update_table()

    @staticmethod
    def remove_friend(friend_info):
        # 將 FriendInfo table 中該 ID 的其他欄位全數清空
        columns = FriendInfo.CLEANED_UP_COLUMNS
        DBAccessor.execute('update FriendInfo{0}{1} where ID={2}'.format(
            get_db_suffix(), convert_data_to_update_command(columns, [''] * len(columns)), friend_info.f_id))
        # 將 FriendRecord table 中對應其 ID 的記錄全數刪除
        DBAccessor.execute('delete from FriendRecord{0} where FriendID={1}'.format(get_db_suffix(), friend_info.f_id))
        DBAccessor.commit()

    def get_corresponding_friend_info_in_row(self, row_number):
        selected_id = self.table_model.getCellRecord(row_number, 0)
        for friend_info in self.friend_infos:
            if friend_info.f_id == selected_id:
                return friend_info


class FriendRecordFrame(MainFrameWithTable):
    def __init__(self, master):
        MainFrameWithTable.__init__(self, master)
        self.set_table_place(34, 29)
        self.table_view.cellwidth = 85
        self.table_model = TableModelAdvance()
        self.table_model.set_columns(FriendRecord.DISPLAYED_COLUMNS, main_column='UsedNames')
        self.table_view.setModel(self.table_model)
        self.filer_manager = FilterRuleManager()
        self.filer_manager.set_comparison_rule('used_names', rule=sub_match_request_or_japanese_character)
        self.filer_manager.set_comparison_rule('current_character')

        self._init_left_frame()
        self._init_upper_frame()

        self._init_context()

    def _init_left_frame(self):
        button = Button(self, text="送出並返回", width=2, height=8, wraplength=1, font=(MS_JH, 12), borderwidth=2)
        button.place(x=4, y=23)
        button["command"] = self.submitting

        button = Button(self, text="取消並返回", width=2, height=8, wraplength=1, font=(MS_JH, 12), borderwidth=2)
        button.place(x=4, y=203)
        button["command"] = self.switching_to_friend_info

    def _init_upper_frame(self):
        basic_y = 3

        # 供使用者調整日期
        basic_x = 60
        Label(self, text='Date:', font=(MS_JH, 11)).place(x=basic_x, y=basic_y)
        self.date = StringVar(value='')
        Entry(self, width=11, textvariable=self.date, font=(MS_JH, 11)).place(x=basic_x + 41, y=basic_y + 2)

        # 選擇是否顯示已登記的好友
        basic_x = 256
        self.is_show_recorded_friends = BooleanVar()
        self.is_show_recorded_friends.trace("w", lambda *args: self.update_table())
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
        entry.bind('<Return>', lambda event: self.update_table())

        basic_x = 550
        self.friend_count_str = StringVar()
        Label(self, textvariable=self.friend_count_str, font=(MS_JH, 12)).place(x=basic_x + 17, y=basic_y)

    def _init_context(self):
        self.date.set(date.today())  # 此次記錄的日期

        # 建立 FriendRecordObjects
        self.friend_records = DBAccessor.select_new_friend_record_list()

        self.friend_count_str.set('Friends: %02d' % len(self.friend_records))  # 好友總數

        self.update_table()

    def update_table(self):
        # 根據名稱要求篩選，同時篩選符合設定的已登記/未登記紀錄
        self.filer_manager.set_specific_condition(
            'status', RECORDED if self.is_show_recorded_friends.get() else UNRECORDED)
        self.table_model.set_rows([record.get_displayed_info() for record in
                                   self.filer_manager.filter(self.friend_records, self.queried_name.get())])

        self.table_model.setSortOrder(columnName='LastProfession')

        self.redisplay_table()
        self.table_view.hide_column('ID')
        self.table_view.hide_column('LastProfession')

    def submitting(self):
        # 先確認資料的正確性
        if self.validate_before_submitting():
            # 將已經登記的 record 逐一更新到 DB 內
            for record in self.friend_records:
                if record.status == RECORDED:
                    DBAccessor.insert_friend_record_into_db(
                        record, self.date.get(), commit_followed=False)
            DBAccessor.commit()

            # 更新 FriendInfo Table 中的資訊（RaisedIn3Weeks, LastCharacter 等）
            take_statistic_to_update_friend_info()

            self.switching_to_friend_info()

    # 檢查數量計算並要求確認，確認後時才真正送出
    def validate_before_submitting(self):
        updated_record_number = sum(1 for record in self.friend_records if record.status == RECORDED)
        return tkMessageBox.askyesno('Recording these records?', '總計 {0} 筆記錄，\n是否確認送出？'.format(
            updated_record_number), parent=self)

    def switching_to_friend_info(self):
        self.master.update_main_frame(FriendInfoFrame(self.master))

    # 若雙擊右側，則欲編輯好友記錄，若雙擊左側，則為更改好友資訊
    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        the_friend_id = int(self.table_model.getCellRecord(row, 0))

        column = self.table_view.get_col_clicked(event)
        if column == 1:
            FriendInfoUpdaterWindow(self, DBAccessor.select_specific_friend_info(the_friend_id),
                                    callback=lambda info: None)
        else:
            for record in self.friend_records:
                if record.f_id == the_friend_id:
                    FriendRecordUpdaterWindow(self, record, self.update_table)
