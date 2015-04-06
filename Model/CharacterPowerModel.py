# -*- coding: utf-8 -*-
from ModelUtility.CommonState import *
from ModelUtility.DataObject import CharacterPower
from ModelUtility.DBAccessor import *
from CharacterModel import select_character_by_specific_column


def select_character_power_list():
    return [CharacterPower(each[1:len(each)], select_character_by_specific_column('ID', each[0])) for each in
            DBAccessor.execute('select {0} from CharacterPower where {1}'.format(
                ','.join(CharacterPower.SELECTED_COLUMNS), _get_condition()))]


def insert_character_power_into_db(cp):
    DBAccessor.execute('insert into CharacterPower({0}){1}'.format(
        ','.join(['Account'] + CharacterPower.UPDATED_COLUMNS),
        convert_data_to_insert_command(get_account_name(), *cp.get_updated_info())))
    DBAccessor.commit()


def update_character_power_into_db(character_power, original_c_id, original_level):
    DBAccessor.execute('update CharacterPower{0} where {1} and CharacterID={2} and Level={3}'.format(
        convert_data_to_update_command(CharacterPower.UPDATED_COLUMNS, character_power.get_updated_info()),
        _get_condition(), original_c_id, original_level))
    DBAccessor.commit()


def delete_character_power_from_db(character_power):
    DBAccessor.execute('delete from CharacterPower where CharacterID={0} and Level={1} and {2}'.format(
        character_power.c_id, character_power.level, _get_condition()))
    DBAccessor.commit()


def _get_condition():
    return 'Account=' + convert_datum_to_command(get_account_name())