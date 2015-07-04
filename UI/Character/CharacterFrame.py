# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from UI.Utility.Combobox import FilteredCombobox
from UI.Utility.Selector import ProfessionSelector, RankSelector
from UI.Character.CharacterWindow import *
from ModelUtility.Comparator import *
from ModelUtility.DataObject import Character
from Model import CharacterModel


class CharacterFrame(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.model = CharacterModel.CharacterFrameModel()
        self.set_table_place(34, 38)
        self.table_model = TableModelAdvance()
        self.table_model.set_columns(Character.TABLE_VIEW_COLUMNS, main_column='Nickname')
        self.table_view.setModel(self.table_model)

        self._init_upper_frame()
        self._init_left_frame()

        self.model.update_data()
        self.update_table()

    def _init_left_frame(self):
        self.character_count = IntVar()
        Label(self, textvariable=self.character_count, width=3, font=(SCP, 9, 'bold')).place(x=5, y=10)

        # 新增記錄的按鈕，分別是日、台服
        button = Button(self, text="新增日服角色", width=2, height=10, wraplength=1, font=(MS_JH, 12))
        button.place(x=4, y=50)
        button["command"] = lambda: open_adding_new_jp_character_window(
            self, lambda character: self.callback_after_adding_character(character))
        button = Button(self, text="台服角色", width=2, height=6, wraplength=1, font=(MS_JH, 11))
        button.place(x=5, y=280)
        button["command"] = lambda: open_adding_new_cn_character_window(
            self, lambda character: self.callback_after_adding_character(character))

    def _init_upper_frame(self):
        filter_frame = Frame(self, width=self['width'], height=40)
        filter_frame.place(x=0, y=0)

        current_x = 45
        self.profession_selector = ProfessionSelector(filter_frame, self.updating_profession)
        self.profession_selector.place(x=current_x, y=-4)

        current_x += 199
        self.rank_selector = RankSelector(filter_frame, self.updating_rank)
        self.rank_selector.place(x=current_x, y=-4)

        # 所屬篩選
        current_x = 448
        Label(filter_frame, text='所屬:', font=(MS_JH, 10)).place(x=current_x + 10, y=-3)
        self.belonged = FilteredCombobox(filter_frame, width=6, justify=CENTER)
        self.belonged['values'] = BELONGEDS
        self.belonged.place(x=current_x, y=16)
        self.belonged.bind('<<ComboboxSelected>>', lambda event: self.updating_belonged())

        # 角色部分名稱篩選
        current_x += 75
        Label(filter_frame, text='篩選:', font=(MS_JH, 12)).place(x=current_x, y=7)
        self.request = StringVar()
        entry = Entry(filter_frame, width=9, textvariable=self.request, font=(MS_JH, 11))
        entry.place(x=current_x + 42, y=9)
        entry.bind('<Return>', lambda event: self.update_table())

        # 清空進行篩選的條件
        button = Button(filter_frame, text="清空條件", width=7, font=(MS_JH, 11))
        button.place(x=667, y=3)
        button["command"] = self.clearing_filters

    def update_table(self):
        # 將符合篩選條件的角色加入欲呈現表格中
        results = self.model.get_displaying_data(self.request.get())
        self.character_count.set(len(results))
        self.table_model.set_rows(results)

        self.table_model.setSortOrder(columnName='Rank', reverse=1)
        self.table_model.setSortOrder(columnName='Profession')

        self.redisplay_table()
        self.table_view.hide_column('ID')

    def callback_after_adding_character(self, character):
        self.model.append(character)
        self.update_table()

    def updating_profession(self, request):
        self.model.set_specific_condition('profession', request)
        self.update_table()

    def updating_rank(self, request):
        self.model.set_specific_condition('rank', request, match_requested_rank)
        self.update_table()

    def updating_belonged(self):
        self.model.set_specific_condition('belonged', self.belonged.get())
        self.update_table()

    def clearing_filters(self):
        self.profession_selector.clean_current_selection()
        self.rank_selector.clean_current_selection()
        self.belonged.set('')
        self.model.clean_specific_condition()
        self.request.set('')
        self.update_table()

    def do_double_clicking(self, event):
        character = self.get_corresponding_character_in_row(self.table_view.get_row_clicked(event))
        open_updating_character_window(self, character, lambda: self.update_table())

    # 主要供方便刪除測試或誤加的角色用，未檢查其他 table 中使用到的該角色
    def do_dragging_along_right(self, row_number):
        character = self.get_corresponding_character_in_row(row_number)
        delete_character_with_conforming(self, character, lambda: (
            self.model.remove(character), self.update_table()))  # 直接從 list 中拿掉，不用重撈

    def get_corresponding_character_in_row(self, row_number):
        selected_id = self.table_model.getCellRecord(row_number, 0)
        return self.model.get_specific_datum('c_id', selected_id)


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_character_with_conforming(master, character, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete character 「{0}」？'.format(
            character.nickname.encode('utf-8')), parent=master):
        CharacterModel.delete_character_from_db(character)
        callback()