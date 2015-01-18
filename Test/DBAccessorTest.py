# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'
''' 責任包含檢查 DB 內容的正確性  '''

import unittest
from ModelUtility.DBAccessor import *


class DBAccessorTest(unittest.TestCase):
    # 是否有未設定好的角色
    def test_valid_id_and_full_name(self):
        characters = DBAccessor.execute('select ID, FullName from Character').fetchall()
        for character in characters:
            the_id = character[0]
            assert the_id is not None, 'ID is None, FullName=' + character[1]

            name = character[1]
            assert name is not None, 'FullName is None when ID={0}'.format(the_id)
