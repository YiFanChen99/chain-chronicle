# -*- coding: utf-8 -*-
from datetime import timedelta


def convert_timedelta_to_ap(time_diff):
    return int(time_diff.total_seconds() / 60 / 8)


def convert_ap_to_timedelta(ap):
    return timedelta(minutes=ap * 8)