# -*- coding: utf-8 -*-
import unittest
from datetime import datetime
from ModelUtility.APTimeCalculator import *


class APTimeCalculatorTest(unittest.TestCase):
    def test_convert_ap_to_timedelta(self):
        time_diff = convert_ap_to_timedelta(189)
        assert time_diff.days == 1 and time_diff.seconds == 9*8*60,\
            'Converted timedelta is {0}'.format(time_diff)

    def test_convert_timedelta_to_ap(self):
        start_time = datetime(2015, 03, 02, 9, 00)
        end_time = datetime(2015, 03, 05, 8, 59)
        assert convert_timedelta_to_ap(end_time - start_time) == 539,\
            'Converted AP is {0}'.format(convert_timedelta_to_ap(end_time - start_time))