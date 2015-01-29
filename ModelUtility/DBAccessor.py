# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from ModelUtility.DataObject import *


class DBAccessor():
    DATABASE = sqlite3.connect('data/ChainChronicle.sqlite')

    def __init__(self):
        pass

    @staticmethod
    def execute(command):
        return DBAccessor.DATABASE.execute(command)

    @staticmethod
    def commit():
        return DBAccessor.DATABASE.commit()

    @staticmethod
    def select_character_by_specific_column(column_name, key):
        matched_character = DBAccessor.execute('select * from Character where {0}={1}'.format(
            column_name, convert_datum_to_command(key))).fetchone()
        if matched_character is None:
            raise ValueError('Character with {0} {1} does not existed.'.format(column_name, key))
        return Character(matched_character)

    @staticmethod
    def update_character_into_db(character, commit_followed):
        DBAccessor.execute('update Character{0} where ID={1}'.format(
            convert_data_to_update_command(Character.DB_TABLE, character.info_list), character.c_id))
        if commit_followed:
            DBAccessor.commit()

    @staticmethod
    def select_friend_info_list(db_suffix):
        return [FriendInfo(each) for each in
                DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames!=\'\''.format(
                    ','.join(FriendInfo.DISPLAYED_COLUMNS), db_suffix))]

    @staticmethod
    def select_specific_friend_info(requested_id, db_suffix):
        return FriendInfo(DBAccessor.execute('select {0} from FriendInfo{1} where ID=={2}'.format(
            ','.join(FriendInfo.DISPLAYED_COLUMNS), db_suffix, requested_id)).fetchone())

    @staticmethod
    def select_unused_friend_info(db_suffix):
        return FriendInfo(DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames==\'\''.format(
            ','.join(FriendInfo.DISPLAYED_COLUMNS), db_suffix)).fetchone())

    @staticmethod
    def update_friend_info_into_db(friend_info, db_suffix, commit_followed):
        DBAccessor.execute('update FriendInfo{0}{1} where ID={2}'.format(db_suffix,
            convert_data_to_update_command(FriendInfo.UPDATED_COLUMNS, friend_info.get_updated_info()),
            friend_info.f_id))
        if commit_followed:
            DBAccessor.commit()

    @staticmethod
    def select_new_friend_record_list(db_suffix):
        return [FriendRecord(each) for each in
                DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames!=\'\''.format(
                    ','.join(FriendRecord.FRIEND_INFO_SELECTED_COLUMNS), db_suffix))]

    @staticmethod
    def insert_friend_record_into_db(record, db_suffix, date, commit_followed):
        DBAccessor.execute('insert into FriendRecord{0} ({1}){2}'.format(
            db_suffix, ','.join(FriendRecord.DB_TABLE),
            convert_data_to_insert_command(*record.get_inserted_info(date))))
        if commit_followed:
            DBAccessor.commit()


# 組成「"values(x1,x2,...,xn)"」的字串回傳
def convert_data_to_insert_command(*args):
    command = ' values('
    is_first = True
    for each in args:
        if is_first:
            is_first = False
        else:
            command += ','
        command += convert_datum_to_command(each)
    command += ')'

    return command


# 組成「"set col1=val1,col2=val2,...,coln=valn"」的字串回傳
def convert_data_to_update_command(column_names, values):
    if len(column_names) != len(values):
        raise Exception("Different list lens")

    max_index = len(column_names) - 1
    command = ' set '
    for index in range(0, max_index):
        command += column_names[index] + '='
        command += convert_datum_to_command(values[index]) + ','

    command += column_names[max_index] + '=' + convert_datum_to_command(values[max_index])

    return command


def convert_datum_to_command(datum):
    if datum == 'None':
        return '\"\"'

    try:  # 若為數值類資訊，不必加「"」
        int(datum)
        return str(datum)
    except (ValueError, AttributeError):  # 為字串資料時
        if type(datum) is unicode:
            return '\"' + convert_to_str(datum) + '\"'
        else:
            return '\"' + datum + '\"'


def convert_to_str(value):
    if value is None:
        return ''
    else:
        return value.encode('utf-8')


def convert_str_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d") if date_str is not None else None
