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
DAILY_MISSIONS = ['週一法師', '週二戰士', '週三騎士', '週四僧侶', '週五弓手', '週末金錢']
ALL_MISSIONS = '週一～五'
DIFFICULTY = ['初級', '中級']
RECORD_TABLE = ['Total', 'Item1', 'Item2', 'Item3', 'Item4']


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

        self.stage_recorder = StageRecorder()
        self.__init_widgets()

        # 根據配置元件的設定更新 Model
        self.changing_state()

    def __init_widgets(self):
        current_y = 21
        self.__init_selecting_mission_widgets(current_y)

        current_y += 151
        self.__init_selecting_difficulty_widgets(current_y)

        # 配置「掉箱情況」區塊
        current_y += 49
        self.dropped_or_not_frame = DroppedOrNotRecorder(self, width=180, height=61)
        self.dropped_or_not_frame.place(x=0, y=current_y)

        # 配置顯示統計數據區塊
        current_y += 69
        self.vars = []
        self.__init_statistics_widgets(current_y)

    # 配置「曜日選擇」區塊，並根據目前時間初始化
    def __init_selecting_mission_widgets(self, y_pos):
        suitable_mission_index = self.get_suitable_daily_mission_index()
        self.current_mission = StringVar(value=DAILY_MISSIONS[suitable_mission_index])
        self.current_mission.trace("w", self.changing_state)

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

        # 根據目前時間初始化呈現，但於此不觸發任何事件
        radiobuttons.selecting_button(suitable_mission_index, None)

    # 配置「難度選擇」區塊
    def __init_selecting_difficulty_widgets(self, y_pos):
        self.current_difficulty = StringVar(value=DIFFICULTY[0])
        self.current_difficulty.trace("w", self.changing_state)

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

    # 配置「統計數據」區塊
    def __init_statistics_widgets(self, y_pos):
        self.create_label(width=16, font_size=14, x_pos=0, y_pos=y_pos)

        y_pos += 31
        self.create_label(width=9, font_size=11, x_pos=-1, y_pos=y_pos)
        self.create_label(width=9, font_size=11, x_pos=90, y_pos=y_pos)

        y_pos += 29
        self.create_label(width=9, font_size=11, x_pos=-1, y_pos=y_pos)
        self.create_label(width=9, font_size=11, x_pos=90, y_pos=y_pos)

    # noinspection PyUnusedLocal
    # 改變「掉箱情況」區塊的顯示，並重新抓出對應關卡的數據
    def changing_state(self, *args):
        # 若選擇「週一～五」時，禁止新增記錄，統計方法改變
        if self.current_mission.get().encode('utf-8') == ALL_MISSIONS:
            self.stage_recorder.collect_all(self.current_difficulty.get())
            self.dropped_or_not_frame.disable()
        else:  # 其他選擇下，恢復允許新增記錄，並對單項統計
            self.stage_recorder.change_stage(self.get_stage_name())
            self.dropped_or_not_frame.enable()
            self.dropped_or_not_frame.change_texts(self.stage_recorder.get_dropped_names())
        self.updating_statistics()

    # 新增資料到 Model，並更新回 DB
    def submitting(self, new_record):
        self.stage_recorder.add_record(new_record)
        DATABASE.execute('update StageDroppedRecord' +
                         convert_data_to_update_command(RECORD_TABLE, self.stage_recorder.records) +
                         ' where StageID=' + str(self.stage_recorder.id))
        DATABASE.commit()
        self.updating_statistics()

    # noinspection PyUnusedLocal
    def updating_statistics(self, *args):
        texts = ['Samples : ', '1st: ', '2nd: ', '3rd: ', '4th: ']

        samples = self.stage_recorder.records[0]
        if samples == 0:
            self.vars[0].set('無任何記錄')
            for index in range(1, 5):
                self.vars[index].set('')
        else:
            self.vars[0].set(texts[0] + str(samples))
            for index in range(1, 5):
                ratio = '%2.1f%%' % (self.stage_recorder.records[index] * 100.0 / samples)
                self.vars[index].set(texts[index] + ratio)

    @staticmethod
    # 回傳適合目前時間使用的曜日類別的位置
    def get_suitable_daily_mission_index():
        weekday = datetime.now().weekday()
        return weekday if weekday < 5 else 5

    def get_stage_name(self):
        return self.current_mission.get() + self.current_difficulty.get()

    # 在給定的位置新增 Label，並將其控制顯示的變數加到 vars 中
    def create_label(self, width, font_size, x_pos, y_pos):
        var = StringVar()
        Label(self, width=width, textvariable=var, font=(MS_JH, font_size)).place(x=x_pos, y=y_pos)
        self.vars.append(var)


class StageRecorder():
    def __init__(self, name=None):
        if name is not None:
            self.change_stage(name)

    # noinspection PyAttributeOutsideInit
    def change_stage(self, name):
        self.id = DATABASE.execute('select ID from Stage where Name=' +
                                   convert_datum_to_command(name)).fetchone()[0]
        self.records = list(DATABASE.execute('select ' + ','.join(RECORD_TABLE) +
                                             ' from StageDroppedRecord where StageID=' + str(self.id)).fetchone())

    # noinspection PyAttributeOutsideInit
    # 統計一～五的情況
    def collect_all(self, difficulty):
        self.id = -1
        self.records = [0, 0, 0, 0, 0]
        all_records = DATABASE.execute('select ' + ','.join(RECORD_TABLE) + ' from StageDroppedRecord, Stage' +
                                       ' where ID=StageID and StageID<12 and Name like \'%' + difficulty +
                                       '\'').fetchall()
        for records in all_records:
            for i in range(5):
                self.records[i] += records[i]

    def get_dropped_names(self):
        return DATABASE.execute('select Name from StageDroppedItem, Item' +
                                ' where StageDroppedItem.ItemID = Item.ID and StageID=' +
                                str(self.id) + ' order by Position ASC').fetchall()

    def add_record(self, new_record):
        self.records[0] += 1  # Total++
        for index in range(4):
            self.records[index + 1] += (new_record[index])


class DroppedOrNotRecorder(Frame):
    AMOUNT = 4
    DEFAULT_VARIABLES = [1, 0, 0, 0]

    def __init__(self, master, texts=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self['bg'] = '#%02x%02x%02x' % (192, 192, 192)  # 預設底色

        if texts is None:
            texts = [1, 2, 3, 4]

        self.buttons = []
        for index in range(self.AMOUNT):
            button = Utilities.ToggleButton(self, selected=self.DEFAULT_VARIABLES[index], text=texts[index],
                                            width=5, font=(MS_JH, 9))
            button.place(x=1 + 45 * index, y=2)
            self.buttons.append(button)

        self.submit_button = Button(self, text='記錄', width=24, font=(MS_JH, 9))
        self.submit_button.place(x=2, y=32)
        self.submit_button['command'] = self.submitting

    # 將選擇的情況通知 master，並還原到預設值
    def submitting(self):
        values = []
        for index in range(self.AMOUNT):
            values.append(self.buttons[index].is_selected)
            self.buttons[index].set_is_selected(self.DEFAULT_VARIABLES[index])
        self.master.submitting(values)

    def change_texts(self, texts):
        for index in range(self.AMOUNT):
            self.buttons[index]['text'] = texts[index]

    def enable(self):
        for button in self.buttons:
            button['state'] = NORMAL
        self.submit_button['state'] = NORMAL

    def disable(self):
        for button in self.buttons:
            button['state'] = DISABLED
        self.submit_button['state'] = DISABLED