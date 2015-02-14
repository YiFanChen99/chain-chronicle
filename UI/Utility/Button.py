# -*- coding: utf-8 -*-
from Tkinter import *


class ToggleButton(Button):
    def __init__(self, master=None, selected=False, **kwargs):
        Button.__init__(self, master, **kwargs)
        self.default_selected_color = '#%02x%02x%02x' % (32, 32, 32)
        self.default_unselected_color = '#%02x%02x%02x' % (240, 240, 240)
        self.is_selected = False
        self.set_is_selected(selected)
        Button.bind(self, '<Button-1>', lambda event: self.toggling())

    def toggling(self):
        self.is_selected = not self.is_selected
        self._update_color()

    def set_is_selected(self, value):
        self.is_selected = bool(value)
        self._update_color()

    def _update_color(self):
        if self.is_selected:
            self["bg"] = self.default_selected_color
            self["fg"] = self.default_unselected_color
        else:
            self["bg"] = self.default_unselected_color
            self["fg"] = self.default_selected_color
