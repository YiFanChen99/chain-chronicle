# -*- coding: utf-8 -*-
from Comparator import *
from ModelUtility.Filter import FilterRuleManager


class DataHolder(object):
    def __init__(self, data_getter):
        self.data = []
        self.data_getter = data_getter
        self.filter_manager = FilterRuleManager()

    def update_data(self):
        self.data = self.data_getter()

    def set_comparison_rule(self, key, rule=sub_match_request):
        self.filter_manager.set_comparison_rule(key, rule)

    def clean_comparison_rules(self):
        self.filter_manager.clean_comparison_rules()

    def set_specific_condition(self, key, request, rule=match_request):
        self.filter_manager.set_specific_condition(key, request, rule)

    def clean_specific_condition(self):
        self.filter_manager.clean_specific_condition()

    def set_sub_object_filter(self, key, filter):
        self.filter_manager.set_sub_object_filter(key, filter)

    def clean_sub_object_filter(self):
        self.filter_manager.clean_sub_object_filter()