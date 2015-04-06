# -*- coding: utf-8 -*-
""" 此 module 放置通用卻無明顯分類的小功能 """
import json
from datetime import datetime


def save_json(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '), sort_keys=True)


def load_json(file_path):
    with open(file_path) as json_data:
        return json.loads(json_data.read().decode('utf-8-sig'))


def convert_str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None


def is_any_japanese_character_contain(variable):
    for character in variable:
        if u'\u3000' <= character <= u'\u30f0':
            return True
    return False


# 使點擊 label 與點擊 check box 有相同效果
# p.s. Checkbutton 本身就有 variable 可以用，還有 onvalue 等內建能力，
# 但缺點在無法調整文字與格子的相對位置，故需要調整要手動建立並 binding
def bind_check_box_and_label(check_box, label):
    # noinspection PyUnusedLocal
    def switching(*args):
        check_box.toggle()
    label.bind('<Button-1>', switching, add='+')
