# -*- coding: utf-8 -*-
_db_suffix = 'JP'


def set_db_suffix(db_suffix):
    global _db_suffix
    _db_suffix = db_suffix


def compose_db_table_name(table_name):
    global _db_suffix
    return table_name + _db_suffix
