# -*- coding: utf-8 -*-
from ModelUtility.DBAccessor import *
from ModelUtility.DataObject import Character
from ModelUtility.DataHolder import DataHolder


def select_character_by_specific_column(column_name, key):
    matched_character = DBAccessor.execute('select * from Character where {0}={1} limit 1'.format(
        column_name, convert_datum_to_command(key))).fetchone()
    if matched_character is None:
        raise ValueError('Character with {0} {1} does not existed.'.format(column_name, key))
    return Character(matched_character)


def select_character_list():
    return [Character(each) for each in
            DBAccessor.execute('select {0} from Character'.format(','.join(Character.DB_TABLE)))]


def select_character_info_for_character_selector():
    return DBAccessor.execute('select Nickname, FullName, Profession, Rank, Belonged from Character').fetchall()


def insert_character_into_db(character):
    DBAccessor.execute('insert into Character({0}){1}'.format(
        ','.join(Character.DB_TABLE), convert_data_to_insert_command(character.c_id, *character.get_updated_info())))
    DBAccessor.commit()


def update_character_into_db(character):
    DBAccessor.execute('update Character{0} where ID={1}'.format(
        convert_data_to_update_command(Character.UPDATED_COLUMNS, character.get_updated_info()), character.c_id))
    DBAccessor.commit()


def delete_character_from_db(character):
    DBAccessor.execute('delete from Character where ID={0}'.format(character.c_id))
    DBAccessor.commit()


def create_new_jp_character():
    character = Character.create_empty_character()
    min_id = DBAccessor.execute('select min(ID) from Character').fetchone()[0]
    character.c_id = min_id - 1 if min_id < 1000 else 900
    return character


def create_new_cn_character():
    character = Character.create_empty_character()
    max_id = DBAccessor.execute('select max(ID) from Character').fetchone()[0]
    character.c_id = max_id + 1 if max_id > 6000 else 6001
    return character


class CharacterFrameModel(DataHolder):
    def __init__(self):
        DataHolder.__init__(self, data_getter=select_character_list)
        self._init_comparison_rules()

    def _init_comparison_rules(self):
        self.set_comparison_rule('full_name')
        self.set_comparison_rule('nickname')
        self.set_comparison_rule('active')
        self.set_comparison_rule('passive_1')
        self.set_comparison_rule('passive_2')
        self.set_comparison_rule('attachment')

    def get_displaying_data(self, request):
        return [character.get_table_view_info() for character in self.get_matched_data(request)]