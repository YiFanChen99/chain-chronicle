# -*- coding: utf-8 -*-
import os
from ModelUtility.CommonString import *
from ModelUtility.CommonState import *
from ModelUtility.GroupController import *
from UI.Character.CharacterFrame import CharacterFrame
from UI.Record.RecordFrame import RecordFrame
from UI.Friend.FriendFrame import FriendInfoFrame
from UI.MyCharacter.MyCharacterFrame import MyCharacterFrame
from UI.RecordOfDrawLots.RecordOfDrawLotsFrame import RecordOfDrawLotsFrame
from FrequentPage import *

FILE_NAME = 'data\OtherInfo.txt'


class BasicMenuFrame(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, bg='#%02x%02x%02x' % (200, 200, 200), **kwargs)
        self.pack(fill=BOTH, expand=1)

        self._do_init_button_group()

    # Template method
    def _do_init_button_group(self):
        pass


class MenuFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)
        self._init_open_txt()

    def _do_init_button_group(self):
        self.buttons = []
        self.buttons.append(Button(self, text='Static Info', width=14, font=(SCP, 11),
                                   command=lambda: self.master.change_sub_menu_frame(StaticGroupFrame(self.master))))
        self.buttons.append(Button(self, text='Fuji Account', width=14, font=(SCP, 11), command=lambda: (
            set_account('Fuji'), self.master.change_sub_menu_frame(AccountGroupFrame(self.master)))))
        self.buttons.append(Button(self, text='Yama Account', width=14, font=(SCP, 11), command=lambda: (
            set_account('Yama'), self.master.change_sub_menu_frame(AccountGroupFrame(self.master)))))

        radio_group = RadioGroupController(lambda: None)
        for index, button in enumerate(self.buttons):
            button.place(x=115 + 165 * index, y=-1)
            radio_group.group_button(button)

        # 預設選擇第一個
        radio_group.selecting_button(0)
        self.master.change_sub_menu_frame(StaticGroupFrame(self.master))

    def _init_open_txt(self):
        button = Button(self, text='其他資訊', width=6, font=(MS_JH, 10))
        button.place(x=MIN_WIDTH - 80, y=1)

        def opening_file():
            os.startfile(FILE_NAME)
        button["command"] = opening_file


class StaticGroupFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)

    def _do_init_button_group(self):
        self.buttons = []
        self.buttons.append(Button(self, text='Frequent', width=15, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(Frequent(self.master))))
        self.buttons.append(Button(self, text='CharacterTable', width=15, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(CharacterFrame(self.master))))
        self.buttons.append(Button(self, text='RecordFrame', width=15, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(RecordFrame(self.master))))

        radio_group = RadioGroupController(lambda: None)
        for index, button in enumerate(self.buttons):
            button.place(x=8 + 145 * index, y=1)
            radio_group.group_button(button)

        # 預設選擇第一個
        radio_group.selecting_button(0)
        self.master.change_main_frame(Frequent(self.master))


class AccountGroupFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)

    def _do_init_button_group(self):
        self.buttons = []
        self.buttons.append(Button(self, text='Friend', width=16, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(FriendInfoFrame(self.master))))
        self.buttons.append(Button(self, text='RecordOfDrawLots', width=16, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(RecordOfDrawLotsFrame(self.master))))
        self.buttons.append(Button(self, text='MyCharacter', width=16, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(MyCharacterFrame(self.master))))
        self.buttons.append(Button(self, text='Resource', width=16, font=(SCP, 10),
                                   command=lambda: self.master.change_main_frame(
                                       MainFrame(self.master, width=100, height=100, background='red'))))

        radio_group = RadioGroupController(lambda: None)
        for index, button in enumerate(self.buttons):
            button.place(x=8 + 152 * index, y=1)
            radio_group.group_button(button)

        # 預設選擇第一個
        radio_group.selecting_button(0)
        self.master.change_main_frame(FriendInfoFrame(self.master))
