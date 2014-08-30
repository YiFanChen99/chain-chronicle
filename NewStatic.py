# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import sqlite3

MIN_WIDTH = 760
MIN_HEIGHT = 460

PROFESSIONS = [u'戰士', u'騎士', u'弓手', u'法師', u'僧侶']
RANKS = [5, 4, 3, 2, 1]
RANKS_WHEN_DRAW_LOTS = [5, 4, 3]
DRAW_LOTS_COST = [u'石抽', u'券抽', u'未記錄', u'九連抽']
WEAPONS = [u'斬', u'打', u'突', u'弓', u'魔', u'聖', u'拳', u'銃', u'狙']
EXP_GROWN = [u'1000', u'750', u'500', u'300', u'LH']
ACTIVE_COST = [3, 2, 1]

DATABASE = sqlite3.connect('ChainChronicle.sqlite')
MS_JH = 'Microsoft JhengHei'  # 微軟正黑體


def convert_to_str(value):
    if value is None:
        return ''
    else:
        return value.encode('utf-8')


# noinspection PyUnusedLocal
def do_nothing(obj=None, event=None):
    pass


def insert_with_empty_str(the_list):
    result = ['']
    result.extend(the_list)
    return result