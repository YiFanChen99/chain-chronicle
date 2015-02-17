# -*- coding: utf-8 -*-
import tkMessageBox
from ModelUtility.CommonState import *
from ModelUtility.DataObject import CharacterPower
from UI.MyCharacter.CharacterPowerWindow import CharacterPowerWindow
from ModelUtility.DBAccessor import *
from CharacterModel import select_character_by_specific_column


def select_character_power_list():
    return [CharacterPower(each[1:len(each)], select_character_by_specific_column('ID', each[0])) for each in
            DBAccessor.execute('select {0} from CharacterPower where {1}'.format(
                ','.join(CharacterPower.SELECTED_COLUMNS), _get_condition()))]


# 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_new_character_power_window(master, callback):
    cp = CharacterPower.create_empty_character_power()
    CharacterPowerWindow(master, cp, lambda: (_insert_character_power_into_db(cp), callback(cp)))


def _insert_character_power_into_db(cp):
    DBAccessor.execute('insert into CharacterPower({0}){1}'.format(
        ','.join(['Account'] + CharacterPower.UPDATED_COLUMNS),
        convert_data_to_insert_command(get_account(), *cp.get_updated_info())))
    DBAccessor.commit()


# 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_character_power_window(master, character_power, callback):
    CharacterPowerWindow(master, character_power, lambda: (
        _update_character_power_into_db(character_power), callback()))


def _update_character_power_into_db(character_power):
    DBAccessor.execute('update CharacterPower{0} where {1} and CharacterID={2} and Level={3}'.format(
        convert_data_to_update_command(CharacterPower.UPDATED_COLUMNS, character_power.get_updated_info()),
        _get_condition(), character_power.c_id, character_power.level))
    DBAccessor.commit()


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_character_power_with_conforming(master, character_power, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete character 「{0}」？'.format(
            character_power.nickname.encode('utf-8')), parent=master):
        DBAccessor.execute('delete from CharacterPower where CharacterID={0} and Level={1} and {2}'.format(
            character_power.c_id, character_power.level, _get_condition()))
        DBAccessor.commit()
        callback()


def _get_condition():
    return 'Account=' + convert_datum_to_command(get_account())