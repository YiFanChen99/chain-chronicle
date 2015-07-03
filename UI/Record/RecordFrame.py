# -*- coding: utf-8 -*-
from datetime import datetime
from UI.Utility.BasicMainFrame import *
from UI.Utility.Button import ToggleButton
from ModelUtility.StatisticTacker import DroppedStatisticTacker
from ModelUtility.CommonState import *
from ModelUtility import APTimeCalculator


class RecordFrame(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        PowerConverterCanvas(self, 'Yama Account').place(x=70, y=15)

        self.canvases = []
        self._init_canvases()
        self._place_canvases()

    def _init_canvases(self):
        self.canvases.append(SpecificStageDroppedCanvas(self, 'Advanced Daily', width=174))
        self.canvases.append(MonthlyDroppedCanvas(self, 'Monthly', width=174))
        self.canvases.append(SpecificStageDroppedCanvas(self, 'Stage 1', width=174))
        self.canvases.append(SpecificStageDroppedCanvas(self, 'Stage 2', width=174))

    def _place_canvases(self):
        for i in range(len(self.canvases)):
            x = 386 + 189 * (i % 2)
            y = -1 + 210 * (i >= 2)
            self.canvases[i].place(x=x, y=y)


class PowerConverterCanvas(Canvas):
    KEY_CURRENT_AP = 'current_ap'
    KEY_MAX_AP = 'max_ap'
    KEY_LAST_TIME = 'last_time'
    KEY_DIFFERENCE = 'difference'
    KEY_REACHED_TIME = 'reached_time'

    def __init__(self, master, title, **kwargs):
        Canvas.__init__(self, master, height=MIN_HEIGHT, highlightthickness=0, **kwargs)
        self.pack(fill=BOTH, expand=1)

        self.title = title
        self._init_widgets()

        # Loading data
        data_record = get_data_record(title)
        self.last_calculation.set(data_record[self.KEY_LAST_TIME])
        self.current_ap.set(data_record[self.KEY_CURRENT_AP])
        self.max_ap.set(data_record[self.KEY_MAX_AP])
        self.difference_for_max.set(data_record[self.KEY_DIFFERENCE])
        self.time_reaching_max_ap.set(data_record[self.KEY_REACHED_TIME])

    def _init_widgets(self):
        self.columnconfigure(0, weight=4)
        self.columnconfigure(2, weight=1)
        span_config = {'columnspan': 3, 'sticky': N+E+S+W}
        entry_config = {'column': 1, 'sticky': N+S, 'pady': 3, 'ipady': 2}

        row = 0
        Label(self, text=self.title, font=(MS_JH, 12)).grid(row=row, pady=5, **span_config)

        row += 1
        self._insert_separator(row, span_config)

        row += 1
        Label(self, text='Current AP', font=(MS_JH, 12)).grid(row=row, sticky=N+E+S+W)
        self.current_ap = StringVar(value='')
        current_ap_entry = Entry(self, width=4, textvariable=self.current_ap, font=(MS_JH, 12))
        current_ap_entry.grid(row=row, **entry_config)
        current_ap_entry.bind('<Return>', lambda event: self.calculate_for_max_ap())
        current_ap_entry.bind('<FocusIn>', lambda event: (
            current_ap_entry.focus_set(), current_ap_entry.selection_range(0, END)))

        row += 1
        Label(self, text='Max AP', font=(MS_JH, 12)).grid(row=row, sticky=N+E+S+W)
        self.max_ap = StringVar(value='89')
        entry = Entry(self, width=4, textvariable=self.max_ap, font=(MS_JH, 12))
        entry.grid(row=row, **entry_config)
        entry.bind('<Return>', lambda event: self.calculate_for_max_ap())

        row += 1
        Label(self, text='Adjustment', font=(MS_JH, 12)).grid(row=row, sticky=N+E+S+W)
        self.adjustment = StringVar(value='')
        Entry(self, width=4, textvariable=self.adjustment, font=(MS_JH, 12)).grid(row=row, **entry_config)

        row += 1
        self.last_calculation = StringVar(value='')
        Label(self, textvariable=self.last_calculation, font=(MS_JH, 11)).grid(row=row, pady=5, **span_config)

        row += 1
        self.difference_for_max = StringVar(value='')
        Label(self, textvariable=self.difference_for_max, font=(MS_JH, 11)).grid(row=row, padx=5, pady=1, **span_config)

        row += 1
        self.time_reaching_max_ap = StringVar(value='')
        Label(self, textvariable=self.time_reaching_max_ap, width=20, font=(MS_JH, 11)).\
            grid(row=row, pady=3, **span_config)

        row += 1
        self._insert_separator(row, span_config)

        row += 1
        Label(self, text='Goad AP', font=(MS_JH, 12)).grid(row=row, sticky=N+E+S+W, pady=3)
        self.goal = StringVar(value='')
        entry = Entry(self, width=4, textvariable=self.goal, font=(MS_JH, 12))
        entry.grid(row=row, **entry_config)
        entry.bind('<Return>', lambda event: self.calculate_for_goal_ap())

        row += 1
        self.difference_for_goal = StringVar(value='')
        Label(self, textvariable=self.difference_for_goal, font=(MS_JH, 10)).grid(row=row, pady=4, **span_config)

        row += 1
        self.time_reaching_goal_ap = StringVar(value='')
        Label(self, textvariable=self.time_reaching_goal_ap, font=(MS_JH, 11)).grid(row=row, **span_config)

    def _insert_separator(self, row, config):
        ttk.Separator(self, orient=HORIZONTAL).grid(row=row, pady=6, **config)

    def calculate_for_max_ap(self):
        # 計算並改動
        current_ap = int(self.current_ap.get()) if self.current_ap.get() else 0
        adjustment_ap = int(self.adjustment.get()) if self.adjustment.get() else 0
        difference_ap = int(self.max_ap.get()) - current_ap - adjustment_ap
        difference_time = APTimeCalculator.convert_ap_to_timedelta(difference_ap)
        self.last_calculation.set('Current :  ' + self.convert_time_to_str(datetime.now()))
        self.difference_for_max.set('%02d AP --> ' % difference_ap + self.convert_timedelta_to_str(difference_time))
        self.time_reaching_max_ap.set('Reached :  ' +
                                      self.convert_time_to_str(datetime.now() + difference_time))

        # Saving data
        data_record = get_data_record(self.title)
        data_record[self.KEY_LAST_TIME] = self.last_calculation.get()
        data_record[self.KEY_CURRENT_AP] = self.current_ap.get()
        data_record[self.KEY_MAX_AP] = self.max_ap.get()
        data_record[self.KEY_DIFFERENCE] = self.difference_for_max.get()
        data_record[self.KEY_REACHED_TIME] = self.time_reaching_max_ap.get()
        save_data_record()

    def calculate_for_goal_ap(self):
        # 計算並改動
        current_ap = int(self.current_ap.get()) if self.current_ap.get() else 0
        difference_ap = int(self.goal.get()) - current_ap
        difference_time = APTimeCalculator.convert_ap_to_timedelta(difference_ap)
        self.difference_for_goal.set('%02d+%02d AP --> ' % (current_ap, difference_ap) +
                                     self.convert_timedelta_to_str(difference_time))
        self.time_reaching_goal_ap.set('Reached :  ' +
                                       self.convert_time_to_str(datetime.now() + difference_time))

    @staticmethod
    def convert_time_to_str(time):
        if time.hour > 12:
            return '%02d:%02d PM' % (time.hour - 12, time.minute)
        else:
            return '%02d:%02d AM' % (time.hour, time.minute)

    @staticmethod
    def convert_timedelta_to_str(the_timedelta):
        total_minutes = the_timedelta.seconds / 60
        minute = total_minutes % 60
        hour = total_minutes / 60
        return '%02d 時 %02d 分' % (hour, minute)


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
    KEY_TITLE = 'title'
    KEY_TOTAL = 'total'
    KEY_DROPS = "drops"
    KEY_VALUES = "values"
    KEY_DEFAULTS = "defaults"

    def __init__(self, master, section, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        self.title = StringVar()
        self.section = section
        self._init_frame()
        self._init_fields()

    def _init_frame(self):
        Label(self, textvariable=self.title, width=13, font=(MS_JH, 14)).place(x=12, y=5)
        self.box_1_button = ToggleButton(self, text='1st', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_1_button.place(x=5 + 43 * 0, y=39)
        self.box_2_button = ToggleButton(self, text='2nd', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_2_button.place(x=5 + 43 * 1, y=39)
        self.box_3_button = ToggleButton(self, text='3rd', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_3_button.place(x=5 + 43 * 2, y=39)
        self.box_4_button = ToggleButton(self, text='4th', width=3, font=(SCP, 11), relief=RIDGE)
        self.box_4_button.place(x=5 + 43 * 3, y=39)

        submit_button = Button(self, text='Submit', width=17, font=(SCP, 11), relief=RIDGE)
        submit_button.place(x=5, y=76)
        submit_button.bind('<Button-1>', lambda event: self.submitting())

        current_y = 114
        self.total_desc = StringVar()
        Label(self, textvariable=self.total_desc, width=16, font=(SCP, 11)).place(x=13, y=current_y)
        current_y += 28
        self.drop_vars = [IntVar(), IntVar(), IntVar(), IntVar()]
        for i in range(4):
            Label(self, textvariable=self.drop_vars[i], width=3, font=(SCP, 11), relief=GROOVE). \
                place(x=6 + 43 * i, y=current_y)
        current_y += 29
        self.values_desc = StringVar()
        Label(self, textvariable=self.values_desc, width=16, font=(SCP, 11)).place(x=13, y=current_y)

    def _init_fields(self):
        data_record = get_data_record(self.section)
        self.title.set(data_record[self.KEY_TITLE])
        self.statistic_tacker = DroppedStatisticTacker(4)
        self.statistic_tacker.set(data_record[self.KEY_TOTAL], data_record[self.KEY_DROPS])
        self.values = data_record[self.KEY_VALUES]

        self._init_buttons_state(data_record[self.KEY_DEFAULTS])
        self._update_statistics()

    def _update_statistics(self):
        from itertools import izip

        self.total_desc.set('Times : %2d ' % self.statistic_tacker.times)
        for i in range(4):
            self.drop_vars[i].set(self.statistic_tacker.drops[i])
        self.values_desc.set('Value : %1.2f' % (sum(p * q for p, q in izip(
            self.values, self.statistic_tacker.get_statistics_ratio())) / 100))

    def _init_buttons_state(self, defaults):
        self.box_1_button.set_is_selected(defaults[0])
        self.box_2_button.set_is_selected(defaults[1])
        self.box_3_button.set_is_selected(defaults[2])
        self.box_4_button.set_is_selected(defaults[3])

    def submitting(self):
        self.statistic_tacker.record([self.box_1_button.is_selected, self.box_2_button.is_selected,
                                      self.box_3_button.is_selected, self.box_4_button.is_selected])

        data_record = get_data_record(self.section)
        data_record[self.KEY_TOTAL] = self.statistic_tacker.times
        data_record[self.KEY_DROPS] = self.statistic_tacker.drops
        save_data_record()

        self._init_buttons_state(data_record[self.KEY_DEFAULTS])
        self._update_statistics()
