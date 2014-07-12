# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import sqlite3

PROFESSIONS = [u'戰士', u'騎士', u'弓手', u'法師', u'僧侶']
RANKS = [5, 4, 3, 2, 1]
RANKS_WHEN_DRAW_LOTS = [5, 4, 3]
DRAW_LOTS_COST = [u'石抽', u'券抽', u'未記錄']
WEAPONS = [u'斬', u'打', u'突', u'弓', u'魔', u'聖']
EXP_GROWN = [u'1000', u'750', u'500', u'300', u'LH']

DATABASE = sqlite3.connect('ChainChronicle.sqlite')
CURSOR = DATABASE.cursor()


def commit():
    DATABASE.commit()


def execute(sql_commend):
    return CURSOR.execute(sql_commend)


def convert_to_str(value):
    if value is None:
        return ''
    else:
        return value.encode('utf-8')


def destroy_frame(obj):
    if obj is not None:
        obj.destroy()