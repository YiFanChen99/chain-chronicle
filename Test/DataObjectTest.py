# -*- coding: utf-8 -*-
import unittest
from ModelUtility.CCGameDBTW import *


class DataObjectTest(unittest.TestCase):
    # Character 物件是否完整讀出所有 CGDTCharacter 的欄位
    def test_character_object_read_cgdt_character_correctly(self):
        cgdt_character = CCGameDBTWDataOwner().find_character_by_id(5002)
        # Note +1. passive_1/2_level, attached_cost -3
        expected_length = cgdt_character.fields_number - 3 + 1

        character = Character(cgdt_character=cgdt_character)
        assert len(character.info_list) == expected_length,\
            'Info list lens {0}, but expected {1}.'.format(len(character.info_list), expected_length)

    # CGDTCharacter.DB_TABLE 是否涵蓋所有 CCGameDBTW.txt 內的欄位
    def test_cgdt_columns_number(filename):
        loaded_data = load_json(CGDT_DEFAULT_PATH)[0]

        try :
            assert len(loaded_data) == len(CGDTCharacter.DB_TABLE),\
                'CGDTCharacter.DB_TABLE lens {0}, but loaded data has {1} columns.'.format(len(CGDTCharacter.DB_TABLE), len(loaded_data))
        except AssertionError as e:
            for i in range(len(CGDTCharacter.DB_TABLE)):
                print CGDTCharacter.DB_TABLE[i], ': ', loaded_data[i]
            raise e

    # 檢查 CGDTCharacter 能使用的資料欄位個數符合設計
    def test_fields_number_of_cgdt_character(self):
        expected = 23
        actual = CCGameDBTWDataOwner().find_character_by_id(5002).fields_number
        assert actual == expected, 'Fields number of CGDTCharacter expected {0}, but actual {1}'.format(
            expected, actual)

    # Character.DB_TABLE 是否涵蓋所有 Character 表內的欄位
    def test_character_db_table_completed(self):
        character = DBAccessor.execute('select * from Character').fetchone()
        assert len(Character.DB_TABLE) == len(character),\
            'Character.DB_TABLE lens {0}, but Character table has {1} columns.'.format(
                len(Character.DB_TABLE), len(character))

    # DRAW_LOTS_DB_TABLE 是否涵蓋所有 RecordOfDrawLots 表內的欄位
    def test_draw_lots_db_table_completed(self):
        draw_lots = DBAccessor.execute('select * from RecordOfDrawLotsJP').fetchone()
        assert len(DRAW_LOTS_DB_TABLE) == len(draw_lots),\
            'DRAW_LOTS_DB_TABLE lens {0}, but RecordOfDrawLots table has {1} columns.'.format(
                len(DRAW_LOTS_DB_TABLE), len(draw_lots))

    # FriendInfo.DB_TABLE 是否涵蓋所有 Friend 表內的欄位
    def test_friend_info_db_table_completed(self):
        friend = DBAccessor.execute('select * from FriendJP').fetchone()
        assert len(FriendInfo.DB_TABLE) == len(friend),\
            'FriendInfo.DB_TABLE lens {0}, but RecordOfDrawLots table has {1} columns.'.format(
                len(FriendInfo.DB_TABLE), len(friend))

    # FriendRecord.DB_TABLE 是否涵蓋所有 FriendRecord 表內的欄位
    def test_friend_record_db_table_completed(self):
        friend_record = DBAccessor.execute('select * from FriendRecordJP').fetchone()
        assert len(FriendRecord.DB_TABLE) == len(friend_record),\
            'FriendRecord.DB_TABLE lens {0}, but RecordOfDrawLots table has {1} columns.'.format(
                len(FriendRecord.DB_TABLE), len(friend_record))
