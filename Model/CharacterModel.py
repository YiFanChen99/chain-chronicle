# -*- coding: utf-8 -*-
from ModelUtility.DBAccessor import *
from Window.CharacterWindow import CharacterWindow
import tkMessageBox


def select_character_by_specific_column(column_name, key):
    matched_character = DBAccessor.execute('select * from Character where {0}={1}'.format(
        column_name, convert_datum_to_command(key))).fetchone()
    if matched_character is None:
        raise ValueError('Character with {0} {1} does not existed.'.format(column_name, key))
    return Character(matched_character)


def select_character_list():
    return [Character(each) for each in
            DBAccessor.execute('select {0} from Character'.format(','.join(Character.DB_TABLE)))]


# CharacterWindow 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_new_character_window(master, callback):
    character = _create_character_with_new_id()
    CharacterWindow(master, character, lambda: (insert_character_into_db(character), callback()))


# CharacterWindow 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_character_window(master, character, callback):
    CharacterWindow(master, character, lambda: (update_character_into_db(character), callback()))


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_character_with_conforming(master, character, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete character 「{0}」？'.format(
            character.nickname.encode('utf-8')), parent=master):
        _delete_character_from_db(character)
        callback()


def _create_character_with_new_id():
    min_id = DBAccessor.execute('select min(ID) from Character').fetchone()[0]
    character_id = 900 if min_id > 999 else min_id - 1
    # noinspection PyTypeChecker
    return Character([character_id] + ([''] * len(Character.UPDATED_COLUMNS)))


def insert_character_into_db(character):
    DBAccessor.execute('insert into Character({0}){1}'.format(
        ','.join(Character.DB_TABLE), convert_data_to_insert_command(character.c_id, *character.get_updated_info())))
    DBAccessor.commit()


def update_character_into_db(character):
    DBAccessor.execute('update Character{0} where ID={1}'.format(
        convert_data_to_update_command(Character.UPDATED_COLUMNS, character.get_updated_info()), character.c_id))
    DBAccessor.commit()


def _delete_character_from_db(character):
    DBAccessor.execute('delete from Character where ID={0}'.format(character.c_id))
    DBAccessor.commit()
