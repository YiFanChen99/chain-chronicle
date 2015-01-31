# -*- coding: utf-8 -*-
from BasicWindow import *
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *


class CharacterWindow(BasicWindow):
    def __init__(self, master, character, callback, width=558, height=287, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.geometry('+840+300')

        self._init_widget()
        self._init_character(character)
        self.callback = callback
        self.title('Character with ID: {0}'.format(self.character.c_id))

    def _init_widget(self):
        label_space = 22  # Label 與 輸入元件的距離

        # 第一個 Row
        current_x = 16
        current_y = 3
        Label(self, width=10, text='暱稱').place(x=current_x, y=current_y)
        self.nickname = StringVar(value='')
        Entry(self, width=10, textvariable=self.nickname).place(x=current_x, y=current_y + label_space)

        current_x += 80
        Label(self, width=17, text='全名').place(x=current_x - 1, y=current_y)
        self.full_name = StringVar(value='')
        Entry(self, width=17, textvariable=self.full_name).place(x=current_x, y=current_y + label_space)

        current_x += 133
        Label(self, width=6, text='職業').place(x=current_x + 1, y=current_y)
        self.profession = ttk.Combobox(self, state='readonly', width=5, justify=CENTER)
        self.profession['values'] = PROFESSIONS
        self.profession.place(x=current_x, y=current_y + label_space - 2)
        self.profession.bind('<<ComboboxSelected>>', lambda event: self.fill_in_automatically_by_professions())

        current_x += 70
        Label(self, width=4, text='等級').place(x=current_x, y=current_y)
        self.rank = ttk.Combobox(self, state='readonly', width=3, justify=CENTER)
        self.rank['values'] = RANKS
        self.rank.place(x=current_x, y=current_y + label_space - 2)

        current_x += 54
        Label(self, width=5, text='Cost').place(x=current_x - 3, y=current_y)
        self.attendance_cost = StringVar(value='')
        Entry(self, width=5, textvariable=self.attendance_cost).place(x=current_x, y=current_y + label_space)

        current_x += 46
        Label(self, width=6, text='武器種類').place(x=current_x + 1, y=current_y)
        self.weapon_type = ttk.Combobox(self, state='readonly', width=5, justify=CENTER)
        self.weapon_type['values'] = WEAPONS
        self.weapon_type.place(x=current_x, y=current_y + label_space - 2)
        self.weapon_type.bind('<<ComboboxSelected>>', lambda event: self.fill_in_automatically_by_weapon())

        current_x += 71
        Label(self, width=6, text='成長類型').place(x=current_x + 2, y=current_y)
        self.exp_grown = ttk.Combobox(self, state='readonly', width=6, justify=CENTER)
        self.exp_grown['values'] = EXP_GROWN
        self.exp_grown.place(x=current_x, y=current_y + label_space - 2)

        # 第二個 Row
        current_x = 15
        current_y = 52
        Label(self, width=6, text='暴擊率').place(x=current_x, y=current_y)
        self.critical_rate = StringVar(value='')
        Entry(self, width=6, textvariable=self.critical_rate).place(x=current_x, y=current_y + label_space)

        current_x += 52
        Label(self, width=6, text='攻速').place(x=current_x, y=current_y)
        self.atk_speed = StringVar(value='')
        Entry(self, width=6, textvariable=self.atk_speed).place(x=current_x, y=current_y + label_space)

        current_x += 57
        Label(self, width=6, text='滿級Atk').place(x=current_x - 1, y=current_y)
        self.max_atk = StringVar(value='')
        Entry(self, width=6, textvariable=self.max_atk).place(x=current_x, y=current_y + label_space)

        current_x += 51
        Label(self, width=6, text='滿級HP').place(x=current_x - 1, y=current_y)
        self.max_hp = StringVar(value='')
        Entry(self, width=6, textvariable=self.max_hp).place(x=current_x, y=current_y + label_space)

        current_x += 51
        Label(self, width=6, text='突滿Atk').place(x=current_x - 1, y=current_y)
        self.max_atk_after_break = StringVar(value='')
        Entry(self, width=6, textvariable=self.max_atk_after_break).place(x=current_x, y=current_y + label_space)

        current_x += 51
        Label(self, width=6, text='突滿HP').place(x=current_x - 1, y=current_y)
        self.max_hp_after_break = StringVar(value='')
        Entry(self, width=6, textvariable=self.max_hp_after_break).place(x=current_x, y=current_y + label_space)

        current_x += 52
        Button(self, text="轉換", command=self.transforming_grown, width=4, borderwidth=3) \
            .place(x=current_x, y=current_y + label_space - 13)

        current_x += 48
        Label(self, width=6, text='Atk成長').place(x=current_x, y=current_y)
        self.atk_grown = StringVar(value='')
        Entry(self, width=6, textvariable=self.atk_grown).place(x=current_x, y=current_y + label_space)

        current_x += 51
        Label(self, width=6, text='HP成長').place(x=current_x, y=current_y)
        self.hp_grown = StringVar(value='')
        Entry(self, width=6, textvariable=self.hp_grown).place(x=current_x, y=current_y + label_space)

        current_x += 57
        Label(self, width=7, text='備註').place(x=current_x - 1, y=current_y)
        self.note = StringVar(value='')
        Entry(self, width=7, textvariable=self.note).place(x=current_x, y=current_y + label_space)

        # 主動技、被動與絆的 Rows
        current_y = 108
        Label(self, width=6, text='技能花費').place(x=13, y=current_y)
        self.active_cost = ttk.Combobox(self, state='readonly', width=3, justify=CENTER)
        self.active_cost['values'] = [3, 2, 1]
        self.active_cost.place(x=70, y=current_y - 2)
        self.active = StringVar(value='')
        Entry(self, width=59, textvariable=self.active).place(x=123, y=current_y)
        current_y += 33
        Label(self, width=6, text='被動技1').place(x=12, y=current_y - 1)
        self.passive1 = StringVar(value='')
        Entry(self, width=67, textvariable=self.passive1).place(x=68, y=current_y)
        current_y += 32
        Label(self, width=6, text='被動技2').place(x=12, y=current_y - 1)
        self.passive2 = StringVar(value='')
        Entry(self, width=67, textvariable=self.passive2).place(x=68, y=current_y)
        current_y += 32
        Label(self, width=6, text='絆能力').place(x=12, y=current_y - 1)
        self.belonged = ttk.Combobox(self, state='readonly', width=6, justify=CENTER)
        self.belonged['values'] = BELONGEDS
        self.belonged.place(x=65, y=current_y - 2)
        self.attachment = StringVar(value='')
        Entry(self, width=56, textvariable=self.attachment).place(x=144, y=current_y)

        # 最後一個 Row
        current_y += 40
        Button(self, text="Submit", command=self.submitting, width=34, relief=RIDGE).place(x=19, y=current_y)
        Button(self, text="Cancel", command=self.destroy, width=34, relief=RIDGE).place(x=286, y=current_y)

    def _init_character(self, character):
        if not isinstance(character, Character):
            raise TypeError('Input Character types {0}, not \'Character\'!'.format(type(character)))

        self.character = character
        self.nickname.set(self.character.nickname)
        self.full_name.set(self.character.full_name)
        self.profession.set(self.character.profession)
        self.rank.set(self.character.rank)
        self.attendance_cost.set(self.character.attendance_cost)
        self.weapon_type.set(self.character.weapon_type)
        self.exp_grown.set(self.character.exp_grown)
        self.critical_rate.set(self.character.critical_rate)
        self.atk_speed.set(self.character.atk_speed)
        self.max_atk.set(self.character.max_atk)
        self.max_hp.set(self.character.max_hp)
        self.max_atk_after_break.set(self.character.max_atk_after_break)
        self.max_hp_after_break.set(self.character.max_hp_after_break)
        self.atk_grown.set(self.character.atk_grown)
        self.hp_grown.set(self.character.hp_grown)
        self.note.set(convert_to_str(self.character.note))
        self.active.set(convert_to_str(self.character.active))
        self.active_cost.set(self.character.active_cost)
        self.passive1.set(convert_to_str(self.character.passive_1))
        self.passive2.set(convert_to_str(self.character.passive_2))
        self.belonged.set(convert_to_str(self.character.belonged))
        self.attachment.set(convert_to_str(self.character.attachment))

    # 根據選擇職業，填入預設的對應資訊
    def fill_in_automatically_by_professions(self):
        profession = self.profession.get()
        if profession == PROFESSIONS[0]:  # 戰士
            self.weapon_type.set(WEAPONS[0])
            self.critical_rate.set(0.4)
            self.atk_speed.set(1.5)
        elif profession == PROFESSIONS[1]:  # 騎士
            self.weapon_type.set(WEAPONS[0])
            self.critical_rate.set(0)
            self.atk_speed.set(1.75)
        elif profession == PROFESSIONS[2]:  # 弓手
            self.weapon_type.set(WEAPONS[3])
            self.critical_rate.set(0)
            self.atk_speed.set(2)
        elif profession == PROFESSIONS[3]:  # 法師
            self.weapon_type.set(WEAPONS[4])
            self.critical_rate.set(0)
            self.atk_speed.set(2)
        else:  # 僧侶
            self.weapon_type.set(WEAPONS[5])
            self.critical_rate.set(0)
            self.atk_speed.set(2)

    # 根據選擇武器，填入預設的對應資訊
    def fill_in_automatically_by_weapon(self):
        weapon = self.weapon_type.get()
        if weapon == WEAPONS[7]:  # 銃 or 狙
            self.atk_speed.set(6)

    # 若四格都有輸入，則會計算出每突的成長值
    def transforming_grown(self):
        if (self.max_atk.get() != '') & (self.max_hp.get() != '') & \
                (self.max_atk_after_break.get() != '') & (self.max_hp_after_break.get() != ''):
            self.atk_grown.set(calculate_grown(int(self.max_atk.get()), int(self.max_atk_after_break.get())))
            self.hp_grown.set(calculate_grown(int(self.max_hp.get()), int(self.max_hp_after_break.get())))
        else:
            tkMessageBox.showerror('錯誤', '部分 Atk/HP 欄位未填', parent=self)

    def submitting(self):
        self.character.nickname = self.nickname.get()
        self.character.full_name = self.full_name.get()
        self.character.profession = self.profession.get()
        self.character.rank = int(self.rank.get())
        self.character.attendance_cost = int(self.attendance_cost.get())
        self.character.weapon_type = self.weapon_type.get()
        self.character.exp_grown = self.exp_grown.get()
        self.character.critical_rate = float(self.critical_rate.get())
        self.character.atk_speed = float(self.atk_speed.get())
        self.character.max_atk = int(self.max_atk.get())
        self.character.max_hp = int(self.max_hp.get())
        self.character.atk_grown = int(self.atk_grown.get())
        self.character.hp_grown = int(self.hp_grown.get())
        self.character.note = self.note.get()
        self.character.active = self.active.get()
        self.character.active_cost = int(self.active_cost.get())
        self.character.passive_1 = self.passive1.get()
        self.character.passive_2 = self.passive2.get()
        self.character.belonged = self.belonged.get()
        self.character.attachment = self.attachment.get()

        self.callback()
        self.destroy()
