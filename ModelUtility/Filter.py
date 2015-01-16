# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Comparator import *


class FilterManager():
    def __init__(self):
        self.__comparison_rules = {}
        self.__specific_conditions = {}

    def set_comparison_rule(self, index, rule=sub_match_request):
        self.__comparison_rules[index] = rule

    def clean_comparison_rules(self):
        self.__comparison_rules = {}

    def set_specific_condition(self, index, request, rule=match_request):
        self.__specific_conditions[index] = (request, rule)

    def clean_specific_condition(self):
        self.__specific_conditions = {}

    def filter(self, records, multi_request=''):
        return self.__filter_by_comparison_rules(self.__filter_by_specific_conditions(records), multi_request)

    def __filter_by_comparison_rules(self, records, multi_request):
        results = records

        requests = multi_request.split(' ')
        for request in requests:
            results = self.__filter_by_comparison_rules_with_single_request(results, request)

        return results

    # 若 request 沒內容代表全部允許，否則依照 request 進行部分比對
    def __filter_by_comparison_rules_with_single_request(self, records, request):
        if request == '':
            return records

        results = []
        for record in records:
            for index, rule in self.__comparison_rules.iteritems():
                if rule(record[index], request):
                    results.append(record)
                    break
        return results

    # 回傳 records 中符合所有 specific_conditions 的項目
    def __filter_by_specific_conditions(self, records):
        results = records
        for index, (request, rule) in self.__specific_conditions.iteritems():
            results = [element for element in results if rule(element[index], request)]
        return results
