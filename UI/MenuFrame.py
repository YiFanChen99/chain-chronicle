# -*- coding: utf-8 -*-
import os
from ModelUtility.CommonString import *
from ModelUtility.CommonState import *
from ModelUtility.GroupController import *
from UI.Character.CharacterFrame import CharacterFrame
from UI.Record.RecordFrame import RecordFrame
from UI.Friend.FriendFrame import FriendInfoFrame
from UI.MyCharacter.MyCharacterFrame import MyCharacterFrame
from UI.DrawLots.DrawLotsFrame import DrawLotsFrame
from FrequentPage import *

FILE_NAME = 'data\OtherInfo.txt'


class BasicMenuFrame(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, bg='#%02x%02x%02x' % (200, 200, 200), **kwargs)
        self.pack(fill=BOTH, expand=1)

        self.radio_group = RadioGroupController(lambda: self._do_change_frame())
        self._do_init_button_group()

    # Template method
    def _do_init_button_group(self):
        pass

    # Template method
    def _do_change_frame(self):
        pass


class MenuFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)
        self._init_open_txt()

    def _do_init_button_group(self):
        self.buttons = []
        self.buttons.append(Button(self, text='Static Info', width=14, font=(SCP, 11)))
        self.buttons.append(Button(self, text='Fuji Account', width=14, font=(SCP, 11)))
        self.buttons.append(Button(self, text='Yama Account', width=14, font=(SCP, 11)))

        for index, button in enumerate(self.buttons):
            button.place(x=114 + 168 * index, y=-1)
            self.radio_group.group_button(button)

        # 預設選擇第一個
        self.radio_group.selecting_button(0)

    def _init_open_txt(self):
        button = Button(self, text='其他資訊', width=6, font=(MS_JH, 10))
        button.place(x=MIN_WIDTH - 80, y=1)

        def opening_file():
            os.startfile(FILE_NAME)
        button["command"] = opening_file

    def _do_change_frame(self):
        frame_index = self.radio_group.current_selection
        if frame_index == 0:
            new_sub_menu_frame = StaticGroupFrame(self.master)
        elif frame_index == 1:
            set_account('Fuji')
            new_sub_menu_frame = AccountGroupFrame(self.master)
        elif frame_index == 2:
            set_account('Yama')
            new_sub_menu_frame = AccountGroupFrame(self.master)
        else:
            raise IndexError('Wrong index for changing frame.')

        self.master.change_sub_menu_frame(new_sub_menu_frame)


class StaticGroupFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)

    def _do_init_button_group(self):
        self.buttons = []
        self.buttons.append(Button(self, text='Frequent', width=15, font=(SCP, 10)))
        self.buttons.append(Button(self, text='CharacterTable', width=15, font=(SCP, 10)))
        self.buttons.append(Button(self, text='RecordFrame', width=15, font=(SCP, 10)))

        for index, button in enumerate(self.buttons):
            button.place(x=8 + 145 * index, y=1)
            self.radio_group.group_button(button)

        # 預設選擇第一個
        self.radio_group.selecting_button(0)

    def _do_change_frame(self):
        frame_index = self.radio_group.current_selection
        if frame_index == 0:
            new_main_frame = Frequent(self.master)
        elif frame_index == 1:
            new_main_frame = CharacterFrame(self.master)
        elif frame_index == 2:
            new_main_frame = RecordFrame(self.master)
        else:
            raise IndexError('Wrong index for changing frame.')

        self.master.change_main_frame(new_main_frame)


class AccountGroupFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)

    def _do_init_button_group(self):
        self.buttons = []
        self.buttons.append(Button(self, text='Friend', width=16, font=(SCP, 10)))
        self.buttons.append(Button(self, text='RecordOfDrawLots', width=16, font=(SCP, 10)))
        self.buttons.append(Button(self, text='MyCharacter', width=16, font=(SCP, 10)))
        self.buttons.append(Button(self, text='Resource', width=16, font=(SCP, 10)))

        for index, button in enumerate(self.buttons):
            button.place(x=8 + 152 * index, y=1)
            self.radio_group.group_button(button)

        # 預設選擇之前的分頁
        self.radio_group.selecting_button(get_account_page_index())

    def _do_change_frame(self):
        frame_index = self.radio_group.current_selection
        if frame_index == 0:
            new_main_frame = FriendInfoFrame(self.master)
        elif frame_index == 1:
            new_main_frame = DrawLotsFrame(self.master)
        elif frame_index == 2:
            new_main_frame = MyCharacterFrame(self.master)
        elif frame_index == 3:
            new_main_frame = MainFrame(self.master, width=100, height=100, background='red')
        else:
            raise IndexError('Wrong index for changing frame.')

        self.master.change_main_frame(new_main_frame)
        set_account_page_index(frame_index)