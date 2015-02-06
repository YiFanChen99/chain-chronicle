# -*- coding: utf-8 -*-


class DroppedStatisticTacker(object):
    def __init__(self, length):
        self.times = 0
        self.drops = [0] * length

    def set(self, times, drops):
        self.verify_record_length(drops)

        self.times = times
        self.drops = drops[:]

    def record(self, the_record):
        self.verify_record_length(the_record)

        self.times += 1
        self.drops = [a + b for a, b in zip(self.drops, the_record)]

    # 回傳的每次的平均個數
    def get_statistics_count(self):
        statistics = []
        for drop in self.drops:
            statistics.append((float(drop) / self.times) if self.times > 0 else 0.0)
        return statistics

    # 回傳的每次的平均比例
    def get_statistics_ratio(self):
        return [element * 100 for element in self.get_statistics_count()]

    def verify_record_length(self, the_record):
        if len(the_record) != len(self.drops):
            raise Exception('Drops length {0}, and the record length {1}.'.format(len(self.drops), len(the_record)))