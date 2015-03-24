# -*- coding: utf-8 -*-
from datetime import datetime
from UI.Utility.BasicMainFrame import *
from ModelUtility import APTimeCalculator


class EventFrame(MainFrame):
    def __init__(self, master, **kwargs):
        MainFrame.__init__(self, master, **kwargs)

        apc = APLeft(self)
        apc.place(x=5, y=5)


class APLeft(Canvas):
    def __init__(self, master, **kwargs):
        Canvas.__init__(self, master, **kwargs)

        self.end_time = datetime(2015, 03, 05, 8, 59)

        button = Button(self, text='計算', width=8, font=(MS_JH, 10))
        button.place(x=1, y=1)
        button["command"] = lambda: self.calculate_ap_left()

        current_y = 32
        self.current_time_desc = StringVar()
        self.end_time_desc = StringVar()
        self.end_time_desc.set('End: ' + self.get_datetime_str(self.end_time))
        self.ap_left_desc = StringVar()
        Label(self, textvariable=self.current_time_desc, width=16, font=(SCP, 11)).place(x=16, y=current_y)
        Label(self, textvariable=self.end_time_desc, width=16, font=(SCP, 11)).place(x=16, y=current_y + 20)
        Label(self, textvariable=self.ap_left_desc, width=16, font=(SCP, 11)).place(x=16, y=current_y + 40)

        self.calculate_ap_left()

    def calculate_ap_left(self):
        current = datetime.now()
        self.current_time_desc.set('At : ' + self.get_datetime_str(current))
        self.ap_left_desc.set('AP Left: %3d' % (APTimeCalculator.convert_timedelta_to_ap(self.end_time - current)))

    @staticmethod
    def get_datetime_str(the_datetime):
        return '%02d/%02d %02d:%02d' % (the_datetime.month, the_datetime.day, the_datetime.hour, the_datetime.minute)
