# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from NewStatic import *
import Character
import RadiobuttonController


class SubMenuFrame(Frame):
    Frames = []

    def __init__(self, master, height,**kwargs):
        Frame.__init__(self, master, width=MIN_WIDTH, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)

        self.radiobuttons = RadiobuttonController.RadiobuttonController(
            self, height=height, bg='#%02x%02x%02x' % (192, 192, 192))

        for page_index in range(len(self.Frames)):
            def do_select_page(obj=self, my_index=page_index):
                obj.do_select_page(my_index)

            self.creat_button_by_index(page_index, self.Frames[page_index], do_select_page)

            # 預設選擇第一個
            if page_index == 0:
                self.radiobuttons.do_select(0, do_select_page)

    def creat_button_by_index(self, index, text, callback):
        self.radiobuttons.create_button(2 + 160 * index, -1, text, callback, width=16)

    # 幫 master 進行切換
    def do_select_page(self, index):
        self.master.update_main_frame(self.create_main_frame(index))

    # Template Method
    def create_main_frame(self, index):
        pass


class StaticGroupFrame(SubMenuFrame):
    Frames = ['CharacterTable']

    def __init__(self, master, height, **kwargs):
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    # TODO 根據index建立並回傳
    def create_main_frame(self, index):
        if index == 0:
            return Frame(width=100, height=100, background='black')
        else:
            raise Exception("Wrong group selected!")


class AccountGroupFrame(SubMenuFrame):
    Frames = ['RecordOfDrawLots', 'FriendList', 'Resources']

    def __init__(self, master, height, account_suffix, **kwargs):
        SubMenuFrame.__init__(self, master, height=height, **kwargs)
        self.account_suffix = account_suffix

    # TODO 根據index建立並回傳
    def create_main_frame(self, index):
        if index == 0:
            return Frame(width=100, height=100, background='black')
        elif index == 1:
            return Frame(width=100, height=100, background='blue')
        elif index == 2:
            return Frame(width=100, height=100, background='red')
        else:
            raise Exception("Wrong group selected!")
