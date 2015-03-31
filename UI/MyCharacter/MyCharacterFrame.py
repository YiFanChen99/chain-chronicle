# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from UI.MyCharacter.CharacterPowerFrame import CharacterPowerFrame
from UI.MyCharacter.CharacterWeaponFrame import CharacterWeaponFrame


class MyCharacterFrame(MainFrame):
    PAGES = ['CharacterPower', 'CharacterWeapon']

    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)
        self.main_frame = None
        self._init_page_selector_frame()
        self.update_main_frame()

    # 用來放置換頁選單，必須置於上層
    def _init_page_selector_frame(self):
        self.page_selector_frame = Frame(self, width=154, height=30)
        self.page_selector_frame.place(x=0, y=0)

        # 換頁選單
        self.page_selector = ttk.Combobox(
            self.page_selector_frame, width=14, font=(MS_JH, 10), state='readonly', justify=CENTER)
        self.page_selector['values'] = self.PAGES
        self.page_selector.set(self.PAGES[0])
        self.page_selector.place(x=16, y=4)
        self.page_selector.bind('<<ComboboxSelected>>', lambda event: self.update_main_frame())

    def update_main_frame(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        if self.page_selector.get() == self.PAGES[0]:  # CharacterPower
            self.main_frame = CharacterPowerFrame(self, width=self['width'], height=self['height'])
        elif self.page_selector.get() == self.PAGES[1]:  # CharacterWeapon
            self.main_frame = CharacterWeaponFrame(self, width=self['width'], height=self['height'])
        else:
            raise Exception("Wrong page selected!")

        self.main_frame.place(x=0, y=0)
        self.main_frame.adjust_size(self['width'], self['height'])
        self.page_selector_frame.tkraise()  # 放回上層，避免被遮到

    def adjust_size(self, width, height):
        MainFrame.adjust_size(self, width, height)
        if self.main_frame is not None:
            self.main_frame.adjust_size(width, height)
