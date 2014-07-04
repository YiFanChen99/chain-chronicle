# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

GROUP_STATIC_INFO = 'Static Info'
GROUP_FUJI_ACCOUNT = 'Fuji Account'


class TabManager(object):
    def __init__(self):
        self.all_tabs = []
        self.groups = [GROUP_STATIC_INFO, GROUP_FUJI_ACCOUNT]

    def add_new_tab(self, group, name):
        # assertion
        self.__assert_legal_group(group)
        self.__assert_legal_tab_name(name)
        # add it
        new_tab = Tab(group, name)
        self.all_tabs.append(new_tab)

    def __assert_legal_group(self, group):
        if group not in self.groups:
            raise Exception("Wrong group name!")

    def __assert_legal_tab_name(self, name):
        for tab in self.all_tabs:
            if name == tab.name:
                raise Exception("Existed tab!")

    def get_groups(self):
        return self.groups

    def get_tabs(self, group=None):
        if group is None:
            return self.all_tabs
        else:
            result = []
            for tab in self.all_tabs:
                if tab.group == group:
                    result.append(tab)
            return result


class Tab(object):
    def __init__(self, group, name):
        self.group = group
        self.name = name
