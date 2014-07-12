# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
import Static
import ttk
import tkMessageBox


class UpdateCharacterWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.window = Toplevel(width=564, height=255)
        self.window.title('About character')

        label_space = 22  # Label 與 輸入元件的距離

        # 第一個 Row
        current_y = 3
        Label(self.window, width=12, text='角色').place(x=10, y=current_y)
        self.id = StringVar(value='')
        Entry(self.window, width=12, textvariable=self.id).place(x=10, y=current_y + label_space)

        Label(self.window, width=15, text='全名').place(x=105, y=current_y)
        self.full_name = StringVar(value='')
        Entry(self.window, width=15, textvariable=self.full_name).place(x=105, y=current_y + label_space)

        Label(self.window, width=4, text='等級').place(x=220, y=current_y)
        self.rank = ttk.Combobox(self.window, state='readonly', width=3, justify=CENTER)
        self.rank['values'] = Static.RANKS
        self.rank.place(x=220, y=current_y + label_space - 2)

        Label(self.window, width=5, text='Cost').place(x=270, y=current_y)
        self.attendance_cost = StringVar(value='')
        Entry(self.window, width=5, textvariable=self.attendance_cost).place(x=272, y=current_y + label_space)

        Label(self.window, width=6, text='職業').place(x=318, y=current_y)
        self.profession = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.profession['values'] = Static.PROFESSIONS
        self.profession.place(x=317, y=current_y + label_space - 2)

        Label(self.window, width=6, text='武器種類').place(x=386, y=current_y)
        self.weapon_type = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.weapon_type['values'] = Static.WEAPONS
        self.weapon_type.place(x=384, y=current_y + label_space - 2)

        Label(self.window, width=6, text='成長類型').place(x=452, y=current_y)
        self.exp_grown = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.exp_grown['values'] = Static.EXP_GROWN
        self.exp_grown.place(x=452, y=current_y + label_space - 2)

        # 第二個 Row
        current_y = 52
        Label(self.window, width=6, text='滿級Atk').place(x=9, y=current_y)
        self.max_atk = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.max_atk).place(x=10, y=current_y + label_space)

        Label(self.window, width=6, text='滿級HP').place(x=60, y=current_y)
        self.max_hp = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.max_hp).place(x=61, y=current_y + label_space)

        Label(self.window, width=6, text='突滿Atk').place(x=111, y=current_y)
        self.max_atk_after_break = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.max_atk_after_break).place(x=112, y=current_y + label_space)

        Label(self.window, width=6, text='突滿HP').place(x=162, y=current_y)
        self.max_hp_after_break = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.max_hp_after_break).place(x=163, y=current_y + label_space)

        Button(self.window, text="轉換", command=self.do_transform_grown, width=4, borderwidth=3) \
            .place(x=215, y=current_y + label_space - 14)

        Label(self.window, width=6, text='Atk成長').place(x=262, y=current_y)
        self.atk_grown = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.atk_grown).place(x=262, y=current_y + label_space)

        Label(self.window, width=6, text='HP成長').place(x=313, y=current_y)
        self.hp_grown = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.hp_grown).place(x=313, y=current_y + label_space)

        Label(self.window, width=6, text='暴擊率').place(x=375, y=current_y)
        self.critical_rate = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.critical_rate).place(x=375, y=current_y + label_space)

        Label(self.window, width=6, text='攻速').place(x=426, y=current_y)
        self.atk_speed = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.atk_speed).place(x=426, y=current_y + label_space)

        Label(self.window, width=6, text='跑速').place(x=477, y=current_y)
        self.walk_speed = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.walk_speed).place(x=477, y=current_y + label_space)

        # 第三個 Row
        current_y = 101
        Label(self.window, width=6, text='技能花費').place(x=12, y=current_y)
        self.active_cost = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.active_cost['values'] = [3, 2, 1]
        self.active_cost.place(x=10, y=current_y+label_space-2)

        Label(self.window, width=39, text='主動技').place(x=78, y=current_y)
        self.active = StringVar(value='')
        Entry(self.window, width=39, textvariable=self.active).place(x=78, y=current_y+label_space)

        Label(self.window, width=25, text='備註').place(x=370, y=current_y)
        self.note = StringVar(value='')
        Entry(self.window, width=25, textvariable=self.note).place(x=370, y=current_y+label_space)

        # 第四個 Row
        current_y = 150
        Label(self.window, width=38, text='被動技1').place(x=10, y=current_y)
        self.passive1 = StringVar(value='')
        Entry(self.window, width=38, textvariable=self.passive1).place(x=10, y=current_y+label_space)

        Label(self.window, width=37, text='被動技2').place(x=288, y=current_y)
        self.passive2 = StringVar(value='')
        Entry(self.window, width=37, textvariable=self.passive2).place(x=288, y=current_y+label_space)

        # 最後一個 Row
        current_y = 215
        Button(self.window, text="Submit", command=self.do_submit, width=33, borderwidth=3).place(x=24, y=current_y)
        Button(self.window, text="Cancel", command=self.do_cancel, width=33, borderwidth=3).place(x=290, y=current_y)

    # 若四格都有輸入，則會計算出每突的成長值
    def do_transform_grown(self):
        if (self.max_atk.get() != '') & (self.max_hp.get() != '') &\
                (self.max_atk_after_break.get() != '') & (self.max_hp_after_break.get() != ''):
            self.atk_grown.set(UpdateCharacterWindow.calculate_grown(
                self.max_atk.get(), self.max_atk_after_break.get()))
            self.hp_grown.set(UpdateCharacterWindow.calculate_grown(
                self.max_hp.get(), self.max_hp_after_break.get()))
        else:
            tkMessageBox.showerror('錯誤', '部分 Atk/HP 欄位未填')

    @staticmethod
    def calculate_grown(max_value, max_after_break):
        return str((int(max_after_break) - int(max_value)) / 4)

    # TODO 更新
    def do_submit(self):
        print 'submit'
        self.window.destroy()

    def do_cancel(self):
        self.window.destroy()

        # # noinspection PyAttributeOutsideInit
        # def __init_record(self, master):
        # # 取得最近一筆資料，以作為預設值
        # command = 'select * from RecordOfDrawLots' + \
        # ' where Times = (select max(Times) from RecordOfDrawLots)'
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
    root.geometry("300x100+540+360")
    app = UpdateCharacterWindow(master=root)
    app.mainloop()
