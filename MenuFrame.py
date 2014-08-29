# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from NewStatic import *
import SubMenuFrame
import RadiobuttonController

GROUP_STATIC_INFO = 'Static Info'
GROUP_ACCOUNT_JP = 'Fuji Account'
GROUP_ACCOUNT_TW = 'Yama Account'
GROUPS = [GROUP_STATIC_INFO, GROUP_ACCOUNT_JP, GROUP_ACCOUNT_TW]


class MenuFrame(Frame):
    def __init__(self, master, height, **kwargs):
        Frame.__init__(self, master, width=MIN_WIDTH, height=height, **kwargs)
        self.pack(fill=BOTH, expand=1)

        radiobuttons = RadiobuttonController.RadiobuttonController(
            self, height=height, bg='#%02x%02x%02x' % (192, 192, 192))
        for group_index in range(len(GROUPS)):
            def do_select_group(obj=self, my_index=group_index):
                obj.do_select_group(my_index)

            radiobuttons.create_button(145 + 165 * group_index, -1, GROUPS[group_index],
                                       do_select_group, width=14)

            # 預設選擇第一個
            if group_index == 0:
                radiobuttons.do_select(0, do_select_group)

    # 幫 master 進行切換
    def do_select_group(self, index):
        self.master.update_sub_menu_frame(self.create_sub_menu_frame(index))

    def create_sub_menu_frame(self, index):
        if GROUPS[index] == GROUP_STATIC_INFO:
            return SubMenuFrame.StaticGroupFrame(self.master, height=31)
        elif GROUPS[index] == GROUP_ACCOUNT_JP:
            return SubMenuFrame.AccountGroupFrame(self.master, height=31, account_suffix='JP')
        elif GROUPS[index] == GROUP_ACCOUNT_TW:
            return SubMenuFrame.AccountGroupFrame(self.master, height=31, account_suffix='TW')
        else:
            raise Exception("Wrong group selected!")