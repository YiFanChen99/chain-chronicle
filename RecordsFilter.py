# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

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