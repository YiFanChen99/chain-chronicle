# -*- coding: utf-8 -*-
import unittest

from Model.CCGameDBTWModel import *


class CCGameDBTWTest(unittest.TestCase):
    # 確認角色個數與欄位正確性
    def test_total_count(self):
        expected = 417
        actual = len(CCGameDBTWDataOwner().data)
        assert actual == expected, 'Total character count expect {0}, but actual {1}'.format(expected, actual)

    # 檢查我資料庫中的角色，是否與 CGDT 內的 ID 與 FullName 吻合
    def test_are_id_and_full_name_matched(self):
        data_owner = CCGameDBTWDataOwner()
        # 若 id>=6000，代表是國服的角色，不用檢查
        characters = DBAccessor.execute('select ID, FullName from Character where ID<6000').fetchall()
        for each_my_info in characters:
            the_id = each_my_info[0]
            name = each_my_info[1]

            cgdt_info = data_owner.find_character_by_id(the_id)
            assert cgdt_info is not None, 'Character ID={0} {1} did not match any id.'.format(
                the_id, name.encode('utf-8'))
            assert _compare_full_name(cgdt_info.full_name, name), 'Character ID={0} has FullName {1} and {2}.'.format(
                the_id, cgdt_info.full_name.encode('utf-8'), name.encode('utf-8'))


def _compare_full_name(cgdt_name, db_name):
    name = db_name.replace('v1', '')  # 主人公的 FullName 有重複
    return cgdt_name == name
