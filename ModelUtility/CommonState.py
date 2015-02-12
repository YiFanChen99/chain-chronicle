# -*- coding: utf-8 -*-
_ACCOUNTS = ['Fuji', 'Yama']
_CORRESPONDING_SERVERS = ['JP', 'CN']
_account = _ACCOUNTS[0]
_db_suffix = _CORRESPONDING_SERVERS[0]


def set_account(account):
    if not account in _ACCOUNTS:
        raise ValueError('Wrong account name!')

    global _account
    global _db_suffix
    _account = account
    _db_suffix = _CORRESPONDING_SERVERS[_ACCOUNTS.index(account)]


def get_account():
    global _account
    return _account


def get_db_suffix():
    global _db_suffix
    return _db_suffix
