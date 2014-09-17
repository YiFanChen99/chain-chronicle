# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MainFrame import *
from BasicWindow import *
import UpdateCharacterWindow
import Utilities
from datetime import timedelta

DB_TABLE = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']


class RecordOfDrawLots(MainFrameWithTable):
    def __init__(self, master, db_suffix):
        MainFrameWithTable.__init__(self, master, db_suffix=db_suffix)
        self.set_table_place(34, 29)

        self.events = DATABASE.execute('select Name, End from ' +
                                       self.compose_table_name('EventOfDrawLots')).fetchall()

        self.__init_add_record_frame()
        self.__init_filter_frame()

        self.records_filter = Utilities.RecordsFilter('select * from ' +
                                                      self.compose_table_name('RecordOfDrawLots'))

        # 呈現資料的表格
        self.table.tkraise()  # 避免被其他元件遮到
        self.updating_table()

    # noinspection PyAttributeOutsideInit
    def __init_add_record_frame(self):
        # 選擇是否允許記錄舊酒廠
        self.is_show_old_events = BooleanVar()
        check_button = Checkbutton(self, variable=self.is_show_old_events)
        check_button.place(x=8, y=48)
        label = Label(self, text='舊', font=(MS_JH, 10))
        label.place(x=10, y=33)

        # 新增記錄的按鈕
        button = Button(self, text="新增記錄", width=2, height=14, wraplength=1, font=(MS_JH, 12))
        button.place(x=5, y=76)
        button["command"] = self.adding_record

    # noinspection PyAttributeOutsideInit
    def __init_filter_frame(self):
        basic_x = 20
        Label(self, text='E:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.event_filter = ttk.Combobox(self, state='readonly', width=14, justify=CENTER)
        self.event_filter['values'] = \
            insert_with_empty_str([event[0] for event in reversed(self.events)])
        self.event_filter.place(x=basic_x + 18, y=3)
        self.event_filter.bind('<<ComboboxSelected>>', self.updating_table)

        basic_x += 146
        Label(self, text='C:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.cost = ttk.Combobox(self, state='readonly', width=6, justify=CENTER)
        self.cost['values'] = insert_with_empty_str(DRAW_LOTS_COST)
        self.cost.place(x=basic_x + 20, y=3)
        self.cost.bind('<<ComboboxSelected>>', self.updating_table)

        basic_x += 91
        Label(self, text='P:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.profession = ttk.Combobox(self, state='readonly', width=4, justify=CENTER)
        self.profession['values'] = insert_with_empty_str(PROFESSIONS)
        self.profession.place(x=basic_x + 20, y=3)
        self.profession.bind('<<ComboboxSelected>>', self.updating_table)

        basic_x += 84
        Label(self, text='Total:', font=(MS_JH, 12)).place(x=basic_x, y=2)
        self.total_count = Label(self, font=(MS_JH, 12))
        self.total_count.place(x=basic_x + 44, y=2)

        basic_x += 83
        Label(self, text='SSR:', font=(MS_JH, 12)).place(x=basic_x, y=2)
        self.ssr_count = Label(self, font=(MS_JH, 10))
        self.ssr_count.place(x=basic_x + 34, y=-3)
        self.ssr_ratio = Label(self, font=(MS_JH, 9))
        self.ssr_ratio.place(x=basic_x + 44, y=13)

        basic_x += 80
        Label(self, text='SR:', font=(MS_JH, 12)).place(x=basic_x, y=2)
        self.sr_count = Label(self, font=(MS_JH, 10))
        self.sr_count.place(x=basic_x + 25, y=-3)
        self.sr_ratio = Label(self, font=(MS_JH, 9))
        self.sr_ratio.place(x=basic_x + 35, y=13)

        basic_x += 78
        Label(self, text='R:', font=(MS_JH, 12)).place(x=basic_x, y=2)
        self.r_count = Label(self, font=(MS_JH, 10))
        self.r_count.place(x=basic_x + 16, y=-3)
        self.r_ratio = Label(self, font=(MS_JH, 9))
        self.r_ratio.place(x=basic_x + 26, y=13)

        # 清空進行篩選的條件
        button = Button(self, text="清空條件", width=7, font=(MS_JH, 11))
        button.place(x=658, y=-1)
        button["command"] = self.clearing_filter

    def update_all_records(self):
        self.records_filter.update_raw_records()
        self.updating_table()

    def clearing_filter(self):
        self.event_filter.set('')
        self.cost.set('')
        self.profession.set('')
        self.updating_table()

    def adding_record(self):
        popup = AddRecordWindow(self.db_suffix, self.get_suitable_event_names(), self.update_all_records)
        self.wait_window(popup)

    # 若有要求只顯示恰當的酒廠，則會計算結束日期滿足條件才會加入
    def get_suitable_event_names(self):
        names = []
        available_time = datetime.now() - timedelta(days=3)

        for each_event in self.events:
            if not self.is_show_old_events.get() and convert_str_to_datetime(each_event[1]) < available_time:
                pass
            else:
                names.append(each_event[0])
        return names

    # noinspection PyUnusedLocal
    def updating_table(self, event=None):
        self.table_model = TableModel()

        for column in DB_TABLE:
            self.table_model.addColumn(column)

        self.__update_filters()
        results = self.records_filter.filtered_records
        if len(results) == 0:
            self.table_model.addRow(Times=0, Event='無任何記錄')
        else:
            for row in results:
                data = iter(list(row))
                self.table_model.addRow(Times=next(data), Event=convert_to_str(next(data)),
                                        Profession=convert_to_str(next(data)), Rank=next(data),
                                        Character=convert_to_str(next(data)),
                                        Cost=convert_to_str(next(data)))

        self.table_model.setSortOrder(columnName=DB_TABLE[0], reverse=1)

        self.redisplay_table()

        # 連動更新統計資料
        self.__update_statistic()

    def __update_filters(self):
        self.records_filter.clear_filters()

        # 依序對活動、花費與職業進行篩選(if需要)
        event = self.event_filter.get()
        if event != '':
            self.records_filter.add_filter(1, event)
        cost = self.cost.get()
        if cost != '':
            self.records_filter.add_filter(5, cost)
        profession = self.profession.get()
        if profession != '':
            self.records_filter.add_filter(2, profession)

    def __update_statistic(self):
        # doing statistic
        total = 0
        ssr = 0
        sr = 0
        r = 0
        for record in self.records_filter.filtered_records:
            total += 1
            rank = record[3]
            if rank == 5:
                ssr += 1
            elif rank == 4:
                sr += 1
            else:
                r += 1

        # 特殊情況，顯示為 0 並結束
        if total == 0:
            self.total_count["text"] = 0
            self.ssr_count["text"] = 0
            self.ssr_ratio["text"] = 0
            self.sr_count["text"] = 0
            self.sr_ratio["text"] = 0
            self.r_count["text"] = 0
            self.r_ratio["text"] = 0
            return

        self.total_count["text"] = '%3d' % total
        self.ssr_count["text"] = ssr
        self.ssr_ratio["text"] = self.convert_to_ratio(total, ssr)
        self.sr_count["text"] = sr
        self.sr_ratio["text"] = self.convert_to_ratio(total, sr)
        self.r_count["text"] = r
        self.r_ratio["text"] = self.convert_to_ratio(total, r)

    @staticmethod
    def convert_to_ratio(total, numerator):
        ratio = round(100.0 * numerator / total, 1)
        return str(ratio) + '%'


class AddRecordWindow(BasicWindow):
    def __init__(self, db_suffix, event_names, callback):
        BasicWindow.__init__(self, width=565, height=118)
        self.window.title('Add new record')

        self.callback = callback

        self.record_table = 'RecordOfDrawLots' + db_suffix
        # 取得最近一筆資料，以作為預設值
        command = 'select * from ' + self.record_table + \
                  ' where Times = (select max(Times) from ' + self.record_table + ')'
        self.last_record = DATABASE.execute(command).fetchone()

        self.characters = None
        self.update_characters()

        self.__init_widgets(event_names)

    # noinspection PyAttributeOutsideInit
    def __init_widgets(self, event_names):
        # 各 Column 的標題: 筆數, 酒廠, 職業, 等級, 角色, 花費
        Label(self.window, text=DB_TABLE[0], width=6, font=("", 12)).place(x=3, y=9)
        Label(self.window, text=DB_TABLE[1], width=14, font=("", 12)).place(x=56, y=9)
        Label(self.window, text=DB_TABLE[2], width=7, font=("", 12)).place(x=200, y=9)
        Label(self.window, text=DB_TABLE[3], width=5, font=("", 12)).place(x=286, y=9)
        Label(self.window, text=DB_TABLE[4], width=11, font=("", 12)).place(x=349, y=9)
        Label(self.window, text=DB_TABLE[5], width=9, font=("", 12)).place(x=453, y=9)

        # 下一次的筆數
        self.times = Variable()
        Label(self.window, textvariable=self.times, width=6, font=("", 12)).place(x=3, y=40)

        # 選擇酒廠
        self.event_selector = ttk.Combobox(self.window, state='readonly', width=14, justify=CENTER)
        self.event_selector['values'] = event_names
        self.event_selector.place(x=63, y=40)

        # 選擇職業
        self.profession_selector = ttk.Combobox(self.window, state='readonly', width=7, justify=CENTER)
        self.profession_selector['values'] = PROFESSIONS
        self.profession_selector.place(x=199, y=40)
        self.profession_selector.bind('<<ComboboxSelected>>', self.updating_character_selector)

        # 選擇等級
        self.rank_selector = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.rank_selector['values'] = RANKS_WHEN_DRAW_LOTS
        self.rank_selector.place(x=285, y=40)
        self.rank_selector.bind('<<ComboboxSelected>>', self.updating_character_selector)

        # 選擇角色
        self.character_selector = ttk.Combobox(self.window, state='readonly', width=10, justify=CENTER)
        self.character_selector.place(x=358, y=40)

        # 選擇花費
        self.cost_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
        self.cost_selector['values'] = DRAW_LOTS_COST
        self.cost_selector.place(x=463, y=40)

        # 送交的按鈕
        button = Button(self.window, text="新增此記錄", width=38, borderwidth=3)
        button.place(x=28, y=79)
        button["command"] = self.submitting

        # 新增角色的按鈕
        button = Button(self.window, text="新增角色", width=12, borderwidth=3)
        button.place(x=326, y=79)
        button["command"] = self.adding_new_character

        # 取消並關閉的按鈕
        button = Button(self.window, text="關閉視窗", width=12, borderwidth=3)
        button.place(x=438, y=79)
        button["command"] = self.closing_window

        self.update_by_last_record()

    def update_by_last_record(self):
        self.times.set(self.last_record[0] + 1)
        self.event_selector.set(self.last_record[1])
        self.updating_character_selector()
        self.cost_selector.set(self.last_record[5])

    def submitting(self):
        if self.is_new_record_legal():
            DATABASE.execute('insert into ' + self.record_table +
                             '(' + ','.join(DB_TABLE) + ')' +
                             convert_data_to_insert_command(self.times.get(), self.event_selector.get(),
                                                            self.profession_selector.get(), self.rank_selector.get(),
                                                            self.character_selector.get(), self.cost_selector.get()))
            DATABASE.commit()

            # 更新顯示的資料
            self.last_record = [self.times.get(), self.event_selector.get(),
                                self.profession_selector.get(), self.rank_selector.get(),
                                self.character_selector.get(), self.cost_selector.get()]
            self.update_by_last_record()
            self.callback()

    def is_new_record_legal(self):
        error_message = ''
        if self.profession_selector.get() == '':
            error_message += '\"Profession\" 未填\n'
        if self.rank_selector.get() == '':
            error_message += '\"Rank\" 未填\n'
        if self.character_selector.get() == '':
            error_message += '\"Character\" 未填\n'

        is_legal = (error_message == '')
        if not is_legal:
            tkMessageBox.showwarning("Can not add this record", error_message)

        return is_legal

    # noinspection PyUnusedLocal
    def updating_character_selector(self, event=None):
        requested_profession = self.profession_selector.get()
        requested_rank = self.rank_selector.get()

        # 依序對職業與等級進行篩選(if需要)
        character_matched = []
        for character_infos in self.characters:
            if (requested_profession == '' or requested_profession == character_infos[1]) and \
                    (requested_rank == '' or int(requested_rank) == character_infos[2]):
                character_matched.append(character_infos[0])

        self.character_selector['values'] = character_matched
        self.character_selector.set('')

    def adding_new_character(self):
        popup = UpdateCharacterWindow.UpdateCharacterWindow()
        self.wait_window(popup)
        self.update_characters()
        self.updating_character_selector()

    def update_characters(self):
        self.characters = DATABASE.execute('select Nickname, Profession, Rank from Character').fetchall()

    def closing_window(self):
        self.destroy()