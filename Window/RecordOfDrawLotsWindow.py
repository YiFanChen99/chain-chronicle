# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from BasicWindow import *
from CharacterWindow import CharacterInfoWindow
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *


class RecordWindow(BasicWindow):
    def __init__(self, db_suffix, event_names):
        BasicWindow.__init__(self, width=565, height=118)

        self.__init_widgets(event_names)

        self.record_table = 'RecordOfDrawLots' + db_suffix
        self.characters = None
        self.update_characters()

    # noinspection PyAttributeOutsideInit
    def __init_widgets(self, event_names):
        # 各 Column 的標題: 筆數, 酒廠, 職業, 等級, 角色, 花費
        Label(self.window, text=DRAW_LOTS_DB_TABLE[0], width=6, font=("", 12)).place(x=3, y=9)
        Label(self.window, text=DRAW_LOTS_DB_TABLE[1], width=14, font=("", 12)).place(x=56, y=9)
        Label(self.window, text=DRAW_LOTS_DB_TABLE[2], width=7, font=("", 12)).place(x=200, y=9)
        Label(self.window, text=DRAW_LOTS_DB_TABLE[3], width=5, font=("", 12)).place(x=286, y=9)
        Label(self.window, text=DRAW_LOTS_DB_TABLE[4], width=11, font=("", 12)).place(x=349, y=9)
        Label(self.window, text=DRAW_LOTS_DB_TABLE[5], width=9, font=("", 12)).place(x=453, y=9)

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
        button = Button(self.window, text="送出此記錄", width=38, borderwidth=3)
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

    def adding_new_character(self):
        popup = CharacterInfoWindow()
        self.wait_window(popup)
        self.update_characters()
        self.updating_character_selector()

    def update_characters(self):
        self.characters = DBAccessor.execute('select Nickname, Profession, Rank from Character').fetchall()

    def closing_window(self):
        self.destroy()

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

    def submitting(self):
        if self.is_new_record_legal():
            self.do_submitting()

    # Template Method
    def do_submitting(self):
        pass

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


class AddRecordWindow(RecordWindow):
    def __init__(self, db_suffix, event_names, callback):
        RecordWindow.__init__(self, db_suffix, event_names)
        self.window.title('Add new record')

        self.callback = callback

        # 取得最近一筆資料，以作為預設值
        command = 'select * from ' + self.record_table + \
                  ' where Times = (select max(Times) from ' + self.record_table + ')'
        self.last_record = DBAccessor.execute(command).fetchone()
        self.reset_context()

    def do_submitting(self):
        DBAccessor.execute('insert into ' + self.record_table +
                           '(' + ','.join(DRAW_LOTS_DB_TABLE) + ')' +
                           convert_data_to_insert_command(self.times.get(), self.event_selector.get(),
                                                          self.profession_selector.get(), self.rank_selector.get(),
                                                          self.character_selector.get(), self.cost_selector.get()))
        DBAccessor.commit()

        # 更新顯示的資料
        self.last_record = [self.times.get(), self.event_selector.get(),
                            self.profession_selector.get(), self.rank_selector.get(),
                            self.character_selector.get(), self.cost_selector.get()]
        self.reset_context()
        self.callback()

    def reset_context(self):
        self.times.set(self.last_record[0] + 1)
        self.event_selector.set(self.last_record[1])
        self.updating_character_selector()
        self.cost_selector.set(self.last_record[5])


class UpdatingRecordWindow(RecordWindow):
    def __init__(self, db_suffix, event_names, record):
        RecordWindow.__init__(self, db_suffix, event_names)
        self.window.title('Update record')

        self.__init_context(record)

    def __init_context(self, record):
        record = iter(record)
        self.times.set(next(record))
        self.event_selector.set(next(record))
        self.profession_selector.set(next(record))
        self.rank_selector.set(next(record))
        self.character_selector.set(next(record))
        self.cost_selector.set(next(record))

    # 單純更新到資料庫，不必寫回原 record (因tuple的關係)
    def do_submitting(self):
        new_data = [self.event_selector.get(), self.profession_selector.get(), self.rank_selector.get(),
                    self.character_selector.get(), self.cost_selector.get()]
        DBAccessor.execute('update ' + self.record_table + convert_data_to_update_command(
            DRAW_LOTS_DB_TABLE[1:6], new_data) + ' where Times=' + str(self.times.get()))
        DBAccessor.commit()

        self.destroy()