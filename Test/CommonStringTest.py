# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

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
