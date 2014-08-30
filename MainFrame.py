# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *


class MainFrame(Frame):
    def __init__(self, master, db_suffix=None, **kwargs):
        self.db_suffix = db_suffix
        Frame.__init__(self, master, **kwargs)
        self.pack(fill=BOTH, expand=1)

    def adjust_size(self, width, height):
        self['width'] = width
        self['height'] = height
        self.adjust_widgets(width, height)

    # Template Method
    def adjust_widgets(self, width, height):
        pass

    def compose_table_name(self, table_name):
        return table_name + self.db_suffix