# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from NewStatic import *


class RadiobuttonController(Frame):
    def __init__(self, master, height, **kwargs):
        Frame.__init__(self, master, width=MIN_WIDTH, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)
        self.default_selected_color = '#%02x%02x%02x' % (32, 32, 32)
        self.default_unselected_color = '#%02x%02x%02x' % (240, 240, 240)
        self.default_font = ('Microsoft JhengHei', 11)
        self.default_width = 14

        self.current_selected = -1
        self.buttons = []

    def create_button(self, pos_x, pos_y, text, callback=None, width=None, **kwargs):
        if width is None:
            width = self.default_width

        next_index = len(self.buttons)

        def do_select(obj=self, the_index=next_index, the_callback=callback):
            obj.do_select(the_index, the_callback)

        button = Button(self, text=text, width=width, font=self.default_font, **kwargs)
        button.place(x=pos_x, y=pos_y)
        button["command"] = do_select

        self.buttons.append(button)

    # 當選擇非選取中的按鈕才會觸發更換事件
    def do_select(self, index, callback):
        if index != self.current_selected:
            self.change_buttons_state(index)
            if callback is not None:
                callback()

    def change_buttons_state(self, index):
        self.current_selected = index
        selecting_button = self.buttons[index]
        for button in self.buttons:
            if button == selecting_button:
                button["bg"] = self.default_selected_color
                button["fg"] = self.default_unselected_color
            else:
                button["bg"] = self.default_unselected_color
                button["fg"] = self.default_selected_color