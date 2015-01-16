# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from ttk import Combobox
from ModelUtility.CommonString import CONDITIONLESS


class FilterCombobox(Combobox):
    def __init__(self, master, **kwargs):
        Combobox.__init__(self, master, **kwargs)

    def set_contexts(self, contexts):
        result = ['']
        result.extend(contexts)
        self['values'] = result

    def get(self):
        selection = Combobox.get(self)
        return CONDITIONLESS if selection == '' else selection
