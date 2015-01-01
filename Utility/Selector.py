# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from PIL import ImageTk
from GroupController import RadioGroupController, FilterGroupController

IMAGE_FOLDER = '../images/'


class BaseSelector(Canvas):
    def __init__(self, master, callback, width, height, **kwargs):
        Canvas.__init__(self, master, width=width, height=height, **kwargs)
        self['bg'] = '#%02x%02x%02x' % (192, 192, 192)
        self.pack(fill=BOTH, expand=0)
        self.callback = callback
        self.width = width
        self.height = height


class ProfessionSelector(BaseSelector):
    PROFESSIONS = ['**', u'戰士', u'騎士', u'弓手', u'法師', u'僧侶']

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
        return self.PROFESSIONS[self.radio_group.current_selection + 1]

    def notify(self):
        return self.callback(self.current_profession)


class RankSelector(BaseSelector):
    RANKS = ['**', '5', '4', '3', '2and1']

    def __init__(self, master, callback, width=194, height=43, **kwargs):
        BaseSelector.__init__(self, master, callback, width=width, height=height, **kwargs)

        self.radio_group = RadioGroupController(self.notify, zero_selectionable=True)
        self.__init_images()
        self.__init_widgets()

    def __init_widgets(self):
        y_position = (self.height - 33) / 2
        distance = 37

        current_x = (self.width - 182) / 2
        Label(self, image=self.image_rank_star).place(x=current_x, y=y_position)
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
        return self.RANKS[self.radio_group.current_selection + 1]

    def notify(self):
        return self.callback(self.current_rank)