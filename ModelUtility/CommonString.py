# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

# Conditions
CONDITIONLESS = '**'
PROFESSIONS = [u'戰士', u'騎士', u'弓手', u'法師', u'僧侶']
BELONGEDS = [u'副都', u'聖都', u'賢塔', u'山脈', u'湖都', u'精靈島', u'九領', u'義勇軍', u'旅人', u'魔神',
             u'海風', u'大海', u'獸之里']
RANKS = [5, 4, 3, 2, 1]
RANKS_WHEN_DRAW_LOTS = [5, 4, 3]
DRAW_LOTS_COST = [u'石抽', u'券抽', u'未記錄', u'九連抽']
WEAPONS = [u'斬', u'打', u'突', u'弓', u'魔', u'聖', u'拳', u'銃', u'狙']
EXP_GROWN = [u'1250', u'1000', u'900', u'750', u'500', u'300', u'LH', u'鍊金SSR', u'鍊金SR']
ACTIVE_COST = [3, 2, 1]
BOTH_2_AND_1 = '2&1'
RECORDED = ''
UNRECORDED = '未登記'

# UI
MS_JH = 'Microsoft JhengHei'  # 微軟正黑體
SCP = 'Source Code Pro'  # Monokai 所用字型

# Path
IMAGE_FOLDER = 'images/'

# Tables
CHARACTER_DB_TABLE = ['ID', 'FullName', 'Nickname', 'Profession', 'Rank',
                      'Active', 'ActiveCost', 'Passive1', 'Passive2', 'Attachment', 'WeaponType',
                      'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown',
                      'HPGrown', 'AtkSpeed', 'CriticalRate', 'Note', 'Belonged']
FRIEND_MODIFIED_COLUMN = ['UsedNames', 'Excellence', 'Defect', 'AddedDate']
FRIEND_DISPLAYED_COLUMN = ['ID', 'UsedNames', 'Excellence', 'Defect', 'UsedCharacters', 'Rank',
                           'RaisedIn3Weeks', 'RaisedIn2Months', 'AddedDate', 'LastProfession']
DRAW_LOTS_DB_TABLE = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']