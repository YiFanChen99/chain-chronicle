# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import unittest
from ModelUtility.DataObject import *
from ModelUtility.CCGameDBTW import CCGameDBTWDataOwner


class DataObjectTest(unittest.TestCase):
    # Character 物件是否完整讀出所有 CGDTCharacter 的欄位
    def test_character_object_read_cgdt_character_correctly(self):
        cgdt_character = CCGameDBTWDataOwner().find_character_by_id(5002)
        # Note +1. passive_1/2_level, attached_cost -3
        expected_length = cgdt_character.fields_number - 3 + 1

        character = Character(cgdt_character=cgdt_character)
        assert len(character.info_list) == expected_length,\
            'Info list lens {0}, but expected {1}.'.format(len(character.info_list), expected_length)

    # 檢查 CGDTCharacter 能使用的資料欄位個數符合設計
    def test_fields_number_of_cgdt_character(self):
        expected = 23
        actual = CCGameDBTWDataOwner().find_character_by_id(5002).fields_number
        assert actual == expected, 'Fields number of CGDTCharacter expected {0}, but actual {1}'.format(
            expected, actual)
