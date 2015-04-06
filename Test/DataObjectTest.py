# -*- coding: utf-8 -*-
import unittest
from Model.CCGameDBTWModel import *
from Model.CCGameDBTWModel import _CGDT_DEFAULT_PATH
from ModelUtility.DataObject import *
from ModelUtility.Utility import load_json


class DBColumnsTest(unittest.TestCase):
    # CGDTCharacter.DB_TABLE 是否涵蓋所有 CCGameDBTW.txt 內的欄位
    def test_cgdt_columns_number(self):
        loaded_data = load_json(_CGDT_DEFAULT_PATH)[0]

        try:
            assert len(loaded_data) == len(CGDTCharacter.DB_TABLE),\
                'CGDTCharacter.DB_TABLE lens {0}, but loaded data has {1} columns.'.format(
                    len(CGDTCharacter.DB_TABLE), len(loaded_data))
        except AssertionError as e:
            for i in range(len(CGDTCharacter.DB_TABLE)):
                print CGDTCharacter.DB_TABLE[i], ': ', loaded_data[i]
            raise e

    # Character.DB_TABLE 是否涵蓋所有 Character 表內的欄位
    def test_character_db_table_completed(self):
        self._assert_db_table_completed('Character', Character.DB_TABLE)

    # RecordOfDrawLots.DB_TABLE 是否涵蓋所有 RecordOfDrawLots 表內的欄位
    def test_record_of_draw_lots_db_table_completed(self):
        self._assert_db_table_completed('RecordOfDrawLots', RecordOfDrawLots.DB_TABLE)

    # EventOfDrawLots.DB_TABLE 是否涵蓋所有 EventOfDrawLots 表內的欄位
    def test_event_of_draw_lots_db_table_completed(self):
        self._assert_db_table_completed('EventOfDrawLots', EventOfDrawLots.DB_TABLE)

    # FriendInfo.DB_TABLE 是否涵蓋所有 FriendInfo 表內的欄位
    def test_friend_info_db_table_completed(self):
        self._assert_db_table_completed('FriendInfoFuji', FriendInfo.DB_TABLE)

    # FriendRecord.DB_TABLE 是否涵蓋所有 FriendRecord 表內的欄位
    def test_friend_record_db_table_completed(self):
        self._assert_db_table_completed('FriendRecordFuji', FriendRecord.DB_TABLE)

    # CharacterPower.DB_TABLE 是否涵蓋所有 CharacterPower 表內的欄位
    def test_character_power_db_table_completed(self):
        self._assert_db_table_completed('CharacterPower', CharacterPower.DB_TABLE)

    @staticmethod
    def _assert_db_table_completed(table_name, table_columns):
        actual_columns = DBAccessor.execute('select * from ' + table_name + ' limit 1').fetchone()
        assert len(table_columns) == len(actual_columns),\
            '{0} table: DB_TABLE lens {1}, but actual DB has {2} columns.'.format(
                table_name, len(table_columns), len(actual_columns))


class CharacterTest(unittest.TestCase):
    # Character 物件是否完整讀出所有 CGDTCharacter 的欄位
    def test_character_object_read_cgdt_character_correctly(self):
        cgdt_character = CCGameDBTWDataOwner().find_character_by_id(5002)
        # Note +1
        expected_length = cgdt_character.fields_number + 1

        character = Character.create_by_cgdt_character(cgdt_character)
        actual_length = len(character.get_updated_info()) + 1  # 加上 ID 欄位
        assert actual_length == expected_length, 'Info list lens {0}, but expected {1}.'.format(
            actual_length, expected_length)

    def test_relation_between_db_table_and_updated_columns(self):
        assert len(Character.DB_TABLE) == len(Character.UPDATED_COLUMNS) + 1


class CGDTCharacterTest(unittest.TestCase):
    # 檢查 CGDTCharacter 能使用的資料欄位個數符合設計
    def test_fields_number_of_cgdt_character(self):
        expected = 23
        actual = CCGameDBTWDataOwner().find_character_by_id(5002).fields_number
        assert actual == expected, 'Fields number of CGDTCharacter expected {0}, but actual {1}'.format(
            expected, actual)


class FriendInfoTest(unittest.TestCase):
    def test_checking_when_get_updated_info(self):
        record = DBAccessor.execute('select {0} from FriendInfoFuji where UsedNames!=\'\''.format(
            ','.join(FriendInfo.SELECTED_COLUMNS))).fetchone()

        FriendInfo(record)  # Pass

        # 故意丟空的 UsedNames
        friend_info = FriendInfo([''] * len(record))
        self.assertRaises(ValueError, lambda: friend_info.get_updated_info())

    def test_relation_between_db_table_and_cleaned_up_columns(self):
        assert len(FriendInfo.DB_TABLE) == len(FriendInfo.CLEANED_UP_COLUMNS) + 1