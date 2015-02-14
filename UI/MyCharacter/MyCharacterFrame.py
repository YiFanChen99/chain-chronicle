# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from ModelUtility.DataObject import CharacterPower

# from Window.CharacterWindow import CharacterWindow TODO
# from ModelUtility.Filter import FilterRuleManager
# from Model import CharacterModel


class MyCharacterFrame(MainFrame):
    PAGES = ['CharacterPower']

    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)
        self.main_frame = None
        self._init_page_selector_frame()
        self.update_main_frame()

    # 用來放置換頁選單，必須置於上層
    def _init_page_selector_frame(self):
        self.page_selector_frame = Frame(self, width=144, height=33, bg='green')
        self.page_selector_frame.place(x=0, y=0)

        # 所屬篩選
        self.page_selector = ttk.Combobox(self.page_selector_frame, width=14, font=(MS_JH, 10), justify=CENTER)
        self.page_selector['values'] = self.PAGES
        self.page_selector.set(self.PAGES[0])
        self.page_selector.place(x=8, y=8)
        self.page_selector.bind('<<ComboboxSelected>>', lambda event: self.update_main_frame())

    def update_main_frame(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        if self.page_selector.get() == self.PAGES[0]:  # CharacterPower
            self.main_frame = CharacterPowerFrame(self, width=self['width'], height=self['height'], background='blue')
        else:
            raise Exception("Wrong page selected!")

        self.main_frame.place(x=0, y=0)
        self.page_selector_frame.tkraise()  # 放回上層，避免被遮到

    def adjust_size(self, width, height):
        MainFrame.adjust_size(self, width, height)
        if self.main_frame is not None:
            self.main_frame.adjust_size(width, height)


class CharacterPowerFrame(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(34, 38)
        self.table_model = TableModelAdvance()
        self.table_model.set_columns(CharacterPower.TABLE_VIEW_FULL_COLUMNS, main_column='Character')
        self.table_view.setModel(self.table_model)

        # TODO
        self.table_model.set_rows((['s9'] * len(CharacterPower.TABLE_VIEW_FULL_COLUMNS)))
        self.redisplay_table()
        self.table_view.hide_column('ID')