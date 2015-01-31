# -*- coding: utf-8 -*-
from Window.CharacterWindow import *
from UIUtility.Selector import ProfessionSelector, RankSelector
from UIUtility.Combobox import FilteredCombobox
from ModelUtility.DBAccessor import *
from ModelUtility.Comparator import *
from ModelUtility.Filter import FilterRuleManager
from Model import CharacterModel


class CharacterSelectorCanvas(Canvas):
    BG = '#%02x%02x%02x' % (200, 200, 200)

    def __init__(self, master, character_selected=None, width=126, height=59, **kwargs):
        Canvas.__init__(self, master, width=width, height=height, bg=self.BG, **kwargs)
        self.pack(fill=BOTH, expand=0)

        self.character_selected = character_selected

        Label(self, text='Character', width=10, font=(SCP, 12), bg=self.BG).place(x=10, y=2)
        self.selected_nickname = StringVar()
        entry = Entry(self, textvariable=self.selected_nickname, width=11, font=(MS_JH, 13),
                      justify=CENTER, state='readonly')
        entry.place(x=7, y=28)
        # 將目前選擇的角色資訊帶過去，並設定 callback，並最後設定焦點為此 canvas
        entry.bind('<ButtonRelease-1>', lambda x: (CharacterSelectionWindow(self, self.set, self.character_selected),
                                                   self.focus_set()))

    def get(self):
        return self.character_selected

    def set(self, character):
        self.character_selected = character
        if character is not None:
            self.selected_nickname.set(character.nickname)
        else:
            self.selected_nickname.set('')


class CharacterSelectionWindow(BasicWindow):
    def __init__(self, master, callback, character_selected, width=422, height=155, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Character selection')
        self.geometry('+780+270')

        self.records = None
        self.update_records()
        self.filter_manager = FilterRuleManager()
        self.filter_manager.set_comparison_rule(0)
        self.filter_manager.set_comparison_rule(1)

        self._init_widgets()
        self._init_character_selected(character_selected)
        self.callback = callback

    def _init_widgets(self):
        self.profession_selector = ProfessionSelector(self, self.updating_request_profession)
        self.profession_selector.place(x=5, y=5)
        self.rank_selector = RankSelector(self, self.updating_request_rank)
        self.rank_selector.place(x=5, y=53)

        Label(self, text='所屬', width=5, font=("", 10)).place(x=221, y=5)
        self.belonged_selector = FilteredCombobox(self, width=7, font=("", 11), justify=CENTER)
        self.belonged_selector['values'] = BELONGEDS
        self.belonged_selector.place(x=213, y=22)
        self.belonged_selector.bind('<<ComboboxSelected>>',
                                    lambda x: self.updating_request_belonged(self.belonged_selector.get()))
        self.belonged_selector.bind('<Return>', lambda x: self.character_selector.focus_set())

        Label(self, text='篩選', width=5, font=("", 11)).place(x=222, y=54)
        self.name_request = StringVar(value='')
        entry = Entry(self, width=8, textvariable=self.name_request, font=("", 12))
        entry.place(x=214, y=73)
        entry.bind('<Return>', lambda x: self.updating_request_name())
        entry.bind('<Escape>', lambda x: (self.name_request.set(''), self.updating_request_name()))

        Label(self, text='Character', width=10, font=("", 12)).place(x=304, y=26)
        self.character_selector = ttk.Combobox(self, state='readonly', width=10, font=("", 12), justify=CENTER)
        self.character_selector.place(x=305, y=48)
        self.character_selector.bind('<Return>', lambda x: self.submitting())

        # 熱鍵，直接指過來
        self.bind('<f>', lambda x: self.character_selector.focus_set())

        y_position = 115
        # 送交的按鈕
        button = Button(self, text="選擇此角色", width=25, borderwidth=3)
        button.place(x=17, y=y_position)
        button["command"] = self.submitting

        # 新增角色的按鈕
        button = Button(self, text="新增角色", width=9, borderwidth=3)
        button.place(x=225, y=y_position)
        button["command"] = lambda: CharacterModel.adding_new_character(
            self, lambda: (self.update_records(), self.updating_character_selector()))

        # 取消並結束的按鈕
        button = Button(self, text="放棄選擇", width=9, borderwidth=3)
        button.place(x=317, y=y_position)
        button["command"] = self.destroy

    def _init_character_selected(self, character_selected):
        if character_selected is None:
            pass
        elif isinstance(character_selected, Character):
            self.profession_selector.select(character_selected.profession)
            self.rank_selector.select(character_selected.rank)
            self.updating_character_selector()
            self.character_selector.set(character_selected.nickname)
        else:
            raise TypeError('In CharacterSelectionWindow, arg: \"character_selected\"')

    def updating_request_profession(self, profession):
        self.filter_manager.set_specific_condition(2, profession)
        self.updating_character_selector()
        self.character_selector.focus_set()

    def updating_request_rank(self, rank):
        self.filter_manager.set_specific_condition(3, rank, match_requested_rank)
        self.updating_character_selector()
        self.character_selector.focus_set()

    def updating_request_belonged(self, belonged):
        self.filter_manager.set_specific_condition(4, belonged)
        self.updating_character_selector()

    def updating_request_name(self):
        self.updating_character_selector()
        self.character_selector.focus_set()

    # 清除原本的選擇，並更新可選擇的角色
    # noinspection PyUnusedLocal
    def updating_character_selector(self, event=None):
        self.character_selector.set('')
        character_matched = []
        for character_infos in self.filter_manager.filter(self.records, self.name_request.get()):
            character_matched.append(character_infos[0])
        self.character_selector['values'] = character_matched

    # 有選擇的情況下才回傳，否則彈出錯誤視窗
    def submitting(self):
        if self.character_selector.get() != '':
            self.callback(CharacterModel.select_character_by_specific_column('Nickname', self.character_selector.get()))
            self.destroy()
        else:
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n', parent=self)

    def update_records(self):
        self.records = DBAccessor.execute(
            'select Nickname, FullName, Profession, Rank, Belonged from Character').fetchall()
