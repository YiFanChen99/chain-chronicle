# -*- coding: utf-8 -*-
from UI.Utility.BasicWindow import *
from ModelUtility.CommonValue import *
from ModelUtility.DataObject import EventOfDrawLots
from Model import DrawLotsModel

TYPES = [u'一般', u'強化', u'特殊']


class EventWindow(BasicWindow):
    def __init__(self, master, event, callback, width=358, height=226, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)

        self.callback = callback
        self._init_widgets()
        self._init_context(event)

    def _init_widgets(self):
        current_y = 16
        Label(self, width=4, text='Name', font=(SCP, 12)).place(x=18, y=current_y)
        self.name = StringVar()
        name_entry = Entry(self, width=22, textvariable=self.name, font=(MS_JH, 12))
        name_entry.place(x=76, y=current_y + 2)
        name_entry.bind('<Return>', lambda event: started_day_entry.focus_set())

        current_y += 39
        Label(self, width=7, text='Duration', font=(SCP, 10)).place(x=20, y=current_y)
        self.started_day = StringVar()
        started_day_entry = Entry(self, width=10, textvariable=self.started_day, font=(MS_JH, 9))
        started_day_entry.place(x=96, y=current_y + 2)
        started_day_entry.bind('<Return>', lambda event: end_day_entry.focus_set())
        self.end_day = StringVar()
        end_day_entry = Entry(self, width=10, textvariable=self.end_day, font=(MS_JH, 9))
        end_day_entry.place(x=180, y=current_y + 2)
        end_day_entry.bind('<Return>', lambda event: self.description_text.focus_set())

        current_y += 31
        Label(self, width=4, text='Desc.', font=(SCP, 11)).place(x=17, y=current_y + 5)
        self.description_text = Text(self, width=29, height=2, font=(MS_JH, 11))
        self.description_text.place(x=71, y=current_y)
        self.description_text.bind('<Return>', lambda event: self.type.focus_set())

        current_y += 50
        Label(self, width=4, text='Type', font=(SCP, 10)).place(x=10, y=current_y - 2)
        self.type = ttk.Combobox(self, width=4, state='readonly', font=(MS_JH, 9), justify=CENTER)
        self.type['value'] = TYPES
        self.type.set(TYPES[2])
        self.type.place(x=50, y=current_y - 1)
        self.type.bind('<Return>', lambda event: ssr_entry.focus_set())
        Label(self, width=4, text='SSR', font=(SCP, 11)).place(x=107, y=current_y)
        self.ssr_rate = DoubleVar()
        ssr_entry = Entry(self, width=4, textvariable=self.ssr_rate, font=(SCP, 11))
        ssr_entry.place(x=146, y=current_y + 1)
        ssr_entry.bind('<Return>', lambda event: sr_entry.focus_set())
        Label(self, width=2, text='SR', font=(SCP, 11)).place(x=190, y=current_y)
        self.sr_rate = DoubleVar()
        sr_entry = Entry(self, width=5, textvariable=self.sr_rate, font=(SCP, 11))
        sr_entry.place(x=216, y=current_y + 1)
        sr_entry.bind('<Return>', lambda event: r_entry.focus_set())
        Label(self, width=1, text='R', font=(SCP, 11)).place(x=270, y=current_y)
        self.r_rate = DoubleVar()
        r_entry = Entry(self, width=5, textvariable=self.r_rate, font=(SCP, 11))
        r_entry.place(x=287, y=current_y + 1)
        r_entry.bind('<Return>', lambda event: self.submitting())

        # 送交、取消並關閉的按鈕
        current_y += 47
        button = Button(self, text="送出", width=25, borderwidth=3)
        button.place(x=25, y=current_y)
        button["command"] = self.submitting
        button = Button(self, text="關閉視窗", width=13, borderwidth=3)
        button.place(x=229, y=current_y)
        button["command"] = self.destroy

    def _init_context(self, event):
        if isinstance(event, EventOfDrawLots):
            self.event = event
            self.name.set(event.name)
            self.started_day.set(event.started_day)
            self.end_day.set(event.end_day)
            self.type.set(event.type)
            self.description_text.insert('1.0', event.description)
            self.ssr_rate.set(event.ssr_rate)
            self.sr_rate.set(event.sr_rate)
            self.r_rate.set(event.r_rate)
        else:
            raise TypeError('In EventWindow, arg: \"event\"')

    # 合法的選擇情況下才繼續進行，否則彈出錯誤視窗
    def submitting(self):
        if self.name.get() is '':
            tkMessageBox.showwarning("Event name is empty.", 'Event name 為空\n', parent=self)
        else:
            self.event.name = self.name.get()
            self.event.started_day = self.started_day.get()
            self.event.end_day = self.end_day.get()
            self.event.type = self.type.get()
            self.event.description = self.description_text.get('1.0', '2.0-1c')
            self.event.ssr_rate = self.ssr_rate.get()
            self.event.sr_rate = self.sr_rate.get()
            self.event.r_rate = self.r_rate.get()
        self.callback()
        self.destroy()


# 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_event_window(master, callback):
    event = EventOfDrawLots.create_empty_event()
    popup = EventWindow(master, event, lambda: (
        DrawLotsModel.insert_event_into_db(event), callback(event)))
    master.wait_window(popup)


# 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_event_window(master, event, callback):
    popup = EventWindow(master, event, lambda: (
        DrawLotsModel.update_event_into_db(event), callback()))
    master.wait_window(popup)
