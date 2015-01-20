# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'


class BaseGroupController():
    def __init__(self, callback):
        # 設成 field 而非 static，使不同用途時可以調整
        self.default_selected_color = '#%02x%02x%02x' % (32, 32, 32)
        self.default_unselected_color = '#%02x%02x%02x' % (240, 240, 240)

        self.callback = callback
        self.buttons = []
        self.counter = 0

    def group_button(self, button):
        # noinspection PyUnusedLocal
        def selecting_button(event, obj=self, the_index=self.counter):
            obj.selecting_button(the_index)

        button.bind("<Button-1>", selecting_button, add='+')

        self.buttons.append(button)
        self.counter += 1

    # Template method
    def selecting_button(self, button):
        pass

    def change_button_state(self, index, selected):
        button = self.buttons[index]
        if selected:
            button["bg"] = self.default_selected_color
            button["fg"] = self.default_unselected_color
        else:
            button["bg"] = self.default_unselected_color
            button["fg"] = self.default_selected_color


class RadioGroupController(BaseGroupController):
    DEFAULT_SELECTION = -1

    def __init__(self, callback, zero_selectionable=False):
        BaseGroupController.__init__(self, callback)
        self.is_zero_selectionable = zero_selectionable
        self.current_selection = self.DEFAULT_SELECTION

    def selecting_button(self, index):
        if index == self.current_selection:
            if self.is_zero_selectionable:
                self.change_button_state(index, False)
                self.current_selection = self.DEFAULT_SELECTION
                self.callback()
        else:
            for i in range(self.counter):
                self.change_button_state(i, i == index)
            self.current_selection = index
            self.callback()

    def clean_current_selection(self):
        if self.is_zero_selectionable:
            if self.current_selection != self.DEFAULT_SELECTION:
                self.change_button_state(self.current_selection, False)
                self.current_selection = self.DEFAULT_SELECTION
                self.callback()
        else:
            raise Exception("Is not zero-selectionable!")


class FilterGroupController(BaseGroupController):
    def __init__(self, callback):
        BaseGroupController.__init__(self, callback)
        self.current_selections = []

    def selecting_button(self, index):
        if index in self.current_selections:
            self.current_selections.remove(index)
            self.change_button_state(index, False)
        else:
            self.current_selections.append(index)
            self.change_button_state(index, True)
        self.callback()

    def clean_current_selections(self):
        for index in self.current_selections:
            self.change_button_state(index, False)
            self.current_selections.remove(index)