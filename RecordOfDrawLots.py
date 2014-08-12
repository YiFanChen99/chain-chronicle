# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import tkMessageBox
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import UpdateCharacterWindow
from datetime import timedelta

# RecordOfDrawLots 表格中的各欄位
COLUMNS = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']


class RecordOfDrawLots(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

        self.__init_add_record_frame()
        self.__init_filter_frame()

        # 呈現資料的表格
        self.table_model = None
        self.__init_table()

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
        button["command"] = self.do_add_record

    # TODO event cost pro
    # noinspection PyAttributeOutsideInit
    def __init_filter_frame(self):
        basic_x = 18
        Label(self, text='E:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.event = ttk.Combobox(self, state='readonly', width=14, justify=CENTER)
        self.event['values'] = PROFESSIONS
        self.event.place(x=basic_x+18, y=5)

        basic_x = 165
        Label(self, text='C:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.cost = ttk.Combobox(self, state='readonly', width=7, justify=CENTER)
        self.cost['values'] = PROFESSIONS
        self.cost.place(x=basic_x+20, y=5)

        basic_x = 265
        Label(self, text='P:', font=(MS_JH, 12)).place(x=basic_x, y=5)
        self.profession = ttk.Combobox(self, state='readonly', width=5, justify=CENTER)
        self.profession['values'] = PROFESSIONS
        self.profession.place(x=basic_x+20, y=5)

        basic_x = 367
        Label(self, text='Total:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.total = Label(self, font=(MS_JH, 12))
        self.total.place(x=basic_x+44, y=3)
        self.total["text"] = '900'

        basic_x = 452
        Label(self, text='SSR:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.ssr = Label(self, font=(MS_JH, 12))
        self.ssr.place(x=basic_x+34, y=3)
        self.ssr["text"] = '90'

        basic_x = 523
        Label(self, text='SR:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.sr = Label(self, font=(MS_JH, 12))
        self.sr.place(x=basic_x+25, y=3)
        self.sr["text"] = '90'

        basic_x = 584
        Label(self, text='R:', font=(MS_JH, 12)).place(x=basic_x, y=3)
        self.r = Label(self, font=(MS_JH, 12))
        self.r.place(x=basic_x + 16, y=3)
        self.r["text"] = '90'

        # 根據條件進行篩選的按鈕
        button = Button(self, text="進行篩選", width=8, font=(MS_JH, 12))
        button.place(x=640, y=0)
        #button["command"] = self.do_add_record  TODO

    def do_add_record(self):
        popup = AddRecordWindow(self, not self.is_show_old_events.get())
        self.wait_window(popup)
        self.update_table()

    # noinspection PyAttributeOutsideInit
    def __init_table(self):
        self.table = Frame(self)
        self.table.place(x=35, y=30)
        self.table_view = TableCanvas(self.table, rowheaderwidth=0, cellwidth=90, editable=False)
        # noinspection PyPep8Naming
        self.table_view.deleteCells = do_nothing  # 按下 Delete 鍵時不做反應(預設會詢問刪除該記錄)

        self.update_table()

    def update_table(self):
        self.table_model = TableModel()

        for column in COLUMNS:
            self.table_model.addColumn(column)

        result = DATABASE.execute('select * from ' + get_name_of_record_table())
        for row in result:
            self.table_model.addRow(Times=row[0], Event=convert_to_str(row[1]),
                                    Profession=convert_to_str(row[2]), Rank=row[3],
                                    Character=convert_to_str(row[4]),
                                    Cost=convert_to_str(row[5]))

        self.table_model.setSortOrder(columnName=COLUMNS[0], reverse=1)

        self.table_view.setModel(self.table_model)
        self.table_view.createTableFrame()
        self.table_view.redrawTable()
        self.table_view.adjustColumnWidths()

    def adjust_view(self, width, height):
        self.table_view['width'] = width - 59
        self.table_view['height'] = height - 74


class AddRecordWindow(Frame):
    def __init__(self, master, is_time_limited):
        Frame.__init__(self, master)
        self.window = Toplevel(width=565, height=118)
        self.window.title('Add new record')
        self.is_time_limited = is_time_limited

        self.__init_widgets()

        # 取得最近一筆資料，以作為預設值
        command = 'select * from ' + get_name_of_record_table() + \
                  ' where Times = (select max(Times) from ' + get_name_of_record_table() + ')'
        self.last_record = DATABASE.execute(command).fetchone()

        self.update_by_last_record()

    # noinspection PyAttributeOutsideInit
    def __init_widgets(self):
        # 各 Column 的標題: 筆數, 酒廠, 職業, 等級, 角色, 花費
        Label(self.window, text=COLUMNS[0], width=6, font=("", 12)).place(x=3, y=9)
        Label(self.window, text=COLUMNS[1], width=14, font=("", 12)).place(x=56, y=9)
        Label(self.window, text=COLUMNS[2], width=7, font=("", 12)).place(x=200, y=9)
        Label(self.window, text=COLUMNS[3], width=5, font=("", 12)).place(x=286, y=9)
        Label(self.window, text=COLUMNS[4], width=11, font=("", 12)).place(x=349, y=9)
        Label(self.window, text=COLUMNS[5], width=9, font=("", 12)).place(x=453, y=9)

        # 下一次的筆數
        self.times = Variable()
        Label(self.window, textvariable=self.times, width=6, font=("", 12)).place(x=3, y=40)

        # 選擇酒廠
        self.event_selector = ttk.Combobox(self.window, state='readonly', width=14, justify=CENTER)
        self.event_selector['values'] = get_suitable_event_names(self.is_time_limited)
        self.event_selector.place(x=63, y=40)

        # 選擇職業
        self.profession_selector = ttk.Combobox(self.window, state='readonly', width=7, justify=CENTER)
        self.profession_selector['values'] = PROFESSIONS
        self.profession_selector.place(x=199, y=40)
        self.profession_selector.bind('<<ComboboxSelected>>', self.update_character_selector)

        # 選擇等級
        self.rank_selector = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.rank_selector['values'] = RANKS_WHEN_DRAW_LOTS
        self.rank_selector.place(x=285, y=40)
        self.rank_selector.bind('<<ComboboxSelected>>', self.update_character_selector)

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
        button["command"] = self.do_submit

        # 新增角色的按鈕
        button = Button(self.window, text="新增角色", width=12, borderwidth=3)
        button.place(x=326, y=79)
        button["command"] = self.do_add_character

        # 取消並關閉的按鈕
        button = Button(self.window, text="關閉視窗", width=12, borderwidth=3)
        button.place(x=438, y=79)
        button["command"] = self.do_close_window

    def update_by_last_record(self):
        self.times.set(self.last_record[0] + 1)
        self.event_selector.set(self.last_record[1])
        self.update_character_selector()
        self.cost_selector.set(self.last_record[5])

    def do_submit(self):
        if self.is_new_record_legal():
            DATABASE.execute('insert into ' + get_name_of_record_table() +
                             '(' + ','.join(COLUMNS) + ')' +
                             convert_data_to_insert_command(self.times.get(), self.event_selector.get(),
                                                            self.profession_selector.get(), self.rank_selector.get(),
                                                            self.character_selector.get(), self.cost_selector.get()))
            DATABASE.commit()

            # 更新顯示的資料
            self.last_record = [self.times.get(), self.event_selector.get(),
                                self.profession_selector.get(), self.rank_selector.get(),
                                self.character_selector.get(), self.cost_selector.get()]
            self.update_by_last_record()
            self.master.update_table()

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
    def update_character_selector(self, event=None):
        # 取得所有的角色
        results = DATABASE.execute('select Character, Rank, Profession from Character').fetchall()

        # 依序對職業與等級進行篩選(if需要)
        profession = self.profession_selector.get()
        if profession != '':
            results = [element for element in results if element[2] == profession]
        rank = self.rank_selector.get()
        if rank != '':
            results = [element for element in results if element[1] == int(rank)]

        characters = []
        [characters.append(element[0]) for element in results]
        self.character_selector['values'] = characters
        self.character_selector.set('')

    def do_add_character(self):
        popup = UpdateCharacterWindow.UpdateCharacterWindow(self)
        self.wait_window(popup)
        self.update_character_selector()

    def do_close_window(self):
        self.window.destroy()
        self.destroy()


def get_name_of_record_table():
    return 'RecordOfDrawLots' + get_suffix_of_account()


def get_name_of_event_table():
    return 'EventOfDrawLots' + get_suffix_of_account()


# 若有要求只顯示恰當的酒廠，則會計算結束日期滿足條件才會加入
def get_suitable_event_names(is_time_limited):
    names = []
    available_time = datetime.now() - timedelta(days=3)
    events = DATABASE.execute('select Name, End from ' + get_name_of_event_table()).fetchall()

    for each_event in events:
        if is_time_limited and convert_str_to_datetime(each_event[1]) < available_time:
            pass
        else:
            names.append(each_event[0])
    return names