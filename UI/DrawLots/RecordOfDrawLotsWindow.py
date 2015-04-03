# -*- coding: utf-8 -*-
from datetime import datetime
from UI.Utility.BasicWindow import *
from UI.Utility.CharacterSelector import CharacterSelectorCanvas
from UI.Utility.Combobox import ObjectCombobox
from ModelUtility.CommonValue import *
from ModelUtility.DataObject import RecordOfDrawLots
from Model import DrawLotsModel


class RecordWindow(BasicWindow):
    def __init__(self, master, record, events, callback, width=445, height=133, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)

        self.callback = callback
        self._init_widgets(events)
        self._init_context(record)

        # 註冊 Enter 確認送出
        self.bind('<Return>', lambda event: self.submitting())
        # 註冊編輯 DateTime 熱鍵
        self.bind('<Control-d>', lambda event: (
            self.date_time_entry.focus_set(), self.date_time_entry.selection_range(0, END)))

    def _init_widgets(self, events):
        # 筆數
        current_y = 15
        Label(self, text='Order', width=6, font=("", 12)).place(x=4, y=current_y)
        self.order = IntVar()  # 下一次的筆數
        Label(self, textvariable=self.order, width=6, font=("", 12)).place(x=4, y=current_y + 27)

        # 酒廠
        Label(self, text='Event', width=14, font=("", 12)).place(x=57, y=current_y)
        self.event_selector = ObjectCombobox(self, setter=lambda obj: obj.name, width=14, justify=CENTER)
        self.event_selector.set_objects(events)
        self.event_selector.place(x=64, y=current_y + 27)

        # 角色
        self.character_selector = CharacterSelectorCanvas(self)
        self.character_selector.place(x=201, y=current_y - 4)

        # 花費
        Label(self, text='Cost', width=9, font=("", 12)).place(x=338, y=current_y)
        self.cost_selector = ttk.Combobox(self, state='readonly', width=8, justify=CENTER)
        self.cost_selector['values'] = DRAW_LOTS_COST
        self.cost_selector.place(x=346, y=current_y + 27)

        # 時間欄位，送交、取消並關閉的按鈕
        current_y = 90
        self.date_time = StringVar()
        self.date_time_entry = Entry(self, textvariable=self.date_time, width=11, font=(SCP, 10), justify=CENTER)
        self.date_time_entry.place(x=14, y=current_y + 5)
        button = Button(self, text="送出此記錄", width=30, borderwidth=3)
        button.place(x=117, y=current_y)
        button["command"] = self.submitting
        button = Button(self, text="關閉視窗", width=10, borderwidth=3)
        button.place(x=348, y=current_y)
        button["command"] = self.destroy

    # noinspection PyUnusedLocal
    def _init_context(self, record):
        if isinstance(record, RecordOfDrawLots):
            self.record = record
            self.order.set(record.order)
            self.event_selector.set(record.event)
            self.character_selector.set(record.character)
            self.cost_selector.set(record.cost)
            self.date_time.set(record.date_time)
        else:
            raise TypeError('In RecordWindow, arg: \"record\"')

    # 合法的選擇情況下才繼續進行，否則彈出錯誤視窗
    def submitting(self):
        if self.event_selector.get() is None:
            tkMessageBox.showwarning("Event haven't selected", '\"Event\" 未選\n', parent=self)
        if self.character_selector.get() is None:
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n', parent=self)
        else:
            self.record.order = self.order.get()
            self.record.event = self.event_selector.get()
            self.record.character = self.character_selector.get()
            self.record.cost = self.cost_selector.get()
            self.record.date_time = self.date_time.get()

            self._post_submitting()

    # Template method
    def _post_submitting(self):
        pass


class AddingRecordWindow(RecordWindow):
    def __init__(self, master, record, events, callback, **kwargs):
        RecordWindow.__init__(self, master, record, events, callback, **kwargs)

    def _post_submitting(self):
        self.callback(self.record)
        self._init_context(RecordOfDrawLots.create_new_record_by_last_one(self.record, _get_current_date_time_str()))


class UpdatingRecordWindow(RecordWindow):
    def __init__(self, master, record, events, callback, **kwargs):
        RecordWindow.__init__(self, master, record, events, callback, **kwargs)

    def _post_submitting(self):
        self.callback()
        self.destroy()


# 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_new_record_window(master, events, callback):
    next_record = RecordOfDrawLots.create_new_record_by_last_one(
        DrawLotsModel.select_last_record(), _get_current_date_time_str())
    popup = AddingRecordWindow(master, next_record, events, lambda added_record: (
        DrawLotsModel.insert_record_into_db(added_record), callback(added_record)))
    master.wait_window(popup)


# 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_record_window(master, record, events, callback):
    popup = UpdatingRecordWindow(master, record, events, lambda: (
        DrawLotsModel.update_record_into_db(record), callback()))
    master.wait_window(popup)


def _get_current_date_time_str():
    return datetime.now().strftime('%m%d %H:%M')