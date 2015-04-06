# -*- coding: utf-8 -*-
from ModelUtility.DataRecorder import Recorder

_data_recorder = Recorder('data/data.json')
_account_recorder = Recorder('data/account.json')
_current_account = _account_recorder.get('Fuji')


# 寫入記憶體，不寫回檔案
def set_account(account_key):
    global _account_recorder
    global _current_account
    _current_account = _account_recorder.get(account_key)
    if not _current_account:
        raise ValueError('Wrong account key!')


def get_account_name():
    global _current_account
    return _current_account['name']


def get_server():
    global _current_account
    return _current_account['server']


def get_enabled_pages():
    global _current_account
    return _current_account['enabled_pages']


def get_last_page_index():
    global _current_account
    return _current_account['last_page']


# 寫入記憶體，不寫回檔案
def set_last_page_index(index):
    global _current_account
    _current_account['last_page'] = index


def get_data_record(key):
    global _data_recorder
    return _data_recorder.get(key)


def save_data_record():
    global _data_recorder
    return _data_recorder.save()
