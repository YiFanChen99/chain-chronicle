# -*- coding: utf-8 -*-
from ModelUtility.Utility import save_json, load_json

_DATA_PATH = 'data/data.json'


class Recorder(object):
    def __init__(self, path=_DATA_PATH):
        self.path = path
        self.data = load_json(self.path)

    def get(self, key):
        return self.data.setdefault(key, {})

    def save(self):
        save_json(self.path, self.data)

    def __str__(self):
        return str(self.data)