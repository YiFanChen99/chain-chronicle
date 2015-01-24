# -*- coding: utf-8 -*-
""" 責任包含檢查 DB 內容的正確性  """
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

    def test_select_character_by_specific_column_with_id(self):
        # 正確的 ID
        assert DBAccessor.select_character_by_specific_column('ID', 5002) is not None
        # 故意丟錯的 ID
        self.assertRaises(ValueError, DBAccessor.select_character_by_specific_column, 'ID', 333)

    def test_select_character_by_specific_column_with_full_name(self):
        # 正確的 FullName
        assert DBAccessor.select_character_by_specific_column('FullName', u'救世の聖女リリス') is not None
        # 故意丟錯的 FullName
        self.assertRaises(ValueError, DBAccessor.select_character_by_specific_column, 'FullName', u'聖女')

    def test_select_character_by_specific_column_with_nickname(self):
        # 正確的 Nickname
        assert DBAccessor.select_character_by_specific_column('Nickname', u'聖女') is not None
        # 故意丟錯的 Nickname
        self.assertRaises(ValueError, DBAccessor.select_character_by_specific_column, 'Nickname', u'救世の聖女リリス')