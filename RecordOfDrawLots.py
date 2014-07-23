# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import tkMessageBox
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

# RecordOfDrawLots 表格中的各欄位
COLUMNS = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']


class RecordOfDrawLots(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

        # 新增記錄的按鈕
        button = Button(self, text="新增記錄", width=2, height=21, wraplength=1, font=14)
        button.place(x=5, y=5)
        button["command"] = self.do_add_record

        # 呈現資料的表格
        self.update_table()

    def do_add_record(self):
        popup = AddRecordWindow(self)
        self.wait_window(popup)

    # noinspection PyAttributeOutsideInit
    def update_table(self):
        self.table = Frame(self)
        self.table.place(x=35, y=7)
        self.table_model = TableModel()
        self.table_view = TableCanvas(self.table, model=self.table_model, width=633,
                                      height=316, rowheaderwidth=0, cellwidth=90, editable=False)
        self.table_view.createTableFrame()

        for column in COLUMNS:
            self.table_model.addColumn(column)

        result = DATABASE.execute('select * from RecordOfDrawLots')
        for row in result:
            self.table_model.addRow(Times=row[0], Event=convert_to_str(row[1]),
                                    Profession=convert_to_str(row[2]), Rank=row[3],
                                    Character=convert_to_str(row[4]),
                                    Cost=convert_to_str(row[5]))

        self.table_model.setSortOrder(columnName=COLUMNS[0], reverse=1)
        self.table_view.adjustColumnWidths()
        self.table_view.redrawTable()


class AddRecordWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.window = Toplevel(width=565, height=115)
        self.window.title('Add new record')

        # 各 Column 的標題
        x = 3
        x_shifted = 90
        for column in COLUMNS:
            label = Label(self.window, text=column, width=9, font=14)
            label.place(x=x, y=9)
            x += x_shifted

        # 初始化，填入預設的記錄
        self.__init_record()

        # 送交的按鈕
        button = Button(self.window, text="Finish", command=self.do_submit, width=70, borderwidth=3)
        button.place(x=30, y=79)

    # noinspection PyAttributeOutsideInit
    def __init_record(self):
        # 取得最近一筆資料，以作為預設值
        command = 'select * from RecordOfDrawLots' + \
                  ' where Times = (select max(Times) from RecordOfDrawLots)'
        last_record = DATABASE.execute(command).fetchone()

        # 下一次的筆數
        self.times = last_record[0] + 1
        Label(self.window, text=self.times, width=8, font=14).place(x=5, y=40)

        # 選擇酒廠
        self.event_selector = ttk.Combobox(self.window, state='readonly', width=9, justify=CENTER)
        events = []
        [events.append(element[0]) for element in DATABASE.execute('select Name from EventOfDrawLots').fetchall()]
        self.event_selector['values'] = events
        self.event_selector.place(x=95, y=40)
        self.event_selector.set(last_record[1])  # 設定初始選項

        # 選擇職業
        self.profession_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
        self.profession_selector['values'] = PROFESSIONS
        self.profession_selector.place(x=189, y=40)
        self.profession_selector.bind('<<ComboboxSelected>>', self.update_character_selector)

        # 選擇等級
        self.rank_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
        self.rank_selector['values'] = RANKS_WHEN_DRAW_LOTS
        self.rank_selector.place(x=280, y=40)
        self.rank_selector.bind('<<ComboboxSelected>>', self.update_character_selector)

        # 選擇角色
        self.character_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
        self.update_character_selector()
        self.character_selector.place(x=368, y=40)

        # 選擇花費
        self.cost_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
        self.cost_selector['values'] = DRAW_LOTS_COST
        self.cost_selector.place(x=463, y=40)
        self.cost_selector.set(last_record[5])  # 設定初始選項

    def do_submit(self):
        if self.is_new_record_legal():
            DATABASE.execute('insert into RecordOfDrawLots(' + ','.join(COLUMNS) + ')' +
                             data_to_insert_command(self.times, self.event_selector.get(),
                                                    self.profession_selector.get(), self.rank_selector.get(),
                                                    self.character_selector.get(), self.cost_selector.get()))
            DATABASE.commit()
            destroy_frame(self.window)

            if self.master.table is not None:
                destroy_frame(self.master.table)
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
        # set condition
        profession = self.profession_selector.get()
        rank = self.rank_selector.get()
        condition = ''
        if profession == '' and rank == '':
            pass
        elif profession == '':
            condition = ' where Rank=' + datum_to_command_by_type(rank)
        elif rank == '':
            condition = ' where Profession=' + datum_to_command_by_type(profession)
        else:
            condition = ' where Profession=' + datum_to_command_by_type(profession) + \
                        'and Rank=' + datum_to_command_by_type(rank)

        result = DATABASE.execute('select Character from Character' + condition).fetchall()
        characters = []
        [characters.append(element[0]) for element in result]
        self.character_selector['values'] = characters
        self.character_selector.set('')