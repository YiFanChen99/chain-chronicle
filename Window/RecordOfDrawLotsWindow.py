# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from BasicWindow import *
from CharacterWindow import CharacterInfoWindow
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *
from ModelUtility.Comparator import match_requested_rank
from ModelUtility.Filter import FilterManager
from UIUtility.Selector import ProfessionSelector, RankSelector


class RecordWindow(BasicWindow):
    def __init__(self, db_suffix, event_names):
        BasicWindow.__init__(self, width=518, height=156)
        self.window.geometry('+840+300')

        self.__init_widgets(event_names)

        self.filter_manager = FilterManager()
        self.record_table = 'RecordOfDrawLots' + db_suffix
        self.characters = None
        self.update_characters()

    # noinspection PyAttributeOutsideInit
    def __init_widgets(self, event_names):
        # 筆數
        current_y = 23
        Label(self.window, text=DRAW_LOTS_DB_TABLE[0], width=6, font=("", 12)).place(x=3, y=current_y)
        self.times = Variable()  # 下一次的筆數
        Label(self.window, textvariable=self.times, width=6, font=("", 12)).place(x=3, y=current_y + 27)

        # 酒廠
        Label(self.window, text=DRAW_LOTS_DB_TABLE[1], width=14, font=("", 12)).place(x=56, y=current_y)
        self.event_selector = ttk.Combobox(self.window, state='readonly', width=14, justify=CENTER)
        self.event_selector['values'] = event_names
        self.event_selector.place(x=63, y=current_y + 27)

        # 選擇職業、等級
        self.profession_selector = ProfessionSelector(self.window, self.updating_request_profession)
        self.profession_selector.place(x=197, y=7)
        self.rank_selector = RankSelector(self.window, self.updating_request_rank)
        self.rank_selector.place(x=197, y=55)

        # 角色
        current_x = 396
        Label(self.window, text=DRAW_LOTS_DB_TABLE[4], width=11, font=("", 12)).place(x=current_x, y=4)
        self.character_selector = ttk.Combobox(self.window, state='readonly', width=10, justify=CENTER)
        self.character_selector.place(x=current_x + 9, y=23)

        # 花費
        Label(self.window, text=DRAW_LOTS_DB_TABLE[5], width=9, font=("", 12)).place(x=current_x + 6, y=53)
        self.cost_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
        self.cost_selector['values'] = DRAW_LOTS_COST
        self.cost_selector.place(x=current_x + 14, y=72)

        # 送交、新增角色、取消並關閉的按鈕
        current_y = 116
        button = Button(self.window, text="送出此記錄", width=37, borderwidth=3)
        button.place(x=19, y=current_y)
        button["command"] = self.submitting
        button = Button(self.window, text="新增角色", width=11, borderwidth=3)
        button.place(x=307, y=current_y)
        button["command"] = self.adding_new_character
        button = Button(self.window, text="關閉視窗", width=11, borderwidth=3)
        button.place(x=410, y=current_y)
        button["command"] = self.destroy

    def adding_new_character(self):
        popup = CharacterInfoWindow()
        self.wait_window(popup)
        self.update_characters()
        self.updating_character_selector()

    def update_characters(self):
        self.characters = DBAccessor.execute('select Nickname, Profession, Rank from Character').fetchall()

    def updating_request_profession(self, profession):
        self.filter_manager.set_specific_condition(1, profession)
        self.updating_character_selector()

    def updating_request_rank(self, rank):
        self.filter_manager.set_specific_condition(2, rank, match_requested_rank)
        self.updating_character_selector()

    # noinspection PyUnusedLocal
    def updating_character_selector(self, event=None):
        self.character_selector.set('')
        character_matched = []
        for character_infos in self.filter_manager.filter(self.characters):
            character_matched.append(character_infos[0])
        self.character_selector['values'] = character_matched
        self.character_selector.focus_set()

    def submitting(self):
        if self.is_submitting_record_legal():
            self.do_submitting()

    # Template Method
    def do_submitting(self):
        pass

    def is_submitting_record_legal(self):
        error_message = ''
        if self.profession_selector.current_profession not in PROFESSIONS:
            error_message += '\"Profession\" 錯誤\n'
        if self.get_legal_rank() not in RANKS_WHEN_DRAW_LOTS:
            error_message += '\"Rank\" 錯誤\n'
        if self.character_selector.get() == '':
            error_message += '\"Character\" 未填\n'

        is_legal = (error_message == '')
        if not is_legal:
            tkMessageBox.showwarning("Can not submit this record", error_message)

        return is_legal

    def get_legal_rank(self):
        rank = self.rank_selector.current_rank
        if rank == '5':
            return 5
        elif rank == '4':
            return 4
        elif rank == '3':
            return 3
        else:
            return -1


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
        DBAccessor.execute('insert into {0}({1})'.format(self.record_table, ','.join(DRAW_LOTS_DB_TABLE)) +
                           convert_data_to_insert_command(
                               self.times.get(), self.event_selector.get(), self.profession_selector.current_profession,
                               self.get_legal_rank(), self.character_selector.get(), self.cost_selector.get()))
        DBAccessor.commit()

        # 更新顯示的資料
        self.last_record = [self.times.get(), self.event_selector.get(),
                            self.profession_selector.current_profession, self.get_legal_rank(),
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
        self.profession_selector.select(next(record))
        self.rank_selector.select(str(next(record)))
        self.character_selector.set(next(record))
        self.cost_selector.set(next(record))

    # 單純更新到資料庫，不寫回原 record (因tuple的關係)
    def do_submitting(self):
        new_data = [self.event_selector.get(), self.profession_selector.current_profession, self.get_legal_rank(),
                    self.character_selector.get(), self.cost_selector.get()]
        DBAccessor.execute('update ' + self.record_table + convert_data_to_update_command(
            DRAW_LOTS_DB_TABLE[1:6], new_data) + ' where Times=' + str(self.times.get()))
        DBAccessor.commit()

        self.destroy()