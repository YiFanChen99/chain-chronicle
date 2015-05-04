# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from UI.Utility.Button import ToggleButton
from ModelUtility.StatisticTacker import DroppedStatisticTacker
from ModelUtility.CommonState import *


class RecordFrame(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        self.jp_advanced_daily_dropped = JPAdvancedDailyDroppedCanvas(self)
        self.jp_advanced_daily_dropped.place(x=15, y=12)

        self.monthly_dropped = MonthlyDroppedCanvas(self, 'CN Monthly 1')
        self.monthly_dropped.place(x=200, y=12)
        self.monthly_dropped_2 = MonthlyDroppedCanvas(self, 'CN Monthly 2')
        self.monthly_dropped_2.place(x=390, y=12)

        self.the_stage_dropped = SpecificStageDroppedCanvas(self, 'Specific Stage 1', width=163)
        self.the_stage_dropped.place(x=582, y=12)


class JPAdvancedDailyDroppedCanvas(Canvas):
    SECTION = 'JP Advanced Daily'
    KEY_TOTAL = 'total'
    KEY_DROPPED = 'dropped'

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
        data_record = get_data_record(self.SECTION)
        self.statistic_tacker = DroppedStatisticTacker(1)
        self.statistic_tacker.set(data_record[self.KEY_TOTAL], [data_record[self.KEY_DROPPED]])

        self._update_statistics()

    def _update_statistics(self):
        self.total_desc.set(' Total  :  %4d ' % self.statistic_tacker.times)
        self.dropped_desc.set('Dropped :  %4d ' % self.statistic_tacker.drops[0])
        self.dropped_ratio_desc.set(' Ratio  :  %.2f' % (self.statistic_tacker.get_statistics_count()[0]))

    def submitting(self):
        self.statistic_tacker.record([self.third_button.is_selected + self.fourth_button.is_selected])

        data_record = get_data_record(self.SECTION)
        data_record[self.KEY_TOTAL] = self.statistic_tacker.times
        data_record[self.KEY_DROPPED] = self.statistic_tacker.drops[0]
        save_data_record()

        self.third_button.set_is_selected(False)
        self.fourth_button.set_is_selected(False)
        self._update_statistics()


class MonthlyDroppedCanvas(Canvas):
    KEY_TOTAL = 'total'
    KEY_FERTILIZER = 'fertilizer'
    KEY_CHARACTER = 'character'

    def __init__(self, master, section, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.title = StringVar()
        self.section = section
        self._init_frame()
        self._init_fields()

    def _init_frame(self):
        Label(self, textvariable=self.title, width=8, font=(MS_JH, 14)).place(x=43, y=5)
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
        data_record = get_data_record(self.section)
        self.title.set(data_record['title'])
        self.statistic_tacker = DroppedStatisticTacker(2)
        self.statistic_tacker.set(data_record[self.KEY_TOTAL],
                                  [data_record[self.KEY_FERTILIZER], data_record[self.KEY_CHARACTER]])

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

        data_record = get_data_record(self.section)
        data_record[self.KEY_TOTAL] = self.statistic_tacker.times
        data_record[self.KEY_FERTILIZER] = self.statistic_tacker.drops[0]
        data_record[self.KEY_CHARACTER] = self.statistic_tacker.drops[1]
        save_data_record()

        self._init_buttons_state()
        self._update_statistics()


class SpecificStageDroppedCanvas(Canvas):
    KEY_TOTAL = 'total'
    KEY_DROPS = "drops"
    KEY_VALUES = "values"

    def __init__(self, master, section, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.title = StringVar()
        self.section = section
        self._init_frame()
        self._init_fields()

    def _init_frame(self):
        Label(self, textvariable=self.title, width=13, font=(MS_JH, 14)).place(x=7, y=5)
        self.box_1_button = ToggleButton(self, text='1st', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_1_button.place(x=5 + 40 * 0, y=39)
        self.box_2_button = ToggleButton(self, text='2nd', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_2_button.place(x=5 + 40 * 1, y=39)
        self.box_3_button = ToggleButton(self, text='3rd', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_3_button.place(x=5 + 40 * 2, y=39)
        self.box_4_button = ToggleButton(self, text='4th', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_4_button.place(x=5 + 40 * 3, y=39)

        submit_button = Button(self, text='Submit', width=16, font=(SCP, 11), relief=RIDGE)
        submit_button.place(x=6, y=76)
        submit_button.bind('<Button-1>', lambda event: self.submitting())

        current_y = 114
        self.total_desc = StringVar()
        Label(self, textvariable=self.total_desc, width=16, font=(SCP, 11)).place(x=8, y=current_y)
        current_y += 28
        self.drop_vars = [IntVar(), IntVar(), IntVar(), IntVar()]
        for i in range(4):
            Label(self, textvariable=self.drop_vars[i], width=3, font=(SCP, 11), relief=GROOVE).\
                place(x=7 + 40 * i, y=current_y)
        self._init_buttons_state()
        current_y += 25
        self.values_desc = StringVar()
        Label(self, textvariable=self.values_desc, width=16, font=(SCP, 11)).place(x=8, y=current_y)

    def _init_fields(self):
        data_record = get_data_record(self.section)
        self.title.set(data_record['title'])
        self.statistic_tacker = DroppedStatisticTacker(4)
        self.statistic_tacker.set(data_record[self.KEY_TOTAL], data_record[self.KEY_DROPS])
        self.values = data_record[self.KEY_VALUES]

        self._update_statistics()

    def _update_statistics(self):
        from itertools import izip
        self.total_desc.set('Times : %2d ' % self.statistic_tacker.times)
        for i in range(4):
            self.drop_vars[i].set(self.statistic_tacker.drops[i])
        self.values_desc.set('Value : %2d ' % (sum(p*q for p,q in izip(
            self.values, self.statistic_tacker.get_statistics_ratio())) / 100))

    def _init_buttons_state(self):
        self.box_1_button.set_is_selected(True)
        self.box_2_button.set_is_selected(True)
        self.box_3_button.set_is_selected(False)
        self.box_4_button.set_is_selected(False)

    def submitting(self):
        self.statistic_tacker.record([self.box_1_button.is_selected, self.box_2_button.is_selected,
                                      self.box_3_button.is_selected, self.box_4_button.is_selected])

        data_record = get_data_record(self.section)
        data_record[self.KEY_TOTAL] = self.statistic_tacker.times
        data_record[self.KEY_DROPS] = self.statistic_tacker.drops
        save_data_record()

        self._init_buttons_state()
        self._update_statistics()
