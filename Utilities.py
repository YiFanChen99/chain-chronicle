# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *


class RecordsFilter():
    def __init__(self, commend):
        self.__selecting_command = commend
        self.__filters = {}
        self.update_raw_records()

    # noinspection PyAttributeOutsideInit
    def update_raw_records(self):
        self.raw_records = DATABASE.execute(self.__selecting_command).fetchall()
        self.__filtering()

    def add_filter(self, index, condition):
        self.__filters[index] = condition
        self.__filtering()

    def clear_filters(self):
        self.__filters.clear()
        self.__filtering()

    def __filtering(self):
        results = self.raw_records
        for index, condition in self.__filters.iteritems():
            results = [element for element in results if element[index] == condition]
        self.filtered_records = results


class RadiobuttonController(Frame):
    def __init__(self, master, width, height, button_type=1, **kwargs):
        Frame.__init__(self, master, width=width, height=height, **kwargs)
        self['bg'] = FRAME_BG_COLOR
        self.default_selected_color = '#%02x%02x%02x' % (32, 32, 32)
        self.default_unselected_color = '#%02x%02x%02x' % (240, 240, 240)
        self.set_button_type(button_type)

        self.current_selected = -1
        self.buttons = []

    # noinspection PyAttributeOutsideInit
    def set_button_type(self, button_type):
        if button_type == 2:
            self.default_font = (MS_JH, 10)
            self.default_width = 12
        elif button_type == 3:
            self.default_font = (MS_JH, 9)
            self.default_width = 10
        else:  # 當 type 為 None/1
            self.default_font = (MS_JH, 11)
            self.default_width = 14

    def create_button(self, pos_x, pos_y, text, callback=None, width=None, **kwargs):
        if width is None:
            width = self.default_width

        next_index = len(self.buttons)

        def selecting_button(obj=self, the_index=next_index, the_callback=callback):
            obj.selecting_button(the_index, the_callback)

        button = Button(self, text=text, width=width, font=self.default_font, **kwargs)
        button.place(x=pos_x, y=pos_y)
        button["command"] = selecting_button

        self.buttons.append(button)

    # 當選擇非選取中的按鈕才會觸發更換事件
    def selecting_button(self, index, callback):
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


class ToggleButton(Button):
    def __init__(self, master=None, selected=False, callback=None, **kwargs):
        Button.__init__(self, master, **kwargs)
        self.default_selected_color = '#%02x%02x%02x' % (32, 32, 32)
        self.default_unselected_color = '#%02x%02x%02x' % (240, 240, 240)
        self.is_selected = bool(selected)
        self.__update_color()
        self.callback = callback
        self['command'] = self.toggling

    def toggling(self):
        self.is_selected = not self.is_selected
        self.__update_color()
        if self.callback is not None:
            self.callback()

    def __update_color(self):
        if self.is_selected:
            self["bg"] = self.default_selected_color
            self["fg"] = self.default_unselected_color
        else:
            self["bg"] = self.default_unselected_color
            self["fg"] = self.default_selected_color

    def set_is_selected(self, value):
        self.is_selected = bool(value)
        self.__update_color()