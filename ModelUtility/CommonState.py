# -*- coding: utf-8 -*-
from ModelUtility.DataRecorder import Recorder

_ACCOUNTS = ['Fuji', 'Yama']
_CORRESPONDING_SERVERS = ['JP', 'CN']
_account = _ACCOUNTS[0]
_server = _CORRESPONDING_SERVERS[0]
_account_page_index = 0
_recorder = Recorder()


def set_account(account):
    if not account in _ACCOUNTS:
        raise ValueError('Wrong account name!')

    global _account
    global _server
    _account = account
    _server = _CORRESPONDING_SERVERS[_ACCOUNTS.index(account)]


def get_account():
    global _account
    return _account


def get_server():
    global _server
    return _server


def get_account_page_index():
    global _account_page_index
    return _account_page_index


def set_account_page_index(index):
    global _account_page_index
    _account_page_index = index


def get_data_record(key):
    return _recorder.get(key)


def save_data_record():
    return _recorder.save()
