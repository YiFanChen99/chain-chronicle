# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *
import ttk
from configparser3 import configparser
from datetime import timedelta
import codecs

FONT = (MS_JH, 12)
FILE_NAME = 'data/AP.txt'


class PowerConverter(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        self.parser = configparser.RawConfigParser()
        self.parser.read(FILE_NAME, "utf8")

        Converter(self, 'Fuji Account', self.parser, width=300, height=MIN_HEIGHT).place(x=10, y=0)
        Converter(self, 'Yama Account', self.parser, width=300, height=MIN_HEIGHT).place(x=325, y=0)


MAX_AP = 'Max AP'
LAST_CALCULATION = 'Last Calculation'
DIFFERENCE = 'Difference'
REACHED_TIME = 'Reached Time'


class Converter(Frame):
    def __init__(self, master, name, parser, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.name = name
        self.parser = parser

        self.__init_widgets()

        # Loading data
        self.last_calculation.set(parser.get(name, LAST_CALCULATION))
        self.max_ap.set(parser.getint(name, MAX_AP))
        self.difference_for_max.set(parser.get(name, DIFFERENCE))
        self.time_reaching_max_ap.set(parser.get(name, REACHED_TIME))

    def __init_widgets(self):
        left_x = 30
        middle_x = left_x + 106
        right_x = middle_x + 90

        current_y = 7
        Label(self, width=12, text=self.name, font=FONT).place(x=92, y=current_y)

        current_y += 33
        ttk.Separator(self, orient=HORIZONTAL).place(x=10, y=current_y, width=300)

        current_y += 10
        self.last_calculation = StringVar(value='')
        Label(self, width=20, textvariable=self.last_calculation, font=FONT).place(x=52, y=current_y)

        current_y += 36
        self.calculate_for_max = Button(self, width=4, height=4, text='轉 換', font=FONT, relief=RIDGE, wraplength=1)
        self.calculate_for_max.place(x=right_x, y=current_y - 1)
        self.calculate_for_max['command'] = self.calculating_for_max_ap

        Label(self, width=8, text='Current AP', font=FONT).place(x=left_x, y=current_y)
        self.current_ap = StringVar(value='')
        current_ap_entry = Entry(self, width=6, textvariable=self.current_ap, font=FONT)
        current_ap_entry.place(x=middle_x, y=current_y)
        current_ap_entry.bind('<Return>', self.calculating_for_max_ap)

        current_y += 36
        Label(self, width=8, text='Max AP', font=FONT).place(x=left_x, y=current_y)
        self.max_ap = StringVar(value='')
        Entry(self, width=6, textvariable=self.max_ap, font=FONT).place(x=middle_x, y=current_y)

        current_y += 36
        Label(self, width=8, text='Adjustment', font=FONT).place(x=left_x, y=current_y)
        self.adjustment = StringVar(value='')
        Entry(self, width=6, textvariable=self.adjustment, font=FONT).place(x=middle_x, y=current_y)

        current_y += 36
        self.difference_for_max = StringVar(value='')
        Label(self, width=20, textvariable=self.difference_for_max, font=FONT).place(x=52, y=current_y)

        current_y += 30
        self.time_reaching_max_ap = StringVar(value='')
        Label(self, width=20, textvariable=self.time_reaching_max_ap, font=FONT).place(x=52, y=current_y)

        current_y += 36
        ttk.Separator(self, orient=HORIZONTAL).place(x=10, y=current_y, width=300)

        current_y += 24
        self.calculate_for_goal = Button(self, width=4, text='轉 換', font=FONT, relief=RIDGE)
        self.calculate_for_goal.place(x=right_x, y=current_y - 6)
        self.calculate_for_goal['command'] = self.calculating_for_goal_ap

        Label(self, width=8, text='Goad AP', font=FONT).place(x=left_x, y=current_y)
        self.goal = StringVar(value='')
        goal_entry = Entry(self, width=6, textvariable=self.goal, font=FONT)
        goal_entry.place(x=middle_x, y=current_y)
        goal_entry.bind('<Return>', self.calculating_for_goal_ap)

        current_y += 37
        self.difference_for_goal = StringVar(value='')
        Label(self, width=20, textvariable=self.difference_for_goal, font=FONT).place(x=52, y=current_y)

        current_y += 30
        self.time_reaching_goal_ap = StringVar(value='')
        Label(self, width=20, textvariable=self.time_reaching_goal_ap, font=FONT).place(x=52, y=current_y)

    # noinspection PyUnusedLocal
    def calculating_for_max_ap(self, event=None):
        # 初始化
        if self.current_ap.get() == '':
            self.current_ap.set(0)
        if self.adjustment.get() == '':
            self.adjustment.set(0)

        # 計算並改動
        difference_ap = int(self.max_ap.get()) - int(self.current_ap.get()) - int(self.adjustment.get())
        difference_time = timedelta(minutes=difference_ap * 8)
        self.last_calculation.set(LAST_CALCULATION + ' :   ' + self.convert_time_to_str(datetime.now()))
        self.difference_for_max.set('%02d AP --> ' % difference_ap +
                                    self.convert_timedelta_to_str(difference_time))
        self.time_reaching_max_ap.set(REACHED_TIME + ' :   ' +
                                      self.convert_time_to_str(datetime.now() + difference_time))

        # 將最新結果存回檔案中
        self.parser.set(self.name, LAST_CALCULATION, self.last_calculation.get())
        self.parser.set(self.name, MAX_AP, self.max_ap.get())
        self.parser.set(self.name, DIFFERENCE, self.difference_for_max.get())
        self.parser.set(self.name, REACHED_TIME, self.time_reaching_max_ap.get())
        with codecs.open(FILE_NAME, encoding="utf8", mode='wb') as data_file:
            self.parser.write(data_file)

    # noinspection PyUnusedLocal
    def calculating_for_goal_ap(self, event=None):
        # 初始化
        if self.current_ap.get() == '':
            self.current_ap.set(0)
        if self.goal.get() == '':
            self.goal.set(0)

        # 計算並改動
        difference_ap = int(self.goal.get()) - int(self.current_ap.get())
        difference_time = timedelta(minutes=difference_ap * 8)
        self.difference_for_goal.set('%02d AP --> ' % difference_ap +
                                     self.convert_timedelta_to_str(difference_time))
        self.time_reaching_goal_ap.set(REACHED_TIME + ' :   ' +
                                       self.convert_time_to_str(datetime.now() + difference_time))

    @staticmethod
    def convert_time_to_str(time):
        return '%02d : %02d' % (time.hour % 12, time.minute)

    @staticmethod
    def convert_timedelta_to_str(the_timedelta):
        total_minutes = the_timedelta.seconds / 60
        minute = total_minutes % 60
        hour = total_minutes / 60
        return '%02d 小時 %02d 分' % (hour, minute)