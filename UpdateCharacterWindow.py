# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *

DEFAULT_CHARACTER_ID = '請輸入名稱'


# TODO 修改並抽出
class UpdateCharacterWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.window = Toplevel(width=565, height=115)
        self.window.title('About character')

        label_space = 27  # Label 與 輸入元件的距離

        current_y = 3
        Label(self.window, width=12, text='角色').place(x=3, y=current_y)
        self.id = StringVar(value=DEFAULT_CHARACTER_ID)
        Entry(self.window, width=12, textvariable=self.id).place(x=3, y=current_y+label_space)

        Label(self.window, width=15, text='全名').place(x=103, y=current_y)
        self.full_name = StringVar(value=DEFAULT_CHARACTER_ID)
        Entry(self.window, width=15, textvariable=self.full_name).place(x=103, y=current_y+label_space)

        # Label(self.window, text='職業').grid(row=2, column=1)
        # self.profession = StringVar(value=DEFAULT_CHARACTER_ID)
        # Entry(self.window, textvariable=self.profession).grid(row=3, column=1)
        #
        # Label(self.window, text='等級').grid(row=2, column=3)
        # self.rank = StringVar(value=DEFAULT_CHARACTER_ID)
        # Entry(self.window, textvariable=self.rank).grid(row=3, column=3)

        Button(self.window, text="Submit", command=self.do_submit, width=15, borderwidth=3).place(x=30, y=80)
        Button(self.window, text="Cancel", command=self.do_cancel, width=15, borderwidth=3).place(x=180, y=80)

    # TODO 更新
    def do_submit(self):
        print 'submit'
        self.window.destroy()

    def do_cancel(self):
        self.window.destroy()

    # # noinspection PyAttributeOutsideInit
    # def __init_record(self, master):
    #     # 取得最近一筆資料，以作為預設值
    #     command = 'select * from RecordOfDrawLots' + \
    #               ' where Times = (select max(Times) from RecordOfDrawLots)'
    #     last_record = master.execute(command).fetchone()
    #
    #     # 下一次的筆數
    #     self.times = last_record[0] + 1
    #     Label(self.window, text=self.times, width=8, font=14).place(x=5, y=40)
    #
    #     # 選擇酒廠
    #     self.event_selector = ttk.Combobox(self.window, state='readonly', width=9, justify=CENTER)
    #     events = []
    #     [events.append(element[0]) for element in master.execute('select Name from EventOfDrawLots').fetchall()]
    #     self.event_selector['values'] = events
    #     self.event_selector.place(x=95, y=40)
    #     self.event_selector.set(last_record[1])  # 設定初始選項
    #
    #     # 選擇職業
    #     self.profession_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
    #     self.profession_selector['values'] = Static.PROFESSIONS
    #     self.profession_selector.place(x=189, y=40)
    #     self.profession_selector.bind('<<ComboboxSelected>>', self.update_character_selector)
    #
    #     # 選擇等級
    #     self.rank_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
    #     self.rank_selector['values'] = Static.RANKS_WHEN_DRAW_LOTS
    #     self.rank_selector.place(x=280, y=40)
    #     self.rank_selector.bind('<<ComboboxSelected>>', self.update_character_selector)
    #
    #     # 選擇角色
    #     self.character_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
    #     self.update_character_selector()
    #     self.character_selector.place(x=368, y=40)
    #
    #     # 選擇花費
    #     self.cost_selector = ttk.Combobox(self.window, state='readonly', width=8, justify=CENTER)
    #     self.cost_selector['values'] = Static.DRAW_LOTS_COST
    #     self.cost_selector.place(x=463, y=40)
    #     self.cost_selector.set(last_record[5])  # 設定初始選項
    #
    # def do_submit(self):
    #     if self.is_new_record_legal():
    #         self.master.execute('insert into RecordOfDrawLots(Times, Event, Profession, Rank, Character, Cost) values '
    #                             + self.convert_data_to_sub_command())
    #         self.master.commit()
    #         BaseTab.destroy_frame(self.window)
    #
    #         if self.master.table is not None:
    #             BaseTab.destroy_frame(self.master.table)
    #         self.master.update_table()
    #
    # def is_new_record_legal(self):
    #     error_message = ''
    #     if self.profession_selector.get() == '':
    #         error_message += '\"Profession\" 未填\n'
    #     if self.rank_selector.get() == '':
    #         error_message += '\"Rank\" 未填\n'
    #     if self.character_selector.get() == '':
    #         error_message += '\"Character\" 未填\n'
    #
    #     is_legal = (error_message == '')
    #     if not is_legal:
    #         tkMessageBox.showwarning("Can not add this record", error_message)
    #
    #     return is_legal
    #
    # def convert_data_to_sub_command(self):
    #     command = '('
    #     command += str(self.times) + ', '
    #     command += '\"' + self.event_selector.get() + '\", '
    #     command += '\"' + self.profession_selector.get() + '\", '
    #     command += str(self.rank_selector.get()) + ', '
    #     command += '\"' + self.character_selector.get() + '\", '
    #     command += '\"' + self.cost_selector.get() + '\")'
    #     return command
    #
    # # noinspection PyUnusedLocal
    # def update_character_selector(self, event=None):
    #     # set condition
    #     profession = self.profession_selector.get()
    #     rank = self.rank_selector.get()
    #     condition = ''
    #     if profession == '' and rank == '':
    #         pass
    #     elif profession == '':
    #         condition = ' where Rank=\"' + str(rank) + '\"'
    #     elif rank == '':
    #         condition = ' where Profession=\"' + profession + '\"'
    #     else:
    #         condition = ' where Profession = \"' + profession + '\" and Rank = \"' + str(rank) + '\"'
    #
    #     result = self.master.execute('select Character from RecordOfDrawLots' + condition).fetchall()
    #     characters = []
    #     [characters.append(element[0]) for element in result]
    #     self.character_selector['values'] = characters
    #     self.character_selector.set('')

if __name__ == "__main__":
    root = Tk()
    root.geometry("728x420+540+360")
    app = UpdateCharacterWindow(master=root)
    app.mainloop()
