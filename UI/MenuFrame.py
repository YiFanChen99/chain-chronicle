# -*- coding: utf-8 -*-
import os
from ModelUtility.CommonState import *
from ModelUtility.GroupController import *
from UI.Utility.BasicMainFrame import *
from UI.Index.IndexFrame import IndexFrame
from UI.Character.CharacterFrame import CharacterFrame
from UI.Record.RecordFrame import RecordFrame
from UI.Event.EventFrame import EventFrame
from UI.Friend.FriendFrame import FriendInfoFrame
from UI.DrawLots.DrawLotsFrame import DrawLotsFrame
from UI.MyCharacter.MyCharacterFrame import MyCharacterFrame


class BasicMenuFrame(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, bg='#%02x%02x%02x' % (200, 200, 200), **kwargs)
        self.pack(fill=BOTH, expand=1)


class MenuFrame(BasicMenuFrame):
    OTHER_INFO_PATH = 'data/OtherInfo.txt'

    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)
        self.radio_group = RadioGroupController(lambda: None)
        self._init_button_group()
        self._init_open_txt()

    def _init_button_group(self):
        buttons = [Button(self, text='Static Info', width=14, font=(SCP, 11),
                          command=lambda: self.master.change_sub_menu_frame(StaticGroupFrame(self.master))),
                   Button(self, text='Yama Account', width=14, font=(SCP, 11),
                          command=lambda: self.change_to_account_frame('Yama')),
                   Button(self, text='Happy Account', width=14, font=(SCP, 11),
                          command=lambda: self.change_to_account_frame('Happy')),
                   Button(self, text='Specials', width=14, font=(SCP, 11),
                          command=lambda: self.master.change_sub_menu_frame(SpecialsFrame(self.master)))]

        for index, button in enumerate(buttons):
            button.place(x=70 + 150 * index, y=-1)
            self.radio_group.group_button(button)

        # 預設選擇第一個
        self.radio_group.selecting_button(0)
        self.radio_group.buttons[0].invoke()

    def _init_open_txt(self):
        button = Button(self, text='其他資訊', width=6, font=(MS_JH, 10))
        button.place(x=MIN_WIDTH - 65, y=1)

        def opening_file():
            os.startfile(self.OTHER_INFO_PATH)
        button["command"] = opening_file

    def change_to_account_frame(self, name):
        set_account(name)
        self.master.change_sub_menu_frame(AccountGroupFrame(self.master))


class StaticGroupFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)
        self.radio_group = RadioGroupController(lambda: None)
        self._init_button_group()

    def _init_button_group(self):
        change_main_frame = lambda new_frame: self.master.change_main_frame(new_frame)
        buttons = [Button(self, text='Index', width=15, font=(SCP, 10),
                          command=lambda: change_main_frame(IndexFrame(self.master))),
                   Button(self, text='Record', width=15, font=(SCP, 10),
                          command=lambda: change_main_frame(RecordFrame(self.master))),
                   Button(self, text='Character', width=15, font=(SCP, 10),
                          command=lambda: change_main_frame(CharacterFrame(self.master))),
                   Button(self, text='Event', width=15, font=(SCP, 10),
                          command=lambda: change_main_frame(EventFrame(self.master)))]

        for index, button in enumerate(buttons):
            button.place(x=15 + 145 * index, y=1)
            self.radio_group.group_button(button)

        # 預設選擇第一個
        self.radio_group.selecting_button(0)
        self.radio_group.buttons[0].invoke()


class AccountGroupFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)
        self.radio_group = RadioGroupController(lambda: set_last_page_index(self.radio_group.current_selection))
        self._init_button_group()

    def _init_button_group(self):
        buttons = []
        change_main_frame = lambda new_frame: self.master.change_main_frame(new_frame)
        enabled_pages = get_enabled_pages()
        if enabled_pages[0]:
            buttons.append(Button(self, text='Friend', width=16, font=(SCP, 10),
                                  command=lambda: change_main_frame(FriendInfoFrame(self.master))))
        if enabled_pages[1]:
            buttons.append(Button(self, text='RecordOfDrawLots', width=16, font=(SCP, 10),
                                  command=lambda: change_main_frame(DrawLotsFrame(self.master))))
        if enabled_pages[2]:
            buttons.append(Button(self, text='MyCharacter', width=16, font=(SCP, 10),
                                  command=lambda: change_main_frame(MyCharacterFrame(self.master))))
        if enabled_pages[3]:
            buttons.append(Button(self, text='Resource', width=16, font=(SCP, 10),
                                  command=lambda: change_main_frame(
                                      MainFrame(self.master, width=100, height=100, background='red'))))

        for index, button in enumerate(buttons):
            button.place(x=15 + 152 * index, y=1)
            self.radio_group.group_button(button)

        # 預設選擇之前的分頁
        self.radio_group.selecting_button(get_last_page_index())
        self.radio_group.buttons[get_last_page_index()].invoke()


class SpecialsFrame(BasicMenuFrame):
    def __init__(self, master, width=MIN_WIDTH, height=31, **kwargs):
        BasicMenuFrame.__init__(self, master, width=width, height=height, **kwargs)
        self.radio_group = RadioGroupController(lambda: None)
        self._init_button_group()

    def _init_button_group(self):
        buttons = [Button(self, text='Fuji RecOfDraw', width=15, font=(SCP, 10),
                          command=lambda: self.show_fuji_record_of_draw_lots())]

        for index, button in enumerate(buttons):
            button.place(x=15 + 145 * index, y=1)
            self.radio_group.group_button(button)

        # 預設選擇第一個
        self.radio_group.selecting_button(0)
        self.radio_group.buttons[0].invoke()

    def show_fuji_record_of_draw_lots(self):
        set_account('Fuji')
        self.master.change_main_frame(DrawLotsFrame(self.master))