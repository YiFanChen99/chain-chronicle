# -*- coding: utf-8 -*-
from UI.Utility.BasicMainFrame import *
from UI.Utility.Combobox import FilteredCombobox, IntFilteredCombobox, FilteredObjectCombobox
from UI.DrawLots.RecordOfDrawLotsWindow import *
from UI.DrawLots.EventOfDrawLotsWindow import *
from UI.Character.CharacterWindow import open_updating_character_window
from ModelUtility.DataObject import RecordOfDrawLots
from ModelUtility.Filter import FilterRuleManager
from Model import DrawLotsModel


class DrawLotsFrame(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        self.set_table_place(34, 29)
        self.table_model = TableModelAdvance()
        self.table_model.set_columns(RecordOfDrawLots.TABLE_VIEW_COLUMNS)
        # 滑鼠中鍵事件註冊，設定為更改角色詳細資訊，並選取該列
        self.table_view.bind("<Button-2>", lambda event: self.opening_character_update_window(event))
        self.table_view.setModel(self.table_model)

        self.filter_manager = FilterRuleManager()
        self.records = DrawLotsModel.select_record_list()
        self.events = DrawLotsModel.select_event_list()

        self._init_adding_frame()
        self._init_filter_frame()

        self.table.tkraise()  # 放上層，避免被其他元件遮到
        self.update_table()

    def _init_adding_frame(self):
        # 新增酒廠的按鈕
        button = Button(self, text="新增酒廠", width=2, height=5, wraplength=1, font=(MS_JH, 11))
        button.place(x=7, y=41)
        button["command"] = lambda: open_adding_event_window(self, lambda event: (
            self.events.insert(0, event), self.event_filter.set_objects(self.events)))

        # 新增記錄的按鈕
        button = Button(self, text="新增記錄", width=2, height=12, wraplength=1, font=(MS_JH, 12))
        button.place(x=5, y=155)
        button['command'] = self.adding_record
        button.bind('<Button-3>', lambda event: self.adding_record(limitation=False))

    def _init_filter_frame(self):
        basic_x = 20
        Label(self, text='E:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.event_filter = FilteredObjectCombobox(
            self, setter=lambda obj: obj.name, getter=lambda obj: obj.e_id, width=16, justify=CENTER)
        self.event_filter.set_objects(self.events)
        self.event_filter.place(x=basic_x + 18, y=3)
        self.event_filter.bind('<<ComboboxSelected>>',
                               lambda x: (self.filter_manager.set_specific_condition(
                                   'event_id', self.event_filter.get()), self.update_table()), add='+')
        self.event_filter.bind('<Button-2>', lambda event: (open_updating_event_window(
            self, self.event_filter.selected_object, lambda: self.event_filter.set_objects(self.events))))

        basic_x += 158
        Label(self, text='C:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.cost_filter = FilteredCombobox(self, width=6, justify=CENTER)
        self.cost_filter['values'] = DRAW_LOTS_COST
        self.cost_filter.place(x=basic_x + 20, y=3)
        self.cost_filter.bind('<<ComboboxSelected>>',
                              lambda x: (self.filter_manager.set_specific_condition('cost', self.cost_filter.get()),
                                         self.update_table()))

        basic_x += 90
        Label(self, text='R:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.rank_filter = IntFilteredCombobox(self, width=3, justify=CENTER)
        self.rank_filter['values'] = [5, 4, 3]
        self.rank_filter.place(x=basic_x + 20, y=3)
        self.rank_filter.bind('<<ComboboxSelected>>',
                              lambda x: (self.filter_manager.set_specific_condition('rank', self.rank_filter.get()),
                                         self.update_table()))

        basic_x = 342
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

    def update_table(self):
        results = self.filter_manager.filter(self.records)
        self.table_model.set_rows([result.get_table_view_info() for result in results])
        self.table_model.setSortOrder(columnName='Order', reverse=1)
        self.redisplay_table()
        self.table_view.resizeColumn(0, 55)  # DrawOrder
        self.table_view.resizeColumn(1, 178)  # Event
        self.table_view.resizeColumn(4, 120)  # Character

        # 就篩選結果更新統計資料
        self._update_statistic_by_specific_results(results)

    def _update_statistic_by_specific_results(self, results):
        # doing statistic: total, ssr, sr, r
        statistic = [0, 0, 0, 0]
        for record in results:
            record.take_statistic(statistic)

        # 特殊情況，顯示為 0 並結束
        if statistic[0] == 0:
            self.total_count["text"] = 0
            self.ssr_count["text"] = 0
            self.ssr_ratio["text"] = 0
            self.sr_count["text"] = 0
            self.sr_ratio["text"] = 0
            self.r_count["text"] = 0
            self.r_ratio["text"] = 0
            return

        self.total_count["text"] = '%3d' % statistic[0]
        self.ssr_count["text"] = statistic[1]
        self.ssr_ratio["text"] = self.convert_to_ratio(statistic[0], statistic[1])
        self.sr_count["text"] = statistic[2]
        self.sr_ratio["text"] = self.convert_to_ratio(statistic[0], statistic[2])
        self.r_count["text"] = statistic[3]
        self.r_ratio["text"] = self.convert_to_ratio(statistic[0], statistic[3])

    @staticmethod
    def convert_to_ratio(total, numerator):
        ratio = round(100.0 * numerator / total, 1)
        return str(ratio) + '%'

    def clearing_filter(self):
        self.event_filter.set(None)
        self.cost_filter.set('')
        self.rank_filter.set('')
        self.filter_manager.clean_specific_condition()
        self.update_table()

    def adding_record(self, limitation=True):
        open_adding_new_record_window(self, DrawLotsModel.get_suitable_events(self.events, limitation), lambda record: (
            self.records.append(record), self.update_table()))

    def do_double_clicking(self, event):
        record = self.get_record_by_order(self.table_model.getCellRecord(self.table_view.get_row_clicked(event), 0))
        open_updating_record_window(self, record, self.events, callback=self.update_table)

    def do_dragging_along_right(self, row_number):
        record = self.get_record_by_order(self.table_model.getCellRecord(row_number, 0))
        delete_record_with_conforming(
            self, record, lambda: (self.records.remove(record), self.update_table()))  # 直接從 list 中拿掉，不用重撈)

    def get_record_by_order(self, order):
        for each_record in self.records:
            if each_record.order == order:
                return each_record

    # 更改角色資訊
    def opening_character_update_window(self, event):
        self.table_view.handle_left_click(event)
        character = self.get_record_by_order(
            self.table_model.getCellRecord(self.table_view.get_row_clicked(event), 0)).character
        open_updating_character_window(self, character, lambda: None)


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_record_with_conforming(master, record, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete record order 「{0}」？'.format(
            record.times), parent=master):
        DrawLotsModel.delete_record_from_db(record)
        callback()