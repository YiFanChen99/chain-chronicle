# -*- coding: utf-8 -*-
import sqlite3


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
