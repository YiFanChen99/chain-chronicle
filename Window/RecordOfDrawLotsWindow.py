# -*- coding: utf-8 -*-
from BasicWindow import *
from UIUtility.CharacterSelector import CharacterSelectorCanvas
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *
from ModelUtility.CommonState import *


class RecordWindow(BasicWindow):
    def __init__(self, master, event_names, width=445, height=131, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.geometry('+850+300')

        self._init_widgets(event_names)

        self.table_name = 'RecordOfDrawLots' + get_db_suffix()

    def _init_widgets(self, event_names):
        # 筆數
        current_y = 15
        Label(self, text=DRAW_LOTS_DB_TABLE[0], width=6, font=("", 12)).place(x=4, y=current_y)
        self.times = Variable()  # 下一次的筆數
        Label(self, textvariable=self.times, width=6, font=("", 12)).place(x=4, y=current_y + 27)

        # 酒廠
        Label(self, text=DRAW_LOTS_DB_TABLE[1], width=14, font=("", 12)).place(x=57, y=current_y)
        self.event_selector = ttk.Combobox(self, state='readonly', width=14, justify=CENTER)
        self.event_selector['values'] = event_names
        self.event_selector.place(x=64, y=current_y + 27)

        # 角色
        self.character_selector = CharacterSelectorCanvas(self)
        self.character_selector.place(x=201, y=current_y - 4)

        # 花費
        Label(self, text=DRAW_LOTS_DB_TABLE[5], width=9, font=("", 12)).place(x=338, y=current_y)
        self.cost_selector = ttk.Combobox(self, state='readonly', width=8, justify=CENTER)
        self.cost_selector['values'] = DRAW_LOTS_COST
        self.cost_selector.place(x=346, y=current_y + 27)

        # 送交、新增角色、取消並關閉的按鈕
        current_y = 90
        button = Button(self, text="送出此記錄", width=39, borderwidth=3)
        button.place(x=23, y=current_y)
        button["command"] = self.submitting
        button = Button(self, text="關閉視窗", width=11, borderwidth=3)
        button.place(x=330, y=current_y)
        button["command"] = self.destroy

    # 有選擇的情況下才繼續進行，否則彈出錯誤視窗
    def submitting(self):
        if self.character_selector.get() is None:
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n', parent=self)
        else:
            self.do_submitting()

    # Template Method
    def do_submitting(self):
        pass


class AddRecordWindow(RecordWindow):
    def __init__(self, master, event_names, callback, **kwargs):
        RecordWindow.__init__(self, master, event_names, **kwargs)
        self.title('Add new record')

        self.callback = callback

        # 以最近一筆資料作為預設值，設定內容
        last_record = DBAccessor.execute(
            'select * from {0} where Times = (select max(Times) from {0})'.format(self.table_name)).fetchone()
        self.times.set(last_record[0] + 1)
        self.event_selector.set(last_record[1])
        self.cost_selector.set(last_record[5])

    def do_submitting(self):
        character = self.character_selector.get()
        DBAccessor.execute('insert into {0}({1})'.format(self.table_name, ','.join(DRAW_LOTS_DB_TABLE)) +
                           convert_data_to_insert_command(
                               self.times.get(), self.event_selector.get(), character.profession,
                               character.rank, character.nickname, self.cost_selector.get()))
        DBAccessor.commit()

        # 更新顯示的資料
        self.times.set(self.times.get() + 1)

        self.callback()


class UpdatingRecordWindow(RecordWindow):
    def __init__(self, master, event_names, record, **kwargs):
        RecordWindow.__init__(self, master, event_names, **kwargs)
        self.title('Update record')

        self._init_context(record)

    # noinspection PyUnusedLocal
    def _init_context(self, record):
        record = iter(record)
        self.times.set(next(record))
        self.event_selector.set(next(record))
        dropped = next(record)
        dropped = next(record)
        self.character_selector.set(DBAccessor.select_character_by_specific_column('Nickname', next(record)))
        self.cost_selector.set(next(record))

    # 單純更新到資料庫，不寫回原 record (因tuple的關係)
    def do_submitting(self):
        character = self.character_selector.get()
        DBAccessor.execute('update {0}{1} where Times={2}'.format(self.table_name, convert_data_to_update_command(
            DRAW_LOTS_DB_TABLE[1:6], [self.event_selector.get(), character.profession, character.rank,
                                      character.nickname, self.cost_selector.get()]), self.times.get()))
        DBAccessor.commit()

        self.destroy()