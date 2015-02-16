# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from UI.Utility.Button import ToggleButton
from ModelUtility.DataObject import CharacterPower
from Model import CharacterPowerModel
from Model import CharacterModel


class CharacterPowerFrame(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(6, 31)
        # 滑鼠中鍵事件註冊，設定為更新好友資訊，並選取該列
        self.table_view.bind("<Button-2>", lambda event: self.opening_character_update_window(event))

        self.characters = CharacterPowerModel.select_character_power_list()
        self._init_upper_frame()
        self._updating_status()

    def _init_upper_frame(self):
        self.state_str = StringVar(value='ToFull')
        self.state = ToggleButton(self, textvariable=self.state_str, width=8, font=(SCP, 10), relief=RIDGE)
        self.state.bind('<Button-1>', lambda event: (self.state.toggling(), self._updating_status()))
        self.state.place(x=MIN_WIDTH - 120, y=1)

        button = Button(self, text='新增', width=8, font=(MS_JH, 10))
        button.place(x=MIN_WIDTH - 210, y=1)
        button["command"] = lambda: CharacterPowerModel.open_adding_new_character_power_window(
            self, lambda cp: self.callback_after_adding_character_power(cp))

    def _updating_status(self):
        if self.state.is_selected:
            self.table_model = TableModelAdvance()
            self.table_model.set_columns(CharacterPower.TABLE_VIEW_FULL_COLUMNS, main_column='Character')
            self.table_view.setModel(self.table_model)
            self.state_str.set('ToSimple')
        else:
            self.table_model = TableModelAdvance()
            self.table_model.set_columns(CharacterPower.TABLE_VIEW_SIMPLE_COLUMNS, main_column='Character')
            self.table_view.setModel(self.table_model)
            self.state_str.set('ToFull')

        self.update_table()

    def callback_after_adding_character_power(self, character_power):
        self.characters.append(character_power)
        self.update_table()

    def update_table(self):
        self.table_model.set_rows(self.get_infos_by_state())
        self.table_model.setSortOrder(columnName='DPS', reverse=1)
        self.redisplay_table()
        self.table_view.hide_column('ID')

    def get_infos_by_state(self):
        return [character.get_table_view_full_info() for character in self.characters] if self.state.is_selected else \
            [character.get_table_view_simple_info() for character in self.characters]

    # 編輯角色傷害
    def do_double_clicking(self, event):
        character_power = self.get_corresponding_character_power_in_row(self.table_view.get_row_clicked(event))
        CharacterPowerModel.open_updating_character_power_window(self, character_power, self.update_table)

    def do_dragging_along_right(self, row_number):
        character = self.get_corresponding_character_power_in_row(row_number)
        CharacterPowerModel.delete_character_power_with_conforming(self, character, lambda: (
            self.characters.remove(character), self.update_table()))  # 直接從 list 中拿掉，不用重撈

    # 更改角色資訊
    def opening_character_update_window(self, event):
        character = self.get_corresponding_character_power_in_row(self.table_view.get_row_clicked(event)).character
        CharacterModel.open_updating_character_window(self, character, lambda: None)
        self.table_view.handle_left_click(event)

    def get_corresponding_character_power_in_row(self, row_number):
        selected_id = self.table_model.getCellRecord(row_number, 0)
        selected_level = self.table_model.getCellRecord(row_number, 2)
        for character in self.characters:
            if character.c_id == selected_id and character.level == selected_level:
                return character
