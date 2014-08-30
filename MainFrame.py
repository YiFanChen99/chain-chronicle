# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *


class MainFrame(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.pack(fill=BOTH, expand=1)

    def adjust_size(self, width, height):
        self['width'] = width
        self['height'] = height
        self.adjust_widgets(width, height)

    # Template Method
    def adjust_widgets(self, width, height):
        pass