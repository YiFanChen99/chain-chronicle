# -*- coding: utf-8 -*-
import sqlite3
from ModelUtility.DataObject import *
from ModelUtility.CommonState import *


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
    def commit_if_requested(requested):
        if requested:
            return DBAccessor.DATABASE.commit()

    @staticmethod
    def select_friend_info_list():
        return [FriendInfo(each) for each in
                DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames!=\'\''.format(
                    ','.join(FriendInfo.SELECTED_COLUMNS), get_db_suffix()))]

    @staticmethod
    def select_specific_friend_info(requested_id):
        return FriendInfo(DBAccessor.execute('select {0} from FriendInfo{1} where ID=={2}'.format(
            ','.join(FriendInfo.SELECTED_COLUMNS), get_db_suffix(), requested_id)).fetchone())

    @staticmethod
    def select_unused_friend_info():
        return FriendInfo(DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames==\'\''.format(
            ','.join(FriendInfo.SELECTED_COLUMNS), get_db_suffix())).fetchone())

    @staticmethod
    def update_friend_info_into_db(friend_info, commit_followed):
        DBAccessor.execute('update FriendInfo{0}{1} where ID={2}'.format(get_db_suffix(), convert_data_to_update_command(
            FriendInfo.UPDATED_COLUMNS, friend_info.get_updated_info()), friend_info.f_id))
        DBAccessor.commit_if_requested(commit_followed)

    @staticmethod
    def select_new_friend_record_list():
        return [FriendRecord(each) for each in
                DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames!=\'\''.format(
                    ','.join(FriendRecord.FRIEND_INFO_SELECTED_COLUMNS), get_db_suffix()))]

    @staticmethod
    def insert_friend_record_into_db(record, the_date, commit_followed):
        DBAccessor.execute('insert into FriendRecord{0} ({1}){2}'.format(
            get_db_suffix(), ','.join(FriendRecord.DB_TABLE),
            convert_data_to_insert_command(*record.get_inserted_info(the_date))))
        DBAccessor.commit_if_requested(commit_followed)


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
