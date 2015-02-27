# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox


class BasicWindow(Toplevel):
    def __init__(self, master=None, position_y_shift=0, **kwargs):
        Toplevel.__init__(self, master, **kwargs)
        self.geometry('+%d+%d' % (self.get_root_x(), self.get_root_y(position_y_shift)))
        self.transient(master)
        self.focus_set()

    def get_root_x(self):
        return self.master.winfo_rootx() + 43 if self.master else 200

    def get_root_y(self, position_y_shift):
        return self.master.winfo_rooty() - 58 + position_y_shift if self.master else 200
