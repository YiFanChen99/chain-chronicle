# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from ModelUtility.CommonString import *


def match_requested(source, requested):
    if requested == CONDITIONLESS:
        return True
    else:
        return source == requested


def match_requested_rank(source, requested):
    if requested == CONDITIONLESS:
        return True
    elif requested == BOTH_2_AND_1:
        return source == 2 or source == 1
    else:
        return source == int(requested)