# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import sqlite3
from datetime import datetime, timedelta

PROFESSIONS = [u'戰士', u'騎士', u'弓手', u'法師', u'僧侶']
RANKS = [5, 4, 3, 2, 1]
RANKS_WHEN_DRAW_LOTS = [5, 4, 3]
DRAW_LOTS_COST = [u'石抽', u'券抽', u'未記錄']
WEAPONS = [u'斬', u'打', u'突', u'弓', u'魔', u'聖']
EXP_GROWN = [u'1000', u'750', u'500', u'300', u'LH']

DATABASE = sqlite3.connect('ChainChronicle.sqlite')


# 組成「"x1,x2,...,xn"」的字串回傳
def convert_data_to_insert_command(*arguments):
    command = ' values('
    is_first = True
    for each in arguments:
        if is_first:
            is_first = False
        else:
            command += ','
        command += convert_datum_to_command(each)
    command += ')'

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


def destroy_frame(obj):
    if obj is not None:
        obj.destroy()


def convert_str_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y/%m/%d")


def do_nothing(obj=None, event=None):
    pass