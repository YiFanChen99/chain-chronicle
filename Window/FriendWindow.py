# -*- coding: utf-8 -*-
from BasicWindow import *
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *


class UpdateFriendWindow(BasicWindow):
    def __init__(self, master, db_suffix, friend_info=None, friend_id=None, width=306, height=272, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Friend Info')
        self.geometry('+720+260')
        self.db_suffix = db_suffix

        self.friend_info = []
        self.init_friend_info(friend_info, friend_id)

        self.__init_widget()

    def init_friend_info(self, friend_info, friend_id):
        if friend_info is None:
            self.friend_info = list(DBAccessor.execute('select ' + ','.join(FRIEND_DISPLAYED_COLUMN) + ' from ' +
                                                       self.get_db_table_name() + ' where ID=' +
                                                       str(friend_id)).fetchone())
        else:
            self.friend_info = friend_info

    def __init_widget(self):
        label_space = 24  # Label 與 輸入元件的距離

        current_y = 8
        Label(self, width=12, text='UsedNames :', font=(MS_JH, 12)).place(x=5, y=current_y)
        self.used_names = StringVar(value=self.friend_info[1])
        Entry(self, width=16, textvariable=self.used_names, font=(MS_JH, 12), justify=LEFT)\
            .place(x=30, y=current_y + label_space)

        Label(self, width=11, text='AddedDate', font=(MS_JH, 10), justify=CENTER)\
            .place(x=197, y=current_y + 1)
        self.added_date = StringVar(value=self.init_added_date())
        Entry(self, width=11, textvariable=self.added_date, font=(MS_JH, 10), justify=CENTER)\
            .place(x=196, y=current_y + label_space + 1)

        current_y += 55
        Label(self, width=25, text='Excellence', font=(MS_JH, 12), justify=CENTER)\
            .place(x=29, y=current_y)
        self.excellence = StringVar(value=self.friend_info[2])
        excellence_entry = Entry(self, width=28, textvariable=self.excellence, font=(MS_JH, 12), justify=CENTER)
        excellence_entry.place(x=27, y=current_y + label_space)

        current_y += 55
        Label(self, width=25, text='Defect', font=(MS_JH, 12), justify=CENTER).place(x=29, y=current_y)
        self.defect = StringVar(value=self.friend_info[3])
        defect_entry = Entry(self, width=28, textvariable=self.defect, font=(MS_JH, 12), justify=CENTER)
        defect_entry.place(x=27, y=current_y + label_space)
        defect_entry.bind('<Return>', self.submitting)

        # noinspection PyUnusedLocal
        def move_focus_to_defect_entry(*args):
            defect_entry.focus_set()
        excellence_entry.bind('<Return>', move_focus_to_defect_entry)

        # 送出的按鈕
        current_y += 66
        Button(self, text="Submit", command=self.submitting, width=26, borderwidth=3,
               font=("", 12)).place(x=29, y=current_y)

        # 取消的按鈕
        current_y += 39
        Button(self, text="Cancel", command=self.destroy, width=26, borderwidth=3,
               font=("", 12)).place(x=29, y=current_y)

    # noinspection PyUnusedLocal
    def submitting(self, *args):
        # 進行檢查，不允許 UsedNames 為空
        if self.used_names.get() == '':
            tkMessageBox.showwarning("Can not submit", '不允許 UsedNames 為空', parent=self)
            return

        # 更新回原記錄
        self.friend_info[1] = self.used_names.get()
        self.friend_info[2] = self.excellence.get()
        self.friend_info[3] = self.defect.get()
        self.friend_info[8] = self.added_date.get()

        # 更新到資料庫
        values = [self.friend_info[1], self.friend_info[2], self.friend_info[3], self.friend_info[8]]
        DBAccessor.execute('update ' + self.get_db_table_name() +
                           convert_data_to_update_command(FRIEND_MODIFIED_COLUMN, values) +
                           ' where ID=' + str(self.friend_info[0]))
        DBAccessor.commit()

        self.destroy()

    # 好友已存在時使用原記錄，若好友不存在時使用當天日期
    def init_added_date(self):
        return self.friend_info[8] if self.used_names.get() != '' else datetime.now().date()

    def get_db_table_name(self):
        return 'Friend' + self.db_suffix


class UpdateFriendRecordWindow(BasicWindow):
    def __init__(self, master, the_record, width=284, height=183, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Friend Record')
        self.geometry('+740+230')
        self.record = the_record

        self.__init_widget()

        self.__init_record()

    def __init_widget(self):
        label_space = 24  # Label 與 輸入元件的距離

        current_y = 8
        Label(self, width=12, text='UsedNames :', font=(MS_JH, 12)).place(x=5, y=current_y)
        Label(self, width=20, text=self.record[2], font=(MS_JH, 12),
              justify=LEFT).place(x=22, y=current_y + label_space)

        current_y = 70
        label = Label(self, width=10, text='Character', font=("", 12))
        label.place(x=6, y=current_y)
        self.character_var = StringVar()
        entry = self.create_entry(width=11, textvariable=self.character_var, state='readonly')
        entry.place(x=9, y=current_y + label_space)

        # noinspection PyUnusedLocal
        def selecting_character(event, obj=self, character_on_selected=self.character_var):
            popup = CharacterSelectionWindow(obj, self.character_var.set, character_on_selected)
            popup.geometry('+732+270')
            obj.wait_window(popup)
            obj.character_level_entry.focus_set()

        label.bind('<ButtonRelease-1>', selecting_character)
        entry.bind('<ButtonRelease-1>', selecting_character)

        Label(self, width=13, text='CharacterLevel', font=("", 12)).place(x=95, y=current_y)
        self.character_level_var = IntVar()
        self.character_level_entry = self.create_entry(width=6, textvariable=self.character_level_var)
        self.character_level_entry.place(x=130, y=current_y + label_space)

        # noinspection PyUnusedLocal
        def move_focus_to_rank(*args):
            self.rank_entry.focus_set()

        self.character_level_entry.bind('<Return>', move_focus_to_rank)

        Label(self, width=6, text='Rank', font=("", 12)).place(x=213, y=current_y)
        self.rank_var = IntVar()
        self.rank_entry = self.create_entry(width=6, textvariable=self.rank_var)
        self.rank_entry.place(x=218, y=current_y + label_space)
        self.rank_entry.bind('<Return>', self.submitting)

        # 取消的按鈕
        Button(self, text="Cancel", command=self.destroy, width=25, borderwidth=3,
               font=("", 12)).place(x=24, y=135)

    def __init_record(self):
        record = self.record

        # 角色未選擇時套用前記錄，已選擇便用已選擇
        self.character_var.set(record[8] if record[4] == '' else record[4])

        # 角色等級/Rank等級未選擇時為空，已選擇便用已選擇
        self.character_level_var.set('' if record[5] is None else record[5])
        self.rank_var.set('' if record[6] is None else record[6])

    def create_entry(self, **kwargs):
        return Entry(self, font=("", 12), justify=CENTER, **kwargs)

    # noinspection PyUnusedLocal
    def submitting(self, *args):
        self.record[0] = RECORDED
        self.record[4] = convert_to_str(self.character_var.get())
        self.record[5] = self.character_level_var.get()
        self.record[6] = self.rank_var.get()
        self.destroy()
