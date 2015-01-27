# -*- coding: utf-8 -*-
from Comparator import *


class FilterRuleManager():
    def __init__(self):
        self._comparison_rules = {}
        self._specific_conditions = {}

    def set_comparison_rule(self, key, rule=sub_match_request):
        self._comparison_rules[key] = rule

    def clean_comparison_rules(self):
        self._comparison_rules = {}

    def set_specific_condition(self, key, request, rule=match_request):
        self._specific_conditions[key] = (request, rule)

    def clean_specific_condition(self):
        self._specific_conditions = {}

    def filter(self, records, multi_request=''):
        return self._filter_by_comparison_rules(self._filter_by_specific_conditions(records), multi_request)

    def _filter_by_comparison_rules(self, records, multi_request):
        results = records

        requests = multi_request.split(' ')
        for request in requests:
            results = self._filter_by_comparison_rules_with_single_request(results, request)

        return results

    # 若 request 沒內容代表全部允許，否則依照 request 進行部分比對
    def _filter_by_comparison_rules_with_single_request(self, records, request):
        if request == '':
            return records

        results = []
        for record in records:
            for key, rule in self._comparison_rules.iteritems():
                if rule(record[key], request):
                    results.append(record)
                    break
        return results

    # 回傳 records 中符合所有 specific_conditions 的項目
    def _filter_by_specific_conditions(self, records):
        results = records
        for key, (request, rule) in self._specific_conditions.iteritems():
            results = [element for element in results if rule(element[key], request)]
        return results
