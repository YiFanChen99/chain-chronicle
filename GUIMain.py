# -*- coding: utf-8 -*-

__author__ = 'Ricky Chen'

from Tkinter import *
import tkMessageBox
import ttk
import TabManager


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
        self.group_selector.bind('<<ComboboxSelected>>', self.__selection_handler)
        # 設定初始選項
        self.group_selector.set(self.tab_manager.groups[0])

    def __selection_handler(self, event):
        if self.current_group != self.group_selector.get():
            self.update_group()

    # 未修改
    def update_group(self):
        self.current_group = self.group_selector.get()
        # 清空並重新配置
        self.__reset_empty_group()
        if self.current_group == TabManager.GROUP_ACCOUNT:
            self.__create_group_account()
        elif self.current_group == TabManager.GROUP_CHARACTER:
            self.__create_group_character()
        else:
            raise Exception("Wrong group selected!")

    def __reset_empty_group(self):
        if self.note_book is not None:
            self.note_book.destroy()
        # 建立 note book 並設定位置
        self.note_book = ttk.Notebook(self, width=720, height=360)
        self.note_book.place(x=3, y=30)

    def __create_group_account(self):
        friend_list = Frame(self.note_book)
        self.note_book.add(friend_list, text="FriendList")
        resources = Frame(self.note_book)
        self.note_book.add(resources, text="Resources")

    def __create_group_character(self):
        character_table = Frame(self.note_book)
        self.note_book.add(character_table, text="CharacterTable")


class PopupEntry(object):
    def __init__(self, master):
        top = self.top_window = Toplevel(master)
        self.input = ''
        label = Label(top, text=u"請輸入事件名稱")
        label.pack()
        self.entry = Entry(top)
        self.entry.pack()
        self.entry.focus_force()
        button = Button(top, text='OK', command=self.cleanup)
        button.pack()

    def cleanup(self):
        self.input = self.entry.get()
        self.top_window.destroy()

    def get_input_in_utf8(self):
        return self.input.encode('utf-8')


if __name__ == "__main__":
    root = Tk()
    root.geometry("728x420+540+360")
    app = GUIMain(parent=root)
    app.mainloop()

'''

        self.note = None


        note = ttk.Notebook(root, width=3200, height=500)

        tab1 = Frame(note)
        tab2 = Frame(note)
        tab3 = Frame(note)
        Button(tab1, text='Exit', command=root.destroy).pack(padx=100, pady=100)

        note.add(tab1, text = "Tab One", compound=TOP)
        note.add(tab2, text = "Tab Two")
        note.add(tab3, text = "Tab Three")
        note.place(x=30, y=30)
'''
