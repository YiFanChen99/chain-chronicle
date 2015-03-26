# -*- coding: utf-8 -*-
from datetime import datetime
from UI.Utility.BasicMainFrame import *
from UI.Utility.Button import ToggleButton
from ModelUtility.CommonState import *
from ModelUtility.DBAccessor import *
from ModelUtility.GroupController import RadioGroupController
from ModelUtility import APTimeCalculator

_DAILY_MISSIONS = ['週一法師', '週二戰士', '週三騎士', '週四僧侶', '週五弓手', '週末金錢']
_ALL_MISSIONS = '週一～五'
_DIFFICULTY = ['初級', '中級']
_RECORD_TABLE = ['Total', 'Item1', 'Item2', 'Item3', 'Item4']
_BUTTON_GROUP_BG = '#%02x%02x%02x' % (192, 192, 192)


class IndexFrame(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        PowerConverterCanvas(self, 'Fuji Account').place(x=5, y=15)
        PowerConverterCanvas(self, 'Yama Account').place(x=196, y=15)
        PowerConverterCanvas(self, 'Shiki Account').place(x=387, y=15)

        DailyDroppedRecorder(self).place(x=576, y=0)


class PowerConverterCanvas(Canvas):
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
        entry = Entry(self, width=4, textvariable=self.current_ap, font=(MS_JH, 12))
        entry.grid(row=row, **entry_config)
        entry.bind('<Return>', lambda event: self.calculate_for_max_ap())

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
        Label(self, textvariable=self.difference_for_max, font=(MS_JH, 10)).grid(row=row, padx=5, pady=2, **span_config)

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
        self.difference_for_max.set('%02d+%02d AP --> ' % (current_ap, difference_ap) +
                                    self.convert_timedelta_to_str(difference_time))
        self.time_reaching_max_ap.set('Reached :  ' +
                                      self.convert_time_to_str(datetime.now() + difference_time))

        # Saving data
        data_record = get_data_record(self.title)
        data_record[self.KEY_LAST_TIME] = self.last_calculation.get()
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


class DailyDroppedRecorder(Frame):
    def __init__(self, master, width=180, height=MIN_HEIGHT, **kwargs):
        Frame.__init__(self, master, width=width, height=height, **kwargs)

        self.stage_model = StageDroppedRecordModel()
        self._init_widgets()

        # 根據配置元件的狀態更新 Model
        self.change_stage()

    def _init_widgets(self):
        current_y = 8
        self._init_selecting_mission_widgets(current_y)

        current_y += 150
        self._init_selecting_difficulty_widgets(current_y)

        # 配置「掉箱情況」區塊
        current_y += 47
        self.dropped_or_not_frame = CurrentDropped(self, self.stage_model, width=180, height=89)
        self.dropped_or_not_frame.place(x=0, y=current_y)

        # 配置顯示統計數據區塊
        current_y += 94
        self.vars = []
        self._init_statistics_widgets(current_y)

    # 配置「曜日選擇」區塊，並根據目前時間初始化
    def _init_selecting_mission_widgets(self, y_pos):
        mission_frame = Frame(self, width=180, height=149, bg=_BUTTON_GROUP_BG)
        mission_frame.place(x=0, y=y_pos)
        self.mission_group = RadioGroupController(lambda: None)

        for index in range(len(_DAILY_MISSIONS)):
            # 設置成 左-右-換行左-右 的配置
            local_x_pos = 5 + 88 * (index % 2)
            local_y_pos = 4 + 36 * (index / 2)

            button = Button(mission_frame, text=_DAILY_MISSIONS[index], width=8, font=(MS_JH, 11))
            button.place(x=local_x_pos, y=local_y_pos)
            self.mission_group.group_button(button)

        # 最後放上全部統計的選項
        button = Button(mission_frame, text=_ALL_MISSIONS, width=12, font=(MS_JH, 11))
        button.place(x=29, y=113)
        self.mission_group.group_button(button)

        # 根據目前時間初始化呈現，但目前不會觸發任何事件
        self.mission_group.selecting_button(self.get_suitable_daily_mission_index())

        # 補回切換時的事件
        self.mission_group.callback = lambda: self.change_stage()

    # 配置「難度選擇」區塊
    def _init_selecting_difficulty_widgets(self, y_pos):
        difficulty_frame = Frame(self, width=180, height=41, bg=_BUTTON_GROUP_BG)
        difficulty_frame.place(x=0, y=y_pos)
        self.difficulty_group = RadioGroupController(lambda: None)

        for index in range(len(_DIFFICULTY)):
            # 左右配置
            local_x_pos = 5 + 88 * (index % 2)
            local_y_pos = 4 + 36 * (index / 2)

            button = Button(difficulty_frame, text=_DIFFICULTY[index], width=8, font=(MS_JH, 11))
            button.place(x=local_x_pos, y=local_y_pos)
            self.difficulty_group.group_button(button)

        # 預設選擇第一個，但目前不會觸發任何事件
        self.difficulty_group.selecting_button(0)

        # 補回切換時的事件
        self.difficulty_group.callback = lambda: self.change_stage()

    # 配置「統計數據」區塊
    def _init_statistics_widgets(self, y_pos):
        self.create_label(width=16, font_size=14, x_pos=0, y_pos=y_pos)

        y_pos += 31
        self.create_label(width=9, font_size=11, x_pos=-1, y_pos=y_pos)
        self.create_label(width=9, font_size=11, x_pos=90, y_pos=y_pos)

        y_pos += 29
        self.create_label(width=9, font_size=11, x_pos=-1, y_pos=y_pos)
        self.create_label(width=9, font_size=11, x_pos=90, y_pos=y_pos)

    # 改變「掉箱情況」區塊的顯示，並重新抓出對應關卡的數據
    def change_stage(self):
        # 若選擇「週一～五」時，禁止新增記錄，統計方法改變
        if self.mission_group.current_selection == len(_DAILY_MISSIONS):
            self.dropped_or_not_frame.submit_button['state'] = DISABLED
            self.updating_statistics(collect_all_statistics(_DIFFICULTY[self.difficulty_group.current_selection]))
        else:  # 其他選擇下，恢復允許新增記錄，並對單項統計
            self.dropped_or_not_frame.submit_button['state'] = NORMAL
            self.stage_model.change_stage_by_name(_DAILY_MISSIONS[self.mission_group.current_selection] +
                                                  _DIFFICULTY[self.difficulty_group.current_selection])
            self.dropped_or_not_frame.change_texts()
            self.updating_statistics(self.stage_model.collect_statistics())

    # noinspection PyUnusedLocal
    def updating_statistics(self, statistics):
        texts = ['Samples : ', '1st: ', '2nd: ', '3rd: ', '4th: ']

        samples, ratios = statistics
        if samples == 0:
            self.vars[0].set('無任何記錄')
            for index in range(1, 5):
                self.vars[index].set('')
        else:
            self.vars[0].set(texts[0] + str(samples))
            for index in range(1, 5):
                self.vars[index].set(texts[index] + '%2.1f%%' % (ratios[index - 1] * 100))

    @staticmethod
    # 回傳適合目前時間使用的曜日類別的位置
    def get_suitable_daily_mission_index():
        weekday = datetime.now().weekday()
        return weekday if weekday < 5 else 5

    # 在給定的位置新增 Label，並將其控制顯示的變數加到 vars 中
    def create_label(self, width, font_size, x_pos, y_pos):
        var = StringVar()
        Label(self, width=width, textvariable=var, font=(MS_JH, font_size)).place(x=x_pos, y=y_pos)
        self.vars.append(var)


# 記錄提升的掉箱率與掉箱情況，以送出到 StageDroppedRecordModel
class CurrentDropped(Frame):
    DEFAULT_DROPS = [1, 0, 0, 0]

    def __init__(self, master, stage_model, **kwargs):
        Frame.__init__(self, master, bg=_BUTTON_GROUP_BG, **kwargs)
        self.pack(fill=BOTH, expand=1)

        self._init_widgets()
        self.stage_model = stage_model

    def _init_widgets(self):
        self.drop_buttons = []
        for index in range(4):
            button = ToggleButton(self, selected=self.DEFAULT_DROPS[index], width=5, font=(MS_JH, 9))
            button.place(x=1 + 45 * index, y=2)
            self.drop_buttons.append(button)

        self.raised_group = RadioGroupController(lambda: None)
        button = Button(self, text='強運', width=12, font=(MS_JH, 9))
        button.place(x=1, y=30)
        self.raised_group.group_button(button)
        button = Button(self, text='帕布利卡', width=11, font=(MS_JH, 9))
        button.place(x=94, y=30)
        self.raised_group.group_button(button)
        # 預設選擇第一個
        self.raised_group.selecting_button(0)

        self.submit_button = Button(self, text='記錄', width=24, font=(MS_JH, 9))
        self.submit_button.place(x=2, y=60)
        self.submit_button['command'] = self.submitting

    # 將選擇的情況通知 stage_model，並還原到預設值
    def submitting(self):
        raised = 0.3 if (self.raised_group.current_selection == 0) else 0.35

        drops = []
        for index in range(4):
            drops.append(self.drop_buttons[index].is_selected)
            self.drop_buttons[index].set_is_selected(self.DEFAULT_DROPS[index])

        self.stage_model.add_record(raised, drops)

        # 通知 master 更新統計結果
        self.master.updating_statistics(self.stage_model.collect_statistics())

    def change_texts(self):
        texts = self.stage_model.get_dropped_items_names()
        for index in range(4):
            self.drop_buttons[index]['text'] = texts[index]


# 負責更新與統計此 Stage 的掉落情形
class StageDroppedRecordModel():
    def __init__(self, stage_id=19):
        self.stage_id = stage_id

    def add_record(self, raised, new_drops):
        total_drops = list(DBAccessor.execute('select {0} from StageDroppedRecord'.format(','.join(_RECORD_TABLE)) +
                                              ' where StageID={0} and Raised={1}'.format(self.stage_id, raised)
                                              ).fetchone())

        total_drops[0] += 1  # Total++
        for index in range(4):
            total_drops[index + 1] += (new_drops[index])

        DBAccessor.execute('update StageDroppedRecord' +
                           convert_data_to_update_command(_RECORD_TABLE, total_drops) +
                           ' where StageID={0} and Raised={1}'.format(self.stage_id, raised))
        DBAccessor.commit()

    # 提供外部使用
    def change_stage_by_name(self, stage_name, server_name='國服'):
        self.stage_id = DBAccessor.execute('select ID from Stage where Server={0} and Stage={1}'.format(
            convert_datum_to_command(server_name), convert_datum_to_command(stage_name))).fetchone()[0]

    def get_dropped_items_names(self):
        return DBAccessor.execute('select Name from StageDroppedItem, Item ' +
                                  'where StageDroppedItem.ItemID = Item.ID and StageID={0} '.format(self.stage_id) +
                                  'order by Position ASC').fetchall()

    def collect_statistics(self):
        (total, drop_ratios) = collect_stage_statistics(self.stage_id)

        if total != 0:
            for index in range(4):
                drop_ratios[index] /= total

        return total, drop_ratios


# 根據不同的關卡，算得特定掉落加成下的掉落機率
def collect_stage_statistics(stage_id):
    records = DBAccessor.execute('select Raised,{0} from StageDroppedRecord where StageID={1}'.format(
        ','.join(_RECORD_TABLE), stage_id)).fetchall()
    return calculate_rate_by_specific_dropped_raise(records)


# 根據一到五的不同難度耀日，算得特定掉落加成下的掉落機率
def collect_all_statistics(difficulty):
    records = DBAccessor.execute('select Raised,{0} from StageDroppedRecord, Stage'.format(','.join(_RECORD_TABLE)) +
                                 ' where ID=StageID and StageID>18 and StageID<31 and Stage like \'%' +
                                 difficulty + '\'').fetchall()

    total_count, raw_drops = calculate_rate_by_specific_dropped_raise(records)
    raw_drop_ratios = [0.0] * 4
    for i in range(4):
        raw_drop_ratios[i] += raw_drops[i] / total_count

    return total_count, raw_drop_ratios


# 計算一律帶強運時的掉落機率
def calculate_rate_by_specific_dropped_raise(records):
    total_count = 0
    raw_drops = [0.0] * 4

    for record in records:
        total_count += record[1]
        for i in range(4):
            raw_drops[i] += (record[i + 2] / (1 + record[0]) * 1.3)

    return total_count, raw_drops
