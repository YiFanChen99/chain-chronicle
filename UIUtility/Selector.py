# -*- coding: utf-8 -*-
from Tkinter import *
from PIL import ImageTk
from ModelUtility.GroupController import RadioGroupController
from ModelUtility.CommonString import *


class BaseSelector(Canvas):
    def __init__(self, master, callback, width, height, **kwargs):
        Canvas.__init__(self, master, width=width, height=height, **kwargs)
        self['bg'] = '#%02x%02x%02x' % (192, 192, 192)
        self.pack(fill=BOTH, expand=0)
        self.callback = callback
        self.width = width
        self.height = height


class ProfessionSelector(BaseSelector):
    OPTIONS = [CONDITIONLESS]
    OPTIONS.extend(PROFESSIONS[0:5])

    def __init__(self, master, callback, width=194, height=43, **kwargs):
        BaseSelector.__init__(self, master, callback, width=width, height=height, **kwargs)

        self.radio_group = RadioGroupController(self.notify, zero_selectionable=True)
        self.__init_images()
        self.__init_widgets()

    def __init_widgets(self):
        y_position = (self.height - 31) / 2
        distance = 37

        current_x = (self.width - 179) / 2
        button = Button(self, image=self.image_profession_warrior)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_profession_knight)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_profession_archer)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_profession_magician)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_profession_healer)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)

    # 必須宣告 self 由 instance 存起來，否則會無法顯示
    def __init_images(self):
        self.image_profession_warrior = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'profession_1_30x.png')
        self.image_profession_knight = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'profession_2_30x.png')
        self.image_profession_archer = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'profession_3_30x.png')
        self.image_profession_magician = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'profession_4_30x.png')
        self.image_profession_healer = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'profession_5_30x.png')

    @property
    def current_profession(self):
        return self.OPTIONS[self.radio_group.current_selection + 1]

    def notify(self):
        return self.callback(self.current_profession)

    # noinspection PyUnusedLocal
    def clean_current_selection(self, event=None):
        self.radio_group.clean_current_selection()

    def select(self, key):
        index = self.OPTIONS.index(key)
        self.radio_group.selecting_button(index - 1)


class RankSelector(BaseSelector):
    OPTIONS = [CONDITIONLESS, '5', '4', '3', BOTH_2_AND_1]

    def __init__(self, master, callback, width=194, height=43, **kwargs):
        BaseSelector.__init__(self, master, callback, width=width, height=height, **kwargs)

        self.radio_group = RadioGroupController(self.notify, zero_selectionable=True)
        self.__init_images()
        self.__init_widgets()

    def __init_widgets(self):
        y_position = (self.height - 33) / 2
        distance = 37

        current_x = (self.width - 182) / 2
        button = Button(self, image=self.image_rank_star)
        button.place(x=current_x, y=y_position)
        button.bind("<Button>", self.clean_current_selection)
        current_x += distance + 1
        button = Button(self, image=self.image_rank_5)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_rank_4)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_rank_3)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)
        current_x += distance
        button = Button(self, image=self.image_rank_other)
        button.place(x=current_x, y=y_position)
        self.radio_group.group_button(button)

    # 必須宣告 self 由 instance 存起來，否則會無法顯示
    def __init_images(self):
        self.image_rank_star = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'rank_star_32x.png')
        self.image_rank_5 = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'rank_5_32x.png')
        self.image_rank_4 = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'rank_4_32x.png')
        self.image_rank_3 = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'rank_3_32x.png')
        self.image_rank_other = ImageTk.PhotoImage(file=IMAGE_FOLDER + 'rank_other_32x.png')

    @property
    def current_rank(self):
        return self.OPTIONS[self.radio_group.current_selection + 1]

    def notify(self):
        return self.callback(self.current_rank)

    # noinspection PyUnusedLocal
    def clean_current_selection(self, event=None):
        self.radio_group.clean_current_selection()

    def select(self, key):
        if isinstance(key, int):
            key = BOTH_2_AND_1 if key < 3 else str(key)
        index = self.OPTIONS.index(key)
        self.radio_group.selecting_button(index - 1)
