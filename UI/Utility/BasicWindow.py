# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox


class BasicWindow(Toplevel):
    def __init__(self, master=None, **kwargs):
        Toplevel.__init__(self, master, **kwargs)
        self.geometry('+%d+%d' % (self.get_root_x(), self.get_root_y()))
        self.transient(master)
        self.focus_set()

    def get_root_x(self):
        return self.master.winfo_rootx() + 43 if self.master else 200

    def get_root_y(self):
        return self.master.winfo_rooty() - 58 if self.master else 200
