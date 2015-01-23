# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Window.CharacterWindow import *
from UIUtility.Selector import ProfessionSelector, RankSelector
from ModelUtility.DBAccessor import *
from ModelUtility.Comparator import *
from ModelUtility.Filter import FilterManager


class CharacterSelectorCanvas(Canvas):
    BG = '#%02x%02x%02x' % (200, 200, 200)

    def __init__(self, master, character_selected, width=126, height=59, **kwargs):
        Canvas.__init__(self, master, width=width, height=height, **kwargs)
        self['bg'] = self.BG
        self.pack(fill=BOTH, expand=0)

        self.character_selected = character_selected

        Label(self, text='Character', width=10, font=(SCP, 12), bg=self.BG).place(x=10, y=2)
        self.selected_nickname = StringVar()
        entry = Entry(self, textvariable=self.selected_nickname, width=11, font=(MS_JH, 13),
                      justify=CENTER, state='readonly')
        entry.place(x=7, y=28)
        entry.bind('<ButtonRelease-1>', self.invoking_character_selection_window)

    # noinspection PyUnusedLocal
    def invoking_character_selection_window(self, event):
        popup = CharacterSelectionWindow(self, self._set_character_selected, self.character_selected)
        self.wait_window(popup)
        self.selected_nickname.set(self.character_selected.nickname)

    def _set_character_selected(self, character_selected):
        self.character_selected = character_selected


class CharacterSelectionWindow(BasicWindow):
    def __init__(self, master, callback, character_selected, width=316, height=146, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Character selection')
        self.geometry('+780+270')

        self.records = None
        self.update_records()
        self.filter_manager = FilterManager()
        self.filter_manager.set_comparison_rule(0)
        self.filter_manager.set_comparison_rule(1)

        self._init_widgets()
        self._init_character_selected(character_selected)
        self.callback = callback

    def _init_widgets(self):
        self.profession_selector = ProfessionSelector(self, self.updating_request_profession)
        self.profession_selector.place(x=3, y=3)
        self.rank_selector = RankSelector(self, self.updating_request_rank)
        self.rank_selector.place(x=3, y=49)

        Label(self, text='篩選', width=5, font=("", 11)).place(x=208, y=3)
        self.name_request = StringVar(value='')
        entry = Entry(self, width=7, textvariable=self.name_request, font=("", 11))
        entry.place(x=226, y=22)
        entry.bind('<Return>', self.updating_character_selector)

        Label(self, text='Character', width=10, font=("", 12)).place(x=204, y=47)
        self.character_selector = ttk.Combobox(self, state='readonly', width=10, justify=CENTER)
        self.character_selector.place(x=209, y=68)

        y_position = 105
        # 送交的按鈕
        button = Button(self, text="選擇此角色", width=11, borderwidth=3)
        button.place(x=15, y=y_position)
        button["command"] = self.submitting

        # 新增角色的按鈕
        button = Button(self, text="新增角色", width=9, borderwidth=3)
        button.place(x=123, y=y_position)
        button["command"] = self.adding_new_character

        # 取消並結束的按鈕
        button = Button(self, text="放棄選擇", width=9, borderwidth=3)
        button.place(x=217, y=y_position)
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

    def updating_request_rank(self, rank):
        self.filter_manager.set_specific_condition(3, rank, match_requested_rank)
        self.updating_character_selector()

    # 清除原本的選擇，並更新可選擇的角色
    # noinspection PyUnusedLocal
    def updating_character_selector(self, event=None):
        self.character_selector.set('')
        character_matched = []
        for character_infos in self.filter_manager.filter(self.records, convert_to_str(self.name_request.get())):
            character_matched.append(character_infos[0])
        self.character_selector['values'] = character_matched
        self.character_selector.focus_set()

    # 有選擇的情況下才回傳，否則彈出錯誤視窗
    def submitting(self):
        if self.character_selector.get() != '':
            self.callback(DBAccessor.select_character_by_specific_column('Nickname', self.character_selector.get()))
            self.destroy()
        else:
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n', parent=self)

    def adding_new_character(self):
        popup = CharacterInfoWindow(self)
        self.wait_window(popup)
        self.update_records()
        self.updating_character_selector()

    def update_records(self):
        self.records = DBAccessor.execute('select Nickname, FullName, Profession, Rank from Character').fetchall()
