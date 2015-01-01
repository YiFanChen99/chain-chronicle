# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

# Conditions
CONDITIONLESS = '**'
PROFESSIONS = [u'戰士', u'騎士', u'弓手', u'法師', u'僧侶']
RANKS = [5, 4, 3, 2, 1]
# RANKS_WHEN_DRAW_LOTS = [5, 4, 3]
# DRAW_LOTS_COST = [u'石抽', u'券抽', u'未記錄', u'九連抽']
WEAPONS = [u'斬', u'打', u'突', u'弓', u'魔', u'聖', u'拳', u'銃', u'狙']
EXP_GROWN = [u'1250', u'1000', u'900', u'750', u'500', u'300', u'LH', u'鍊金SSR', u'鍊金SR']
ACTIVE_COST = [3, 2, 1]
# FRAME_BG_COLOR = '#%02x%02x%02x' % (192, 192, 192)
BOTH_2_AND_1 = '2&1'
# MS_JH = 'Microsoft JhengHei'  # 微軟正黑體

# Path
IMAGE_FOLDER = 'images/'

# Tables
CHARACTER_DB_TABLE = ['FullName', 'Nickname', 'Profession', 'Rank',
                      'Active', 'ActiveCost', 'Passive1', 'Passive2', 'Attachment', 'WeaponType',
                      'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown',
                      'HPGrown', 'AtkSpeed', 'CriticalRate', 'Note']