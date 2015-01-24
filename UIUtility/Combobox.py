# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from ttk import Combobox
from ModelUtility.CommonString import CONDITIONLESS


class ComboboxWithEmptyOptions(Combobox):
    def __init__(self, master, **kwargs):
        Combobox.__init__(self, master, **kwargs)

    # 預設有一個為空的選項
    def __setitem__(self, key, value):
        if key == 'values':
            result = ['']
            result.extend(value)
            Combobox.__setitem__(self, key, result)


class FilteredCombobox(ComboboxWithEmptyOptions):
    def __init__(self, master, state='readonly', **kwargs):
        ComboboxWithEmptyOptions.__init__(self, master, state=state, **kwargs)

    def get(self):
        selection = ComboboxWithEmptyOptions.get(self)
        return CONDITIONLESS if selection == '' else selection
