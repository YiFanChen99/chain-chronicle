# -*- coding: utf-8 -*-
from ModelUtility.CommonState import *
from ModelUtility.DataObject import CharacterWeapon
from ModelUtility.DBAccessor import *
from CharacterModel import select_character_by_specific_column


def select_character_weapon_list():
    return [CharacterWeapon(each[1:len(each)], select_character_by_specific_column('ID', each[0])) for each in
            DBAccessor.execute('select {0} from CharacterWeapon where {1}'.format(
                ','.join(CharacterWeapon.SELECTED_COLUMNS), _get_condition()))]


def insert_character_weapon_into_db(cw):
    DBAccessor.execute('insert into CharacterWeapon({0}){1}'.format(
        ','.join(['Account'] + CharacterWeapon.UPDATED_COLUMNS),
        convert_data_to_insert_command(get_account(), *cw.get_updated_info())))
    DBAccessor.commit()


def update_character_weapon_into_db(character_weapon, original_c_id):
    DBAccessor.execute('update CharacterWeapon{0} where {1} and CharacterID={2}'.format(
        convert_data_to_update_command(CharacterWeapon.UPDATED_COLUMNS,
                                       character_weapon.get_updated_info()), _get_condition(), original_c_id))
    DBAccessor.commit()


def delete_character_weapon_from_db(character_weapon):
    DBAccessor.execute('delete from CharacterWeapon where CharacterID={0} and {1}'.format(
        character_weapon.c_id, _get_condition()))
    DBAccessor.commit()


def _get_condition():
    return 'Account=' + convert_datum_to_command(get_account())