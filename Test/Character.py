# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from ModelUtility.DBAccessor import *


def run_all_test():
    test_valid_id_and_full_name()


# 是否有未設定好的角色
def test_valid_id_and_full_name():
    characters = DBAccessor.execute('select ID, FullName from Character').fetchall()
    for character in characters:
        the_id = character[0]
        assert the_id is not None, 'ID is None, FullName=' + character[1]

        name = character[1]
        assert name is not None, 'FullName is None when ID={0}'.format(the_id)
