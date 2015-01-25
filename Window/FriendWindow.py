# -*- coding: utf-8 -*-
from BasicWindow import *
from UIUtility.CharacterSelector import CharacterSelectorCanvas
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *


class FriendInfoUpdaterWindow(BasicWindow):
    def __init__(self, master, db_suffix, friend_info, callback, width=312, height=273, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Friend Info')
        self.geometry('+750+260')
        self.db_suffix = db_suffix

        self.friend_info = friend_info  #TODO 放到_init_widget下
        self._init_widget()
        self.callback = callback

    def _init_widget(self):
        label_space = 24  # Label 與 輸入元件的距離

        current_y = 8
        Label(self, width=12, text='UsedNames :', font=(MS_JH, 12)).place(x=5, y=current_y)
        self.used_names = StringVar(value=self.friend_info[1])
        Entry(self, width=16, textvariable=self.used_names, font=(MS_JH, 12), justify=LEFT)\
            .place(x=30, y=current_y + label_space)

        Label(self, width=11, text='AddedDate', font=(MS_JH, 10)).place(x=197, y=current_y + 1)
        self.added_date = StringVar(value=self.init_added_date())
        Entry(self, width=11, textvariable=self.added_date, font=(MS_JH, 10), justify=CENTER)\
            .place(x=196, y=current_y + label_space + 1)

        current_y += 55
        Label(self, width=25, text='Excellence', font=(MS_JH, 12)).place(x=29, y=current_y)
        self.excellence = StringVar(value=self.friend_info[2])
        excellence_entry = Entry(self, width=28, textvariable=self.excellence, font=(MS_JH, 12), justify=CENTER)
        excellence_entry.place(x=27, y=current_y + label_space)

        current_y += 55
        Label(self, width=25, text='Defect', font=(MS_JH, 12)).place(x=29, y=current_y)
        self.defect = StringVar(value=self.friend_info[3])
        defect_entry = Entry(self, width=28, textvariable=self.defect, font=(MS_JH, 12), justify=CENTER)
        defect_entry.place(x=27, y=current_y + label_space)
        defect_entry.bind('<Return>', self.submitting)

        # noinspection PyUnusedLocal
        def move_focus_to_defect_entry(*args):
            defect_entry.focus_set()
        excellence_entry.bind('<Return>', move_focus_to_defect_entry)

        # 送出的按鈕
        current_y += 69
        Button(self, text="Submit", command=self.submitting, width=26, borderwidth=3,
               font=("", 12)).place(x=31, y=current_y)

        # 取消的按鈕
        current_y += 39
        Button(self, text="Cancel", command=self.destroy, width=26, borderwidth=3,
               font=("", 12)).place(x=31, y=current_y)

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
        self.callback()

    # 好友已存在時使用原記錄，若好友不存在時使用當天日期
    def init_added_date(self):
        return self.friend_info[8] if self.used_names.get() != '' else datetime.now().date()

    def get_db_table_name(self):
        return 'Friend' + self.db_suffix


class FriendRecordUpdaterWindow(BasicWindow):
    def __init__(self, master, record, callback, width=309, height=198, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Friend Record')
        self.geometry('+740+230')

        self._init_widget()
        self._init_record(record)
        self.callback = callback

    def _init_widget(self):
        Label(self, width=12, text='UsedNames :', font=(SCP, 12)).place(x=15, y=8)
        self.used_names = StringVar()
        Label(self, width=22, textvariable=self.used_names, font=(MS_JH, 12), anchor=W).place(x=47, y=32)

        self.character_selector = CharacterSelectorCanvas(self)
        self.character_selector.place(x=8, y=68)
        self.character_selector.bind('<Return>', lambda x: character_level_entry.focus_set())

        current_y = 71
        Label(self, width=7, text='C.Level', font=(SCP, 12)).place(x=146, y=current_y)
        self.character_level_var = IntVar()
        character_level_entry = Entry(self, width=6, textvariable=self.character_level_var,
                                      font=(SCP, 12), justify=CENTER)
        character_level_entry.place(x=153, y=current_y + 28)
        character_level_entry.bind('<Return>', lambda x: rank_entry.focus_set())

        Label(self, width=6, text='Rank', font=(SCP, 12)).place(x=229, y=current_y)
        self.rank_var = IntVar()
        rank_entry = Entry(self, width=6, textvariable=self.rank_var, font=(SCP, 12), justify=CENTER)
        rank_entry.place(x=232, y=current_y + 27)
        rank_entry.bind('<Return>', lambda x: self.submitting())

        # 取消的按鈕
        Button(self, text="Cancel", command=self.destroy, width=28, borderwidth=2, font=(SCP, 11)).place(x=23, y=150)

    def _init_record(self, record):
        self.record = record
        self.used_names.set(record[2])
        # 角色名稱已指定時便套用，否則套用前名稱
        character_name = record[4] if record[4] is not None else record[8]
        self.character_selector.set(DBAccessor.select_character_by_specific_column('Nickname', character_name)
                                    if character_name != '' else None)
        # 角色等級/Rank等級未選擇時為空，已選擇便用已選擇
        self.character_level_var.set('' if record[5] is None else record[5])
        self.rank_var.set('' if record[6] is None else record[6])

    def submitting(self):
        self.record[0] = RECORDED
        self.record[4] = convert_to_str(self.character_selector.get().nickname)
        self.record[5] = self.character_level_var.get()
        self.record[6] = self.rank_var.get()
        self.destroy()
        self.callback()
