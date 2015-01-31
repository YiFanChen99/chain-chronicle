# -*- coding: utf-8 -*-
from ModelUtility.DBAccessor import *
from Window.CharacterWindow import CharacterWindow


def select_character_by_specific_column(column_name, key):
    matched_character = DBAccessor.execute('select * from Character where {0}={1}'.format(
        column_name, convert_datum_to_command(key))).fetchone()
    if matched_character is None:
        raise ValueError('Character with {0} {1} does not existed.'.format(column_name, key))
    return Character(matched_character)


def select_character_list():
    return [Character(each) for each in
            DBAccessor.execute('select {0} from Character'.format(','.join(Character.DB_TABLE)))]


def delete_character_from_db(character, commit_followed):
    DBAccessor.execute('delete from Character where ID={0}'.format(character.c_id))
    DBAccessor.commit_if_requested(commit_followed)


def update_character_into_db(character, commit_followed):
    DBAccessor.execute('update Character{0} where ID={1}'.format(
        convert_data_to_update_command(Character.UPDATED_COLUMNS, character.get_updated_info()), character.c_id))
    DBAccessor.commit_if_requested(commit_followed)


# 若 CharacterWindow 送出新增要求，才新增至 DB 並通知 caller
def adding_new_character(master, callback):
    character = _create_character_with_new_id()
    CharacterWindow(master, character, lambda: (_insert_character_into_db(character), callback()))


def _create_character_with_new_id():
    min_id = DBAccessor.execute('select min(ID) from Character').fetchone()[0]
    character_id = 900 if min_id > 999 else min_id - 1
    # noinspection PyTypeChecker
    return Character([character_id] + ([''] * len(Character.UPDATED_COLUMNS)))


def _insert_character_into_db(character):
    DBAccessor.execute('insert into Character({0}){1}'.format(
        ','.join(Character.DB_TABLE), convert_data_to_insert_command(character.c_id, *character.get_updated_info())))
    DBAccessor.commit()