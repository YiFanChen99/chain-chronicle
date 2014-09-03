# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Static import *
import ttk
import tkMessageBox

# Character 表格中的各欄位
COLUMNS = ['FullName', 'Nickname', 'Profession', 'Rank',
           'Active', 'ActiveCost', 'Passive1', 'Passive2', 'WeaponType',
           'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown',
           'HPGrown', 'AtkSpeed', 'WalkSpeed', 'CriticalRate', 'Note']


class UpdateCharacterWindow(Frame):
    def __init__(self, master, character=None):
        Frame.__init__(self, master)
        self.window = Toplevel(width=564, height=255)
        self.window.title('About character')
        self.window.geometry('+700+210')

        label_space = 22  # Label 與 輸入元件的距離

        # 第一個 Row
        current_y = 3
        Label(self.window, width=10, text='暱稱').place(x=10, y=current_y)
        self.nickname = StringVar(value='')
        Entry(self.window, width=10, textvariable=self.nickname).place(x=10, y=current_y + label_space)

        Label(self.window, width=17, text='全名').place(x=89, y=current_y)
        self.full_name = StringVar(value='')
        Entry(self.window, width=17, textvariable=self.full_name).place(x=90, y=current_y + label_space)

        Label(self.window, width=4, text='等級').place(x=220, y=current_y)
        self.rank = ttk.Combobox(self.window, state='readonly', width=3, justify=CENTER)
        self.rank['values'] = RANKS
        self.rank.place(x=220, y=current_y + label_space - 2)

        Label(self.window, width=5, text='Cost').place(x=272, y=current_y)
        self.attendance_cost = StringVar(value='')
        Entry(self.window, width=5, textvariable=self.attendance_cost).place(x=274, y=current_y + label_space)

        Label(self.window, width=6, text='職業').place(x=321, y=current_y)
        self.profession = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.profession['values'] = PROFESSIONS
        self.profession.place(x=320, y=current_y + label_space - 2)

        Label(self.window, width=6, text='武器種類').place(x=389, y=current_y)
        self.weapon_type = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.weapon_type['values'] = WEAPONS
        self.weapon_type.place(x=387, y=current_y + label_space - 2)

        Label(self.window, width=6, text='成長類型').place(x=455, y=current_y)
        self.exp_grown = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.exp_grown['values'] = EXP_GROWN
        self.exp_grown.place(x=455, y=current_y + label_space - 2)

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
            .place(x=215, y=current_y + label_space - 13)

        Label(self.window, width=6, text='Atk成長').place(x=263, y=current_y)
        self.atk_grown = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.atk_grown).place(x=263, y=current_y + label_space)

        Label(self.window, width=6, text='HP成長').place(x=314, y=current_y)
        self.hp_grown = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.hp_grown).place(x=314, y=current_y + label_space)

        Label(self.window, width=6, text='暴擊率').place(x=377, y=current_y)
        self.critical_rate = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.critical_rate).place(x=377, y=current_y + label_space)

        Label(self.window, width=6, text='攻速').place(x=429, y=current_y)
        self.atk_speed = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.atk_speed).place(x=429, y=current_y + label_space)

        Label(self.window, width=6, text='跑速').place(x=481, y=current_y)
        self.walk_speed = StringVar(value='')
        Entry(self.window, width=6, textvariable=self.walk_speed).place(x=481, y=current_y + label_space)

        # 第三個 Row
        current_y = 101
        Label(self.window, width=6, text='技能花費').place(x=12, y=current_y)
        self.active_cost = ttk.Combobox(self.window, state='readonly', width=5, justify=CENTER)
        self.active_cost['values'] = [3, 2, 1]
        self.active_cost.place(x=10, y=current_y + label_space - 2)

        Label(self.window, width=46, text='主動技').place(x=82, y=current_y)
        self.active = StringVar(value='')
        Entry(self.window, width=46, textvariable=self.active).place(x=82, y=current_y + label_space)

        Label(self.window, width=18, text='備註').place(x=419, y=current_y)
        self.note = StringVar(value='')
        Entry(self.window, width=18, textvariable=self.note).place(x=420, y=current_y + label_space)

        # 第四個 Row
        current_y = 150
        Label(self.window, width=38, text='被動技1').place(x=10, y=current_y)
        self.passive1 = StringVar(value='')
        Entry(self.window, width=38, textvariable=self.passive1).place(x=10, y=current_y + label_space)

        Label(self.window, width=37, text='被動技2').place(x=288, y=current_y)
        self.passive2 = StringVar(value='')
        Entry(self.window, width=37, textvariable=self.passive2).place(x=288, y=current_y + label_space)

        # 最後一個 Row
        current_y = 215
        Button(self.window, text="Submit", command=self.do_submit, width=33, borderwidth=3).place(x=24, y=current_y)
        Button(self.window, text="Cancel", command=self.do_cancel, width=33, borderwidth=3).place(x=290, y=current_y)

        self.__init_character(character)

    # 若四格都有輸入，則會計算出每突的成長值
    def do_transform_grown(self):
        if (self.max_atk.get() != '') & (self.max_hp.get() != '') & \
                (self.max_atk_after_break.get() != '') & (self.max_hp_after_break.get() != ''):
            self.atk_grown.set(self.calculate_grown(self.max_atk.get(), self.max_atk_after_break.get()))
            self.hp_grown.set(self.calculate_grown(self.max_hp.get(), self.max_hp_after_break.get()))
        else:
            tkMessageBox.showerror('錯誤', '部分 Atk/HP 欄位未填')

    @staticmethod
    def calculate_grown(max_value, max_after_break):
        return str((int(max_after_break) - int(max_value)) / 4)

    def do_submit(self):
        # 將可能存在資料庫的資料先刪除，接續之後的插入就是更新動作了
        full_name = self.full_name.get()
        DATABASE.execute('delete from Character where FullName=' + convert_datum_to_command(full_name))

        DATABASE.execute('insert into Character(' + ','.join(COLUMNS) + ')' +
                         convert_data_to_insert_command(full_name, self.nickname.get(),
                                                        self.profession.get(), self.rank.get(),
                                                        self.active.get(),
                                                        self.active_cost.get(), self.passive1.get(),
                                                        self.passive2.get(), self.weapon_type.get(),
                                                        self.exp_grown.get(), self.attendance_cost.get(),
                                                        self.max_atk.get(), self.max_hp.get(),
                                                        self.atk_grown.get(), self.hp_grown.get(),
                                                        self.atk_speed.get(), self.walk_speed.get(),
                                                        self.critical_rate.get(), self.note.get()))
        DATABASE.commit()
        self.window.destroy()
        self.destroy()

    @staticmethod
    def select_character(character):
        condition = ' where Character=' + convert_datum_to_command(character)
        return DATABASE.execute('select * from Character' + condition).fetchone()

    # 當有特定的 character 時，讀取其資料並更新各元件
    def __init_character(self, character):
        if character is not None:
            data = iter(self.select_character(character))
            self.full_name.set(convert_to_str(next(data)))
            self.nickname.set(convert_to_str(next(data)))
            self.profession.set(convert_to_str(next(data)))
            self.rank.set(next(data))
            self.active.set(convert_to_str(next(data)))
            self.active_cost.set(next(data))
            self.passive1.set(convert_to_str(next(data)))
            self.passive2.set(convert_to_str(next(data)))
            self.weapon_type.set(convert_to_str(next(data)))
            self.exp_grown.set(convert_to_str(next(data)))
            self.attendance_cost.set(next(data))
            self.max_atk.set(next(data))
            self.max_hp.set(next(data))
            self.atk_grown.set(next(data))
            self.hp_grown.set(next(data))
            self.atk_speed.set(next(data))
            self.walk_speed.set(next(data))
            self.critical_rate.set(next(data))
            self.note.set(convert_to_str(next(data)))
        else:
            self.walk_speed.set(1.5)

    def do_cancel(self):
        self.window.destroy()
        self.destroy()