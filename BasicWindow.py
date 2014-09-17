# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import tkMessageBox


class BasicWindow(Frame):
    def __init__(self, width, height):
        Frame.__init__(self)
        self.window = Toplevel(width=width, height=height)

    def destroy(self):
        self.window.destroy()
        Frame.destroy(self)