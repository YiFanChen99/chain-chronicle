# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from UI.MyCharacter.CharacterWeaponWindow import *
from UI.Utility.Button import ToggleButton
from UI.Utility.Combobox import FilteredCombobox
from ModelUtility.DataObject import CharacterWeapon
from ModelUtility.Filter import FilterRuleManager
from ModelUtility.Comparator import not_match_request
from Model import CharacterWeaponModel


class CharacterWeaponFrame(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(6, 31)
        self.filter_manager = FilterRuleManager()
        self.table_model = TableModelAdvance()
        self.table_model.set_columns(CharacterWeapon.TABLE_VIEW_COLUMNS)
        self.table_view.setModel(self.table_model)

        self.characters = CharacterWeaponModel.select_character_weapon_list()
        self._init_upper_frame()
        self.update_table()

    def _init_upper_frame(self):
        self.insufficiently = ToggleButton(self, text='Insufficiently', width=14, font=(SCP, 8), relief=RIDGE)
        self.insufficiently.bind('<Button-1>', lambda event: (
            self.filter_manager.set_specific_condition(
                'unforged', 0 if self.insufficiently.is_selected else CONDITIONLESS, rule=not_match_request),
            self.update_table()), add='+')
        self.insufficiently.place(x=380, y=3)

        Label(self, text='Type:', width=5, font=(MS_JH, 11)).place(x=510, y=3)
        self.type_selector = FilteredCombobox(self, width=4, font=(MS_JH, 9), justify=CENTER, state='readonly')
        self.type_selector['values'] = WEAPONS
        self.type_selector.place(x=558, y=5)
        self.type_selector.bind('<<ComboboxSelected>>', lambda event: (
            self.filter_manager.set_specific_condition('weapon_type', self.type_selector.get()), self.update_table()))

        button = Button(self, text='新增', width=8, font=(MS_JH, 10))
        button.place(x=640, y=1)
        button["command"] = lambda: open_adding_new_character_weapon_window(
            self, callback=lambda cw: (self.characters.append(cw), self.update_table()))

    def update_table(self):
        results = self.filter_manager.filter(self.characters)
        self.table_model.set_rows([result.get_table_view_info() for result in results])
        self.table_model.setSortOrder(columnName='Total Left', reverse=1)
        self.redisplay_table()

    # 編輯武器狀態
    def do_double_clicking(self, event):
        character_weapon = self.get_corresponding_character_weapon_in_row(self.table_view.get_row_clicked(event))
        open_updating_character_weapon_window(self, character_weapon, self.update_table)

    def do_dragging_along_right(self, row_number):
        character = self.get_corresponding_character_weapon_in_row(row_number)
        delete_character_weapon_with_conforming(self, character, lambda: (
            self.characters.remove(character), self.update_table()))  # 直接從 list 中拿掉，不用重撈

    def get_corresponding_character_weapon_in_row(self, row_number):
        selected_name = self.table_model.getCellRecord(row_number, 0)
        for character in self.characters:
            if character.nickname.encode('utf-8') == selected_name:
                return character


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_character_weapon_with_conforming(master, character_weapon, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete character 「{0}」？'.format(
            character_weapon.nickname.encode('utf-8')), parent=master):
        CharacterWeaponModel.delete_character_weapon_from_db(character_weapon)
        callback()
