# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import Character
import RecordOfDrawLots

MIN_WIDTH = 760
MIN_HEIGHT = 460


class GUIMain(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        parent.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)
        self.bind('<Configure>', self.do_update_width_and_height)

        self.current_group = 'Empty'  # 檢查用，避免重複讀取
        self.__init_selector()
        self.note_book = None
        self.tabs = []
        self.__current_width = MIN_WIDTH
        self.__current_height = MIN_HEIGHT
        self.update_group()

    # noinspection PyAttributeOutsideInit
    def __init_selector(self):
        # 建立下拉式選單 與 其事件
        self.group_selector = ttk.Combobox(self, state='readonly')
        self.group_selector['values'] = GROUPS
        self.group_selector.place(x=3, y=3)
        self.group_selector.bind('<<ComboboxSelected>>', self.do_selection_handler)
        # 設定初始選項
        self.group_selector.set(GROUPS[0])

        index = 0
        x = 185
        for group in GROUPS:
            button = Button(self, text=group, width=13, font=(MS_JH, 11))
            button.place(x=x, y=-2)

            def do_select_group(obj=self, my_index=index):
                obj.do_select_group(my_index)
            button["command"] = do_select_group

            index += 1
            x += 140

    def do_select_group(self, index):
        self.group_selector.set(GROUPS[index])
        self.do_selection_handler()

    # noinspection PyUnusedLocal
    def do_selection_handler(self, event=None):
        if self.current_group != self.group_selector.get():
            self.update_group()

    def update_group(self):
        self.current_group = self.group_selector.get()

        # 清空舊的 note book
        if self.note_book is not None:
            self.note_book.destroy()
        self.tabs = []

        # 根據選擇，建立新的 note book 並設定位置
        self.note_book = ttk.Notebook(self)
        if self.current_group == GROUP_STATIC_INFO:
            self.__create_group_static_info()
        elif self.current_group == GROUP_ACCOUNT_JP:
            set_suffix_of_account('JP')
            self.__create_group_account()
        elif self.current_group == GROUP_ACCOUNT_TW:
            set_suffix_of_account('TW')
            self.__create_group_account()
        else:
            raise Exception("Wrong group selected!")
        self.adjust_note_book_size()
        self.note_book.place(x=3, y=30)

    # TODO 角色功能表未設計
    def __create_group_static_info(self):
        # 角色
        character_table = Character.Character(self.note_book)
        self.note_book.add(character_table, text=" CharacterTable ")
        self.tabs.append(character_table)
        # 另一個tab的寫法
        # new_tab = Frame(self.note_book)
        # self.note_book.add(new_tab, text=" 名稱 ")

    # TODO 好友、道具、我的角色未設計
    def __create_group_account(self):
        # 抽卡記錄、好友、道具
        record_of_draw_lots = RecordOfDrawLots.RecordOfDrawLots(self.note_book)
        self.note_book.add(record_of_draw_lots, text=" RecordOfDrawLots ")
        self.tabs.append(record_of_draw_lots)
        friend_list = Frame(self.note_book)
        self.note_book.add(friend_list, text=" FriendList ")
        #self.tabs.append(friend_list)
        resources = Frame(self.note_book)
        self.note_book.add(resources, text=" Resources ")
        #self.tabs.append(resources)

    # noinspection PyUnusedLocal
    def do_update_width_and_height(self, event=None):
        if self.winfo_width() > MIN_WIDTH:
            self.__current_width = self.winfo_width()
        else:
            self.__current_width = MIN_WIDTH

        if self.winfo_height() > MIN_HEIGHT:
            self.__current_height = self.winfo_height()
        else:
            self.__current_height = MIN_HEIGHT

        self.adjust_note_book_size()

    def adjust_note_book_size(self):
        widget_width = self.__current_width - 8
        widget_height = self.__current_height - 59
        self.note_book['width'] = widget_width
        self.note_book['height'] = widget_height
        for each_tab in self.tabs:
            each_tab.adjust_view(widget_width, widget_height)


if __name__ == "__main__":
    root = Tk()
    init_size = str(MIN_WIDTH) + 'x' + str(MIN_HEIGHT)
    root.geometry(init_size + '+540+360')
    app = GUIMain(parent=root)
    app.mainloop()