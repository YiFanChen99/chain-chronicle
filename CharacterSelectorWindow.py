# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from BasicWindow import *
import UpdateCharacterWindow


class CharacterSelectorWindow(BasicWindow):
    def __init__(self, character_selected):
        BasicWindow.__init__(self, width=302, height=123)
        self.window.title('Selecting character')

        self.character_selected = character_selected

        self.characters = None
        self.update_characters()

        self.__init_widgets()

    # noinspection PyAttributeOutsideInit
    def __init_widgets(self):
        # 各 Column 的標題: 職業, 等級, 角色
        Label(self.window, text='Profession', width=7, font=("", 12)).place(x=21, y=9)
        Label(self.window, text='Rank', width=5, font=("", 12)).place(x=111, y=9)
        Label(self.window, text='Character', width=11, font=("", 12)).place(x=179, y=9)

        # 選擇職業
        self.profession_selector = ttk.Combobox(self.window, state='readonly', width=7, justify=CENTER)
        self.profession_selector['values'] = PROFESSIONS
        self.profession_selector.place(x=19, y=40)
        self.profession_selector.bind('<<ComboboxSelected>>', self.updating_character_selector)

        # 選擇等級
        self.rank_selector = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.rank_selector['values'] = RANKS
        self.rank_selector.place(x=110, y=40)
        self.rank_selector.bind('<<ComboboxSelected>>', self.updating_character_selector)

        # 選擇角色
        self.character_selector = ttk.Combobox(self.window, state='readonly', width=10, justify=CENTER)
        self.character_selector.place(x=188, y=40)

        # 送交的按鈕
        button = Button(self.window, text="選擇此角色", width=11, borderwidth=3)
        button.place(x=13, y=80)
        button["command"] = self.submitting

        # 新增角色的按鈕
        button = Button(self.window, text="新增角色", width=9, borderwidth=3)
        button.place(x=118, y=80)
        button["command"] = self.adding_new_character

        # 取消並結束的按鈕
        button = Button(self.window, text="放棄選擇", width=9, borderwidth=3)
        button.place(x=208, y=80)
        button["command"] = self.destroy

    def submitting(self):
        if self.is_character_legal():
            self.character_selected.set(self.character_selector.get())
            self.destroy()

    def is_character_legal(self):
        if self.character_selector.get() == '':
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n')
            return False
        else:
            return True

    # noinspection PyUnusedLocal
    def updating_character_selector(self, event=None):
        requested_profession = self.profession_selector.get()
        requested_rank = self.rank_selector.get()

        # 依序對職業與等級進行篩選(if需要)
        character_matched = []
        for character_infos in self.characters:
            if (requested_profession == '' or requested_profession == character_infos[1]) and \
                    (requested_rank == '' or int(requested_rank) == character_infos[2]):
                character_matched.append(character_infos[0])

        self.character_selector['values'] = character_matched
        self.character_selector.set('')

    def adding_new_character(self):
        popup = UpdateCharacterWindow.UpdateCharacterWindow()
        self.wait_window(popup)
        self.update_characters()
        self.updating_character_selector()

    def update_characters(self):
        self.characters = DATABASE.execute('select Nickname, Profession, Rank from Character').fetchall()