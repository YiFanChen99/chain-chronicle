# -*- coding: utf-8 -*-
from Tkinter import *


class IntEntry(Entry):
    def __init__(self, master=None, value='', justify=CENTER, **kwargs):
        self.value = StringVar(value)
        Entry.__init__(self, master, textvariable=self.value, justify=justify, **kwargs)

    def get(self):
        return int(self.value.get()) if self.value.get() else 0

    def set(self, value):
        self.value.set(value if value else '')
