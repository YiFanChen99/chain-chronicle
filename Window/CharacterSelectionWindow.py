# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Window.BasicWindow import *
from Window.CharacterInfoWindow import CharacterInfoWindow
from UIUtility.Selector import ProfessionSelector, RankSelector
from ModelUtility.DBAccessor import DBAccessor
from ModelUtility.Comparator import *


class CharacterSelectionWindow(BasicWindow):
    def __init__(self, character_on_selected):
        BasicWindow.__init__(self, width=316, height=144)
        self.window.title('Character selection')

        self.character_on_selected = character_on_selected

        self.records = None
        self.update_records()
        self.requested_profession = CONDITIONLESS
        self.requested_rank = CONDITIONLESS

        self.__init_widgets()

    def __init_widgets(self):
        self.profession_selector = ProfessionSelector(self.window, self.updating_profession)
        self.profession_selector.place(x=3, y=3)

        self.rank_selector = RankSelector(self.window, self.updating_rank)
        self.rank_selector.place(x=3, y=49)

        Label(self.window, text='Character', width=10, font=("", 12)).place(x=205, y=14)
        self.character_selector = ttk.Combobox(self.window, state='readonly', width=10, justify=CENTER)
        self.character_selector.place(x=209, y=43)

        y_position = 103
        # 送交的按鈕
        button = Button(self.window, text="選擇此角色", width=11, borderwidth=3)
        button.place(x=15, y=y_position)
        button["command"] = self.submitting

        # 新增角色的按鈕
        button = Button(self.window, text="新增角色", width=9, borderwidth=3)
        button.place(x=123, y=y_position)
        button["command"] = self.adding_new_character

        # 取消並結束的按鈕
        button = Button(self.window, text="放棄選擇", width=9, borderwidth=3)
        button.place(x=217, y=y_position)
        button["command"] = self.destroy

    def updating_profession(self, profession):
        self.requested_profession = profession
        self.updating_character_selector()

    def updating_rank(self, rank):
        self.requested_rank = rank
        self.updating_character_selector()

    def updating_character_selector(self):
        character_matched = []
        for character_infos in self.records:
            if (match_requested(character_infos[1], self.requested_profession)) and \
                    (match_requested_rank(character_infos[2], self.requested_rank)):
                character_matched.append(character_infos[0])
        self.character_selector['values'] = character_matched
        self.character_selector.set('')

    # 有選擇的情況下才儲存並回傳，否則彈出錯誤視窗
    def submitting(self):
        if self.character_selector.get() != '':
            self.character_on_selected.set(self.character_selector.get())
            self.destroy()
        else:
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n')

    def adding_new_character(self):
        popup = CharacterInfoWindow()
        self.wait_window(popup)
        self.update_records()
        self.updating_character_selector()

    def update_records(self):
        self.records = DBAccessor.execute('select Nickname, Profession, Rank from Character').fetchall()