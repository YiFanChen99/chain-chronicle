# -*- coding: utf-8 -*-
from CommonString import *


def match_request(source, request):
    if request == CONDITIONLESS:
        return True
    else:
        return source == request


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


# TODO 未用
# def is_any_japanese_character_contain(variable):
#     variable = variable.decode('utf8')
#     for character in variable:
#         if u'\u3000' <= character <= u'\u30f0':
#             return True
#     return False