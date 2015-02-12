# -*- coding: utf-8 -*-
""" 暫訂維持 DB 的設計，不改成只存 c_id 後 join 的方式取得資料（簡單方便） """
from BaseFrame import *
from Window.RecordOfDrawLotsWindow import AddRecordWindow, UpdatingRecordWindow
from ModelUtility.DBAccessor import *
from ModelUtility.Utility import bind_check_box_and_label, convert_str_to_date
from ModelUtility.CommonState import *
from UIUtility.Combobox import FilteredCombobox, IntFilteredCombobox
from ModelUtility.Filter import FilterRuleManager
from datetime import timedelta, date

DB_TABLE = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']
EVENT_DURATION_TOLERANCE = 2


class RecordOfDrawLotsFrame(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(34, 29)

        self.filter_manager = FilterRuleManager()
        self.records = None
        self.events = DBAccessor.execute('select Name, End from EventOfDrawLots' + get_db_suffix()).fetchall()

        self._init_add_record_frame()
        self._init_filter_frame()

        # 呈現資料的表格
        self.table.tkraise()  # 放上層，避免被其他元件遮到
        self.update_all_records()

    # noinspection PyAttributeOutsideInit
    def _init_add_record_frame(self):
        # 選擇是否允許記錄舊酒廠
        self.is_show_old_events = BooleanVar()
        check_button = Checkbutton(self, variable=self.is_show_old_events)
        check_button.place(x=8, y=48)
        label = Label(self, text='舊', font=(MS_JH, 10))
        label.place(x=10, y=33)
        bind_check_box_and_label(check_button, label)

        # 新增記錄的按鈕
        button = Button(self, text="新增記錄", width=2, height=14, wraplength=1, font=(MS_JH, 12))
        button.place(x=5, y=76)
        button["command"] = self.adding_record

    # noinspection PyAttributeOutsideInit
    def _init_filter_frame(self):
        basic_x = 20
        Label(self, text='E:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.event_filter = FilteredCombobox(self, width=14, justify=CENTER)
        self.event_filter['values'] = [event[0] for event in reversed(self.events)]
        self.event_filter.place(x=basic_x + 18, y=3)
        self.event_filter.bind('<<ComboboxSelected>>',
                               lambda x: (self.filter_manager.set_specific_condition(1, self.event_filter.get()),
                                          self.updating_table()))

        basic_x += 146
        Label(self, text='C:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.cost_filter = FilteredCombobox(self, width=6, justify=CENTER)
        self.cost_filter['values'] = DRAW_LOTS_COST
        self.cost_filter.place(x=basic_x + 20, y=3)
        self.cost_filter.bind('<<ComboboxSelected>>',
                              lambda x: (self.filter_manager.set_specific_condition(5, self.cost_filter.get()),
                                         self.updating_table()))

        basic_x += 91
        Label(self, text='R:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.rank_filter = IntFilteredCombobox(self, width=4, justify=CENTER)
        self.rank_filter['values'] = RANKS_WHEN_DRAW_LOTS
        self.rank_filter.place(x=basic_x + 20, y=3)
        self.rank_filter.bind('<<ComboboxSelected>>',
                              lambda x: (self.filter_manager.set_specific_condition(3, self.rank_filter.get()),
                                         self.updating_table()))

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
        self.records = DBAccessor.execute('select * from RecordOfDrawLots' + get_db_suffix()).fetchall()
        self.updating_table()

    def clearing_filter(self):
        self.event_filter.set('')
        self.cost_filter.set('')
        self.rank_filter.set('')
        self.filter_manager.clean_specific_condition()
        self.updating_table()

    def adding_record(self):
        # 該 Window 預設送出後不關閉，故需要提供更新的 callback method
        # 理論上該 callback 將記錄插入 self.records 即可，但目前偷懶讓他全部更新
        AddRecordWindow(self, self.get_suitable_event_names(), self.update_all_records)

    # 若有要求只顯示恰當的酒廠，則會計算結束日期滿足條件才會加入
    def get_suitable_event_names(self):
        names = []
        available_time = date.today() - timedelta(days=EVENT_DURATION_TOLERANCE)

        for each_event in self.events:
            if not self.is_show_old_events.get() and convert_str_to_date(each_event[1]) < available_time:
                pass
            else:
                names.append(each_event[0])
        return names

    # noinspection PyUnusedLocal
    def updating_table(self, event=None):
        self.table_model = TableModel()

        for column in DB_TABLE:
            self.table_model.addColumn(column)

        results = self.filter_manager.filter(self.records)
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

        self.redisplay_table(is_reset_model=True)

        # 就篩選結果更新統計資料
        self._update_statistic_by_specific_results(results)

    def _update_statistic_by_specific_results(self, results):
        # doing statistic
        total = 0
        ssr = 0
        sr = 0
        r = 0
        for record in results:
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

    def do_double_clicking(self, event):
        row = self.table_view.get_row_clicked(event)
        record = self.get_record_by_times(int(self.table_model.getCellRecord(row, 0)))
        UpdatingRecordWindow(self, self.get_suitable_event_names(), record, callback=self.update_all_records)

    def do_dragging_along_right(self, row_number):
        times = self.table_model.getCellRecord(row_number, 0)

        # 確認是否刪除
        if tkMessageBox.askyesno('Deleting',
                                 'Are you sure you want to delete the {0}th record ?'.format(times), parent=self):
            DBAccessor.execute('delete from RecordOfDrawLots{0} where Times={1}'.format(get_db_suffix(), times))
            DBAccessor.commit()

        # 從已撈出的資料中將之移除，並更新顯示
        for record in self.records:
            if record[0] == int(times):
                self.records.remove(record)
        self.updating_table()

    def get_record_by_times(self, times):
        for each_record in self.records:
            if each_record[0] == times:
                return each_record
