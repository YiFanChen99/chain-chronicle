# -*- coding: utf-8 -*-
from Tkinter import *
from Static import *
import FrequentPage
import Utilities
from MainFrameNew.BaseFrame import *
from MainFrameNew.CharacterFrame import CharacterFrame
from MainFrameNew.RecordFrame import RecordFrame
from MainFrameNew.RecordOfDrawLotsFrame import RecordOfDrawLotsFrame
from MainFrameNew.FriendFrame import FriendInfoFrame


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
    Frames = ['Frequent', 'CharacterTable', 'RecordFrame']

    def __init__(self, master, height, **kwargs):
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    def create_main_frame(self, index):
        if index == 0:
            return FrequentPage.Frequent(self.master)
        elif index == 1:
            return CharacterFrame(self.master)
        elif index == 2:
            return RecordFrame(self.master)
        else:
            raise Exception("Wrong group selected!")


class AccountGroupFrame(SubMenuFrame):
    Frames = ['Friend', 'RecordOfDrawLots', 'MyCharacter', 'Resource']

    def __init__(self, master, height, **kwargs):
        SubMenuFrame.__init__(self, master, height=height, **kwargs)

    def create_main_frame(self, index):
        frame_name = self.Frames[index]
        if frame_name == 'MyCharacter':
             # TODO MyCharacter
            return MainFrame(self.master, width=100, height=100, background='blue')
        elif frame_name == 'Resource':
             # TODO Resource
            return MainFrame(self.master, width=100, height=100, background='red')
        elif frame_name == 'RecordOfDrawLots':
            return RecordOfDrawLotsFrame(self.master)
        elif frame_name == 'Friend':
            return FriendInfoFrame(self.master)
        else:
            raise Exception("Wrong group selected!")