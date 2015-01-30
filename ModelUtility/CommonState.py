# -*- coding: utf-8 -*-
_db_suffix = 'JP'


def set_db_suffix(db_suffix):
    if not db_suffix in ['JP', 'CN']:
        raise ValueError('Wrong db suffix!')

    global _db_suffix
    _db_suffix = db_suffix


def get_db_suffix():
    global _db_suffix
    return _db_suffix
