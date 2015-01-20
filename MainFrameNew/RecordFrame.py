# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from configparser3 import configparser
import codecs
from BaseFrame import *
from UIUtility.Button import ToggleButton

RECORD_PATH = 'data\Record.txt'


class RecordFrame(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)
        self._init_advanced_daily_dropped_fields()
        self._init_advanced_daily_dropped_frame()

    def _init_advanced_daily_dropped_fields(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(RECORD_PATH, "utf8")
        self.total = self.config_parser.getint('Advanced Daily', 'Total')
        self.dropped = self.config_parser.getint('Advanced Daily', 'Dropped')

        self.total_desc = StringVar()
        self.dropped_desc = StringVar()
        self.dropped_ratio_desc = StringVar()
        self._update_advanced_daily_descs()

    def _init_advanced_daily_dropped_frame(self):
        Label(self, text='上級曜日', width=8, font=(MS_JH, 14)).place(x=42, y=5)
        self.third_button = ToggleButton(self, text='Third', width=7, font=(SCP, 11))
        self.third_button.place(x=17 + 79 * 0, y=38)
        self.fourth_button = ToggleButton(self, text='Fourth', width=7, font=(SCP, 11))
        self.fourth_button.place(x=17 + 79 * 1, y=38)

        submit_button = Button(self, text='Submit', width=16, font=(SCP, 11))
        submit_button.place(x=16, y=73)
        submit_button.bind('<Button-1>', self.submitting)

        current_y = 119
        Label(self, textvariable=self.total_desc, width=16, font=(SCP, 11)).place(x=15, y=current_y)
        Label(self, textvariable=self.dropped_desc, width=16, font=(SCP, 11)).place(x=15, y=current_y + 20)
        Label(self, textvariable=self.dropped_ratio_desc, width=16, font=(SCP, 11)).place(x=15, y=current_y + 40)

    def _update_advanced_daily_descs(self):
        self.total_desc.set(' Total  :  %4d ' % self.total)
        self.dropped_desc.set('Dropped :  %4d ' % self.dropped)
        self.dropped_ratio_desc.set(' Ratio  :  %.1f' % (self.dropped * 100.0 / self.total))

    # noinspection PyUnusedLocal
    def submitting(self, event):
        self.total += 1
        self.dropped += self.third_button.is_selected + self.fourth_button.is_selected
        self.config_parser.set('Advanced Daily', 'Total', str(self.total))
        self.config_parser.set('Advanced Daily', 'Dropped', str(self.dropped))
        with codecs.open(RECORD_PATH, encoding="utf8", mode='wb') as data_file:
            self.config_parser.write(data_file)

        self.third_button.set_is_selected(False)
        self.fourth_button.set_is_selected(False)
        self._update_advanced_daily_descs()
