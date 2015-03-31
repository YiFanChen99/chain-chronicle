# -*- coding: utf-8 -*-
from CommonValue import *
from Utility import is_any_japanese_character_contain


def match_request(source, request):
    if request == CONDITIONLESS:
        return True
    else:
        return source == request


def not_match_request(source, request):
    if request == CONDITIONLESS:
        return True
    else:
        return source != request


def match_requested_rank(source, request):
    if request == CONDITIONLESS:
        return True
    elif request == BOTH_2_AND_1:
        return source == 2 or source == 1
    else:
        return source == int(request)


def sub_match_request(source, request, is_case_sensitive=False):
    if is_case_sensitive:
        return request in source
    else:
        return request.lower() in source.lower()


def sub_match_request_or_japanese_character(source, request, is_case_sensitive=False):
    if request == '*j' or request == '*J':
        return is_any_japanese_character_contain(source)
    else:
        return sub_match_request(source, request, is_case_sensitive)
