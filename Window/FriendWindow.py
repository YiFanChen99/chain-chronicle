# -*- coding: utf-8 -*-
from BasicWindow import *
from UIUtility.CharacterSelector import CharacterSelectorCanvas
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *
from Model import CharacterModel


class FriendInfoUpdaterWindow(BasicWindow):
    def __init__(self, master, friend_info, callback, width=347, height=283, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Friend Info')
        self.geometry('+750+260')

        self._init_widget()
        self._init_info(friend_info)
        self.callback = callback

    def _init_widget(self):
        current_y = 11
        Label(self, width=12, text='UsedNames:', font=(SCP, 12)).place(x=5, y=current_y)
        self.used_names = StringVar()
        Entry(self, width=19, textvariable=self.used_names, font=(MS_JH, 12))\
            .place(x=34, y=current_y + 25)

        Label(self, width=11, text='AddedDate', font=(SCP, 10)).place(x=226, y=current_y + 6)
        self.added_date = StringVar()
        Entry(self, width=10, textvariable=self.added_date, font=(MS_JH, 10), justify=CENTER)\
            .place(x=231, y=current_y + 26)

        current_y += 69
        label_x = 7
        entry_x = label_x + 56

        Label(self, width=6, text='Exce.', font=(SCP, 10)).place(x=label_x, y=current_y)
        self.excellence = StringVar()
        excellence_entry = Entry(self, width=28, textvariable=self.excellence, font=(MS_JH, 12), justify=CENTER)
        excellence_entry.place(x=entry_x, y=current_y)
        excellence_entry.bind('<Return>', lambda x: defect_entry.focus_set())

        current_y += 36
        Label(self, width=6, text='Defe.', font=(SCP, 10)).place(x=label_x, y=current_y)
        self.defect = StringVar()
        defect_entry = Entry(self, width=28, textvariable=self.defect, font=(MS_JH, 12), justify=CENTER)
        defect_entry.place(x=entry_x, y=current_y)
        defect_entry.bind('<Return>', self.submitting)
        defect_entry.bind('<Return>', lambda x: relation_entry.focus_set())

        current_y += 36
        Label(self, width=6, text='Rela.', font=(SCP, 10)).place(x=label_x, y=current_y)
        self.relation = StringVar()
        relation_entry = Entry(self, width=28, textvariable=self.relation, font=(MS_JH, 12), justify=CENTER)
        relation_entry.place(x=entry_x, y=current_y)
        relation_entry.bind('<Return>', lambda x: offline_entry.focus_set())

        current_y += 36
        Label(self, width=6, text='Off .', font=(SCP, 10)).place(x=label_x, y=current_y)
        self.offline = StringVar()
        offline_entry = Entry(self, width=28, textvariable=self.offline, font=(MS_JH, 12), justify=CENTER)
        offline_entry.place(x=entry_x, y=current_y)
        offline_entry.bind('<Return>', self.submitting)

        # 送出、取消的按鈕
        current_y += 46
        Button(self, text="Submit", command=self.submitting, width=20, relief=RIDGE,
               font=(SCP, 11)).place(x=19, y=current_y)
        Button(self, text="Cancel", command=self.destroy, width=10, relief=RIDGE,
               font=(SCP, 11)).place(x=226, y=current_y)

    def _init_info(self, friend_info):
        self.friend_info = friend_info
        self.used_names.set(friend_info.used_names)
        self.added_date.set(friend_info.added_date)
        self.excellence.set(friend_info.excellence)
        self.defect.set(friend_info.defect)
        self.relation.set(friend_info.relation)
        self.offline.set(friend_info.offline)

    # noinspection PyUnusedLocal
    def submitting(self, *args):
        # 進行檢查，不允許 UsedNames 為空
        if not self.used_names.get():
            tkMessageBox.showwarning("Can not submit", 'UsedNames 不能為空', parent=self)
            return

        # 更新回原記錄
        self.friend_info.used_names = self.used_names.get()
        self.friend_info.excellence = self.excellence.get()
        self.friend_info.defect = self.defect.get()
        self.friend_info.added_date = self.added_date.get()
        self.friend_info.relation = self.relation.get()
        self.friend_info.offline = self.offline.get()

        self.destroy()
        self.callback()


class FriendRecordUpdaterWindow(BasicWindow):
    def __init__(self, master, record, callback, width=309, height=198, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Friend Record')
        self.geometry('+760+230')

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
        if isinstance(record, FriendRecord):
            self.record = record
            self.used_names.set(record.used_names)
            self.character_selector.set(CharacterModel.select_character_by_specific_column(
                'Nickname', record.current_character) if record.current_character != '' else None)
            self.character_level_var.set(record.current_character_level)
            self.rank_var.set(record.current_rank)
        else:
            raise TypeError('In FriendRecordUpdaterWindow, arg: \"record\"')

    def submitting(self):
        # 確認 rank 沒有異常
        if self.record.is_unusual_rank(self.rank_var.get()):
            message = 'Friend {0} has rank {1} with previous rank {2}.\nSure to continue?'.format(
                self.used_names.get().encode('utf-8'), self.rank_var.get(), self.record.last_rank)
            if not tkMessageBox.askyesno('Unusual rank', message, parent=self):
                return

        self.record.record(self.character_selector.get().nickname, self.character_level_var.get(), self.rank_var.get())
        self.destroy()
        self.callback()
