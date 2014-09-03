# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import PowerConverter
import Utilities
import Character
import RecordOfDrawLots


class SubMenuFrame(Frame):
    Frames = []

    def __init__(self, master, height, **kwargs):
        Frame.__init__(self, master, width=MIN_WIDTH, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)

        self.radiobuttons = Utilities.RadiobuttonController(self, height=height, button_type=2)

        for page_index in range(len(self.Frames)):
            def do_select_page(obj=self, my_index=page_index):
                obj.do_select_page(my_index)

            self.creat_button_by_index(page_index, self.Frames[page_index], do_select_page)

            # 預設選擇第一個
            if page_index == 0:
                self.radiobuttons.do_select(0, do_select_page)

    def creat_button_by_index(self, index, text, callback):
        self.radiobuttons.create_button(6 + 145 * index, -1, text, callback, width=16)

    # 幫 master 進行切換
    def do_select_page(self, index):
        self.master.update_main_frame(self.create_main_frame(index))

    # Template Method
    def create_main_frame(self, index):
        pass


class StaticGroupFrame(SubMenuFrame):
    Frames = ['CharacterTable', 'PowerConverter']

    def __init__(self, master, height, **kwargs):
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    def create_main_frame(self, index):
        if index == 0:
            return Character.Character(self.master)
        elif index == 1:
            return PowerConverter.PowerConverter(self.master)
        else:
            raise Exception("Wrong group selected!")


class AccountGroupFrame(SubMenuFrame):
    Frames = ['RecordOfDrawLots', 'FriendList', 'Resources']

    def __init__(self, master, height, db_suffix, **kwargs):
        self.db_suffix = db_suffix
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    def create_main_frame(self, index):
        if index == 0:
            return RecordOfDrawLots.RecordOfDrawLots(self.master, self.db_suffix)
        elif index == 1:
             # TODO FriendList
            return RecordOfDrawLots.MainFrame(self.master, self.db_suffix, width=100, height=100, background='blue')
        elif index == 2:
             # TODO Resources
            return RecordOfDrawLots.MainFrame(self.master, self.db_suffix, width=100, height=100, background='red')
        else:
            raise Exception("Wrong group selected!")