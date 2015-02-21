# -*- coding: utf-8 -*-
import codecs
from configparser3 import configparser
from UI.Utility.BasicMainFrame import *
from UI.Utility.Button import ToggleButton
from ModelUtility.StatisticTacker import DroppedStatisticTacker


class RecordFrame(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        self.jp_advanced_daily_dropped = JPAdvancedDailyDroppedCanvas(self)
        self.jp_advanced_daily_dropped.place(x=15, y=12)

        self.cn_jiyo_monthly_dropped = CNJiYoMonthlyDroppedCanvas(self)
        self.cn_jiyo_monthly_dropped.place(x=200, y=12)


class JPAdvancedDailyDroppedCanvas(Canvas):
    RECORD_PATH = 'data\Record.txt'
    SECTION = 'JP Advanced Daily'

    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self._init_frame()
        self._init_fields()

    def _init_frame(self):
        Label(self, text='上級曜日', width=8, font=(MS_JH, 14)).place(x=43, y=5)
        self.third_button = ToggleButton(self, text='Third', width=7, font=(SCP, 11), relief=RIDGE)
        self.third_button.place(x=18 + 78 * 0, y=39)
        self.fourth_button = ToggleButton(self, text='Fourth', width=7, font=(SCP, 11), relief=RIDGE)
        self.fourth_button.place(x=18 + 78 * 1, y=39)

        submit_button = Button(self, text='Submit', width=15, font=(SCP, 11), relief=RIDGE)
        submit_button.place(x=20, y=76)
        submit_button.bind('<Button-1>', lambda event: self.submitting())

        current_y = 114
        self.total_desc = StringVar()
        self.dropped_desc = StringVar()
        self.dropped_ratio_desc = StringVar()
        Label(self, textvariable=self.total_desc, width=16, font=(SCP, 11)).place(x=16, y=current_y)
        Label(self, textvariable=self.dropped_desc, width=16, font=(SCP, 11)).place(x=16, y=current_y + 20)
        Label(self, textvariable=self.dropped_ratio_desc, width=16, font=(SCP, 11)).place(x=16, y=current_y + 40)

    def _init_fields(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(self.RECORD_PATH, "utf8")

        self.statistic_tacker = DroppedStatisticTacker(1)
        self.statistic_tacker.set(
            self.config_parser.getint(self.SECTION, 'Total'), [self.config_parser.getint(self.SECTION, 'Dropped')])

        self._update_statistics()

    def _update_statistics(self):
        self.total_desc.set(' Total  :  %4d ' % self.statistic_tacker.times)
        self.dropped_desc.set('Dropped :  %4d ' % self.statistic_tacker.drops[0])
        self.dropped_ratio_desc.set(' Ratio  :  %.2f' % (self.statistic_tacker.get_statistics_count()[0]))

    def submitting(self):
        self.statistic_tacker.record([self.third_button.is_selected + self.fourth_button.is_selected])
        self.config_parser.set(self.SECTION, 'Total', str(self.statistic_tacker.times))
        self.config_parser.set(self.SECTION, 'Dropped', str(self.statistic_tacker.drops[0]))
        with codecs.open(self.RECORD_PATH, encoding="utf8", mode='wb') as data_file:
            self.config_parser.write(data_file)

        self.third_button.set_is_selected(False)
        self.fourth_button.set_is_selected(False)
        self._update_statistics()


class CNJiYoMonthlyDroppedCanvas(Canvas):
    RECORD_PATH = 'data\Record.txt'
    SECTION = 'CN JiYo Monthly'

    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self._init_frame()
        self._init_fields()

    def _init_frame(self):
        Label(self, text='自由月間', width=8, font=(MS_JH, 14)).place(x=43, y=5)
        self.box_12_button = ToggleButton(self, text='1&2', width=4, font=(SCP, 11), relief=RIDGE)
        self.box_12_button.place(x=18 + 51 * 0, y=39)
        self.box_3_button = ToggleButton(self, text='3', width=4, font=(SCP, 11), relief=RIDGE)
        self.box_3_button.place(x=18 + 51 * 1, y=39)
        self.box_4_button = ToggleButton(self, text='4', width=4, font=(SCP, 11), relief=RIDGE)
        self.box_4_button.place(x=18 + 51 * 2, y=39)

        submit_button = Button(self, text='Submit', width=15, font=(SCP, 11), relief=RIDGE)
        submit_button.place(x=20, y=76)
        submit_button.bind('<Button-1>', lambda event: self.submitting())

        label_x = 12
        var_x = label_x + 98
        current_y = 114
        Label(self, text='  Times   :', width=12, font=(SCP, 10)).place(x=label_x, y=current_y)
        Label(self, text='Fertilizer:', width=12, font=(SCP, 10)).place(x=label_x, y=current_y + 20)
        self.times_var = StringVar()
        self.fertilizer_var = StringVar()
        Label(self, textvariable=self.times_var, width=6, font=(SCP, 11)).place(x=var_x, y=current_y)
        Label(self, textvariable=self.fertilizer_var, width=6, font=(SCP, 11)).place(x=var_x, y=current_y + 20)

        current_y += 45
        Label(self, text=' Avg.Fer. :', width=12, font=(SCP, 10)).place(x=label_x, y=current_y)
        Label(self, text='Character :', width=12, font=(SCP, 10)).place(x=label_x, y=current_y + 20)
        self.avg_fertilizer_var = StringVar()
        self.character_var = StringVar()
        Label(self, textvariable=self.avg_fertilizer_var, width=6, font=(SCP, 11)).place(x=var_x, y=current_y)
        Label(self, textvariable=self.character_var, width=6, font=(SCP, 11)).place(x=var_x, y=current_y + 20)

        self._init_buttons_state()

    def _init_fields(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(self.RECORD_PATH, "utf8")

        self.statistic_tacker = DroppedStatisticTacker(2)
        self.statistic_tacker.set(self.config_parser.getint(self.SECTION, 'total'),
                                  [self.config_parser.getint(self.SECTION, 'fertilizer'),
                                   self.config_parser.getint(self.SECTION, 'character')])

        self._update_statistics()

    def _update_statistics(self):
        self.times_var.set(self.statistic_tacker.times)
        self.fertilizer_var.set(self.statistic_tacker.drops[0])
        avg_count = self.statistic_tacker.get_statistics_count()
        self.avg_fertilizer_var.set('%.2f' % (avg_count[0]))
        self.character_var.set(' %.1f %%' % ((avg_count[1]) * 100))

    def _init_buttons_state(self):
        self.box_12_button.set_is_selected(True)
        self.box_3_button.set_is_selected(False)
        self.box_4_button.set_is_selected(False)

    def submitting(self):
        self.statistic_tacker.record([int(self.box_12_button.is_selected) * 2 + self.box_3_button.is_selected,
                                      self.box_4_button.is_selected])
        self.config_parser.set(self.SECTION, 'total', str(self.statistic_tacker.times))
        self.config_parser.set(self.SECTION, 'fertilizer', str(self.statistic_tacker.drops[0]))
        self.config_parser.set(self.SECTION, 'character', str(self.statistic_tacker.drops[1]))
        with codecs.open(self.RECORD_PATH, encoding="utf8", mode='wb') as data_file:
            self.config_parser.write(data_file)

        self._init_buttons_state()
        self._update_statistics()
