# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *
FONT = (MS_JH, 12)
# For PowerConverter
import codecs
from configparser3 import configparser
from datetime import timedelta
AP_FILE_NAME = 'data/AP.txt'
MAX_AP = 'Max AP'
LAST_CALCULATION = 'Last Calculation'
DIFFERENCE = 'Difference'
REACHED_TIME = 'Reached Time'
# For DailyDroppedRecorder
import Utilities
DAILY_MISSIONS = ['週一法師', '週二戰士', '週三騎士', '週四僧侶', '週五法師', '週末金錢']
ALL_MISSIONS = '週一～五'
DIFFICULTY = ['初級', '中級']


class Frequent(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        parser_of_power_converter = configparser.RawConfigParser()
        parser_of_power_converter.read(AP_FILE_NAME, "utf8")
        PowerConverter(self, 'Fuji Account', parser_of_power_converter, width=280, height=MIN_HEIGHT).place(x=5, y=0)
        PowerConverter(self, 'Yama Account', parser_of_power_converter, width=280, height=MIN_HEIGHT).place(x=289, y=0)

        DailyDroppedRecorder(self, width=180, height=MIN_HEIGHT).place(x=576, y=0)


class PowerConverter(Frame):
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
        left_x = 20
        middle_x = left_x + 106
        right_x = middle_x + 90

        current_y = 7
        Label(self, width=12, text=self.name, font=FONT).place(x=82, y=current_y)

        current_y += 33
        ttk.Separator(self, orient=HORIZONTAL).place(x=3, y=current_y, width=284)

        current_y += 10
        self.last_calculation = StringVar(value='')
        Label(self, width=20, textvariable=self.last_calculation, font=FONT).place(x=42, y=current_y)

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
        Label(self, width=20, textvariable=self.difference_for_max, font=FONT).place(x=42, y=current_y)

        current_y += 30
        self.time_reaching_max_ap = StringVar(value='')
        Label(self, width=20, textvariable=self.time_reaching_max_ap, font=FONT).place(x=42, y=current_y)

        current_y += 36
        ttk.Separator(self, orient=HORIZONTAL).place(x=3, y=current_y, width=284)

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
        Label(self, width=20, textvariable=self.difference_for_goal, font=FONT).place(x=42, y=current_y)

        current_y += 30
        self.time_reaching_goal_ap = StringVar(value='')
        Label(self, width=20, textvariable=self.time_reaching_goal_ap, font=FONT).place(x=42, y=current_y)

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
        with codecs.open(AP_FILE_NAME, encoding="utf8", mode='wb') as data_file:
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
        return '%02d : %02d' % (time.hour - 12 if time.hour > 12 else time.hour, time.minute)

    @staticmethod
    def convert_timedelta_to_str(the_timedelta):
        total_minutes = the_timedelta.seconds / 60
        minute = total_minutes % 60
        hour = total_minutes / 60
        return '%02d 小時 %02d 分' % (hour, minute)


class DailyDroppedRecorder(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)

        self.__init_widgets()

        # TODO 依照時間更換 current_mission

    def __init_widgets(self):
        current_y = 25
        self.__init_selecting_mission_widgets(current_y)

        current_y += 151
        self.__init_selecting_difficulty_widgets(current_y)

        current_y += 46
        self.__init_dropped_or_not_widgets(current_y)

    # 配置「曜日選擇」區塊
    def __init_selecting_mission_widgets(self, y_pos):
        self.current_mission = StringVar(value=DAILY_MISSIONS[0])
        self.current_mission.trace("w", self.updating_statistics)

        radiobuttons = Utilities.RadiobuttonController(self, width=180, height=149, button_type=1)
        radiobuttons.place(x=0, y=y_pos)

        for index in range(len(DAILY_MISSIONS)):
            def selecting_mission(my_index=index):
                self.current_mission.set(DAILY_MISSIONS[my_index])

            # 設置成 左-右-換行左-右 的配置
            x_pos = 5 + 88 * (index % 2)
            y_pos = 4 + 36 * (index / 2)
            radiobuttons.create_button(x_pos, y_pos, DAILY_MISSIONS[index], selecting_mission, width=8)

        # 最後放上全部統計的選項
        def selecting_all_mission():
            self.current_mission.set(ALL_MISSIONS)
        radiobuttons.create_button(29, 113, ALL_MISSIONS, selecting_all_mission, width=12)

        # 預設選擇第一個，並不觸發任何事件，配合初始 current_mission 的情況
        radiobuttons.selecting_button(0, None)

    # 配置「難度選擇」區塊
    def __init_selecting_difficulty_widgets(self, y_pos):
        self.current_difficulty = StringVar(value=DIFFICULTY[0])
        self.current_difficulty.trace("w", self.updating_statistics)

        radiobuttons = Utilities.RadiobuttonController(self, width=180, height=41, button_type=1)
        radiobuttons.place(x=0, y=y_pos)

        for index in range(len(DIFFICULTY)):
            def selecting_difficulty(my_index=index):
                self.current_difficulty.set(DIFFICULTY[my_index])

            # 左右配置
            x_pos = 5 + 88 * (index % 2)
            y_pos = 4 + 36 * (index / 2)
            radiobuttons.create_button(x_pos, y_pos, DIFFICULTY[index], selecting_difficulty, width=8)

        # 預設選擇第一個，並不觸發任何事件，配合初始 current_difficulty 的情況
        radiobuttons.selecting_button(0, None)

    # 配置「掉箱情況」區塊
    def __init_dropped_or_not_widgets(self, y_pos):
        aa = ['一星肥', '一星肥', '鍛造卡', '二星肥']  # TODO
        self.frame = DroppedOrNotRecorder(self, aa, width=180, height=61)
        self.frame.place(x=0, y=y_pos)

    # noinspection PyUnusedLocal  todo
    def updating_statistics(self, *args):
        print self.get_stage_name()

    # TODO 記錄到DB
    def submitting(self, values):
        print values
        self.updating_statistics()

    def get_stage_name(self):
        return self.current_mission.get() + self.current_difficulty.get()


class DroppedOrNotRecorder(Frame):
    DEFAULT_VARIABLES = [1, 0, 0, 0]

    def __init__(self, master, texts, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self['bg'] = '#%02x%02x%02x' % (192, 192, 192)  # 預設底色

        self.buttons = []
        for index in range(len(self.DEFAULT_VARIABLES)):
            button = Utilities.ToggleButton(self, selected=self.DEFAULT_VARIABLES[index], text=texts[index],
                                            width=5, font=(MS_JH, 9))
            button.place(x=1 + 45 * index, y=2)
            self.buttons.append(button)

        submit_button = Button(self, text='送出', width=24, font=(MS_JH, 9))
        submit_button.place(x=2, y=32)
        submit_button['command'] = self.submitting

    # 將選擇的情況通知 master，並還原到預設值
    def submitting(self):
        values = []
        for index in range(len(self.buttons)):
            values.append(self.buttons[index].is_selected)
            self.buttons[index].set_is_selected(self.DEFAULT_VARIABLES[index])
        self.master.submitting(values)