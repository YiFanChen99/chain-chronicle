# -*- coding: utf-8 -*-
import unittest
from Model import CharacterModel


class CharacterModelTest(unittest.TestCase):
    def test_select_character_by_specific_column_with_id(self):
        # 正確的 ID
        assert CharacterModel.select_character_by_specific_column('ID', 5002) is not None
        # 故意丟錯的 ID
        self.assertRaises(ValueError, CharacterModel.select_character_by_specific_column, 'ID', 333)

    def test_select_character_by_specific_column_with_full_name(self):
        # 正確的 FullName
        assert CharacterModel.select_character_by_specific_column('FullName', u'救世の聖女リリス') is not None
        # 故意丟錯的 FullName
        self.assertRaises(ValueError, CharacterModel.select_character_by_specific_column, 'FullName', u'聖女')

    def test_select_character_by_specific_column_with_nickname(self):
        # 正確的 Nickname
        assert CharacterModel.select_character_by_specific_column('Nickname', u'聖女') is not None
        # 故意丟錯的 Nickname
        self.assertRaises(ValueError, CharacterModel.select_character_by_specific_column, 'Nickname', u'救世の聖女リリス')