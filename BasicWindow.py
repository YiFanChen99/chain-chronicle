# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import tkMessageBox


class BasicWindow(Frame):
    def __init__(self, **kwargs):
        Frame.__init__(self, **kwargs)
        self.window = None

    def destroy(self):
        self.window.destroy()
        Frame.destroy(self)