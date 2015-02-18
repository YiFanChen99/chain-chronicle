# -*- coding: utf-8 -*-
from ttk import Combobox
from ModelUtility.CommonValue import CONDITIONLESS


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


class IntFilteredCombobox(FilteredCombobox):
    def __init__(self, master, **kwargs):
        FilteredCombobox.__init__(self, master, **kwargs)

    def get(self):
        selection = ComboboxWithEmptyOptions.get(self)
        return CONDITIONLESS if selection == '' else int(selection)


class ObjectCombobox(ComboboxWithEmptyOptions):
    def __init__(self, master, setter=lambda obj: str(obj), getter=lambda obj: obj, state='readonly', **kwargs):
        ComboboxWithEmptyOptions.__init__(self, master, state=state, **kwargs)
        self._objects = []
        self.selected_object = None
        self.setter = setter
        self.getter = getter

        self.bind('<<ComboboxSelected>>', lambda event: self.change_selected_object())

    def set_objects(self, objects):
        self._objects = objects
        self['values'] = [self.setter(obj) for obj in objects]

    def set(self, the_object):
        self.selected_object = the_object
        ComboboxWithEmptyOptions.set(self, '' if the_object is None else self.setter(the_object))

    def change_selected_object(self):
        for obj in self._objects:
            if self.setter(obj) == ComboboxWithEmptyOptions.get(self):
                self.selected_object = obj
                return
        # 至此無符合物件，設定為 None
        self.selected_object = None

    def get(self):
        return self.getter(self.selected_object) if self.selected_object is not None else None


class FilteredObjectCombobox(ObjectCombobox):
    def __init__(self, master, setter=lambda obj: str(obj), getter=lambda obj: obj, **kwargs):
        ObjectCombobox.__init__(self, master, setter=setter, getter=getter, **kwargs)

    def get(self):
        return CONDITIONLESS if self.selected_object is None else self.getter(self.selected_object)