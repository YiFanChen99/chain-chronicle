# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox


class BasicWindow(Toplevel):
    def __init__(self, master=None, **kwargs):
        Toplevel.__init__(self, master, **kwargs)
        self.transient(master)
        self.focus_set()