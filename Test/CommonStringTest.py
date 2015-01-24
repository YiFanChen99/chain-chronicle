# -*- coding: utf-8 -*-
import unittest
from ModelUtility.DBAccessor import DBAccessor
from ModelUtility.CommonString import *


class CommonStringTest(unittest.TestCase):
    # CHARACTER_DB_TABLE 是否涵蓋所有 Character 表內的欄位
    def test_character_db_table_completed(self):
        character = DBAccessor.execute('select * from Character').fetchone()
        assert len(CHARACTER_DB_TABLE) == len(character),\
            'CHARACTER_DB_TABLE lens {0}, but Character table has {1} columns.'.format(
                len(CHARACTER_DB_TABLE), len(character))

    # DRAW_LOTS_DB_TABLE 是否涵蓋所有 RecordOfDrawLots 表內的欄位
    def test_draw_lots_db_table_completed(self):
        draw_lots = DBAccessor.execute('select * from RecordOfDrawLotsJP').fetchone()
        assert len(DRAW_LOTS_DB_TABLE) == len(draw_lots),\
            'DRAW_LOTS_DB_TABLE lens {0}, but RecordOfDrawLots table has {1} columns.'.format(
                len(DRAW_LOTS_DB_TABLE), len(draw_lots))
