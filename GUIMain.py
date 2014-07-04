# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
import tkMessageBox
import ttk
import TabManager
import RecordOfDrawLots


class GUIMain(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        parent.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        self.current_group = 'Empty'  # 檢查用，避免重複讀取
        self.tab_manager = TabManager.TabManager()
        self.__init_selector()
        self.note_book = None

        self.update_group()

    def __init_selector(self):
        # 建立下拉式選單 與 其事件
        self.group_selector = ttk.Combobox(self, state='readonly')
        self.group_selector['values'] = self.tab_manager.groups
        self.group_selector.place(x=3, y=3)
        self.group_selector.bind('<<ComboboxSelected>>', self.do_selection_handler)
        # 設定初始選項
        self.group_selector.set(self.tab_manager.groups[0])

    def do_selection_handler(self, event):
        if self.current_group != self.group_selector.get():
            self.update_group()

    def update_group(self):
        self.current_group = self.group_selector.get()

        # 清空舊的 note book
        if self.note_book is not None:
            self.note_book.destroy()

        # 根據選擇，建立新的 note book 並設定位置
        self.note_book = ttk.Notebook(self, width=720, height=360)
        if self.current_group == TabManager.GROUP_STATIC_INFO:
            self.__create_group_static_info()
        elif self.current_group == TabManager.GROUP_FUJI_ACCOUNT:
            self.__create_group_fuji_account()
        else:
            raise Exception("Wrong group selected!")
        self.note_book.place(x=3, y=30)

    # TODO 未設計
    def __create_group_static_info(self):
        # 角色、酒場
        character_table = Frame(self.note_book)
        self.note_book.add(character_table, text=" CharacterTable ")
        place_draw_lots = Frame(self.note_book)
        self.note_book.add(place_draw_lots, text=" 酒廠 ")

    # TODO 好友、道具未設計，可參考抽卡
    def __create_group_fuji_account(self):
        # 好友、抽卡、道具
        friend_list = Frame(self.note_book)
        self.note_book.add(friend_list, text=" FriendList ")
        record_of_draw_lots = RecordOfDrawLots.RecordOfDrawLots(self.note_book)
        self.note_book.add(record_of_draw_lots, text=" RecordOfDrawLots ")
        resources = Frame(self.note_book)
        self.note_book.add(resources, text=" Resources ")


if __name__ == "__main__":
    root = Tk()
    root.geometry("728x420+540+360")
    app = GUIMain(parent=root)
    app.mainloop()
