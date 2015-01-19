# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import unittest
from ModelUtility.DataObject import *


class DataObjectTest(unittest.TestCase):
    # Character 物件是否涵蓋所有 Character 表內的欄位
    def test_character_object_completed(self):
        character = DBAccessor.execute('select * from Character').fetchone()
        character_object = Character(character[0])
        assert len(character_object.info_list) == len(character),\
            'Info list lens {0}, but Character table has {1} columns.'.format(
                len(character_object.info_list), len(character))
