# -*- coding: utf-8 -*-
""" 此 module 放置通用卻無明顯分類的小功能 """


# 使點擊 label 與點擊 check box 有相同效果
# p.s. Checkbutton 本身就有 variable 可以用，還有 onvalue 等內建能力，
# 但缺點在無法調整文字與格子的相對位置，故需要調整要手動建立並 binding
def bind_check_box_and_label(check_box, label):
    # noinspection PyUnusedLocal
    def switching(*args):
        check_box.toggle()
    label.bind('<Button-1>', switching, add='+')
