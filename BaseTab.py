# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
import sqlite3


class BaseTab(Frame):
    def __init__(self, parent=None):
        self.database = sqlite3.connect('ChainChronicle.sqlite')
        self.cursor = self.database.cursor()

        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

    def commit(self):
        self.database.commit()

    def execute(self, sql_commend):
        return self.cursor.execute(sql_commend)

    @staticmethod
    def convert_to_str(value):
        if value is None:
            return ''
        else:
            return value.encode('utf-8')

    @staticmethod
    def destroy_frame(obj):
        if obj is not None:
            obj.destroy()