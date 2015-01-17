# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import unittest
from ModelUtility.CCGameDBTW import *


class CCGameDBTWTest(unittest.TestCase):
    # 確認角色個數與欄位正確性
    def test_total_count(self):
        expected = 413
        actual = len(CCGameDBTWDataOwner().data)
        assert actual == expected, 'Total character count expect {0}, but actual {1}'.format(expected, actual)

    # 檢查我資料庫中的角色，是否與 CGDT 內的 ID 與 FullName 吻合
    def test_are_id_and_full_name_matched(self):
        data_owner = CCGameDBTWDataOwner()
        characters = DBAccessor.execute('select ID, FullName from Character').fetchall()
        for each_my_info in characters:
            the_id = each_my_info[0]
            name = each_my_info[1]

            # 若 id>=6000，代表是國服的角色，不用檢查
            if the_id < 6000:
                cgdt_info = data_owner.find_character_by_id(the_id)
                assert cgdt_info is not None, 'Character ID={0} {1} did not match any id.'.format(
                    the_id, name.encode('utf-8'))
                assert cgdt_info.full_name == name, 'Character ID={0} has FullName {1} and {2}.'.format(
                    the_id, name.encode('utf-8'), cgdt_info.full_name.encode('utf-8'))
