# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import FrequentPage
import Utilities
import CharacterPage
import RecordOfDrawLotsPage
import FriendPage


class SubMenuFrame(Frame):
    Frames = []

    def __init__(self, master, height, **kwargs):
        Frame.__init__(self, master, width=MIN_WIDTH, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)

        self.radiobuttons = Utilities.RadiobuttonController(self, width=MIN_WIDTH, height=height, button_type=2)
        self.radiobuttons.place(x=0, y=0)
        for page_index in range(len(self.Frames)):
            def selecting_page(obj=self, my_index=page_index):
                obj.selecting_page(my_index)

            self.creat_button_by_index(page_index, self.Frames[page_index], selecting_page)

            # 預設選擇第一個
            if page_index == 0:
                self.radiobuttons.selecting_button(0, selecting_page)

    def creat_button_by_index(self, index, text, callback):
        self.radiobuttons.create_button(6 + 137 * index, -1, text, callback, width=15)

    # 幫 master 進行切換
    def selecting_page(self, index):
        self.master.update_main_frame(self.create_main_frame(index))

    # Template Method
    def create_main_frame(self, index):
        pass


class StaticGroupFrame(SubMenuFrame):
    Frames = ['Frequent', 'CharacterTable']

    def __init__(self, master, height, **kwargs):
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    def create_main_frame(self, index):
        if index == 0:
            return FrequentPage.Frequent(self.master)
        elif index == 1:
            return CharacterPage.Character(self.master)
        else:
            raise Exception("Wrong group selected!")


class AccountGroupFrame(SubMenuFrame):
    Frames = ['MyCharacter', 'Resource', 'RecordOfDrawLots', 'Friend']

    def __init__(self, master, height, db_suffix, **kwargs):
        self.db_suffix = db_suffix
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    def create_main_frame(self, index):
        if index == 0:
             # TODO MyCharacter
            return RecordOfDrawLotsPage.MainFrame(self.master, self.db_suffix, width=100, height=100, background='blue')
        elif index == 1:
             # TODO Resource
            return RecordOfDrawLotsPage.MainFrame(self.master, self.db_suffix, width=100, height=100, background='red')
        elif index == 2:
            return RecordOfDrawLotsPage.RecordOfDrawLots(self.master, self.db_suffix)
        elif index == 3:
            return FriendPage.FriendInfo(self.master, self.db_suffix)
        else:
            raise Exception("Wrong group selected!")