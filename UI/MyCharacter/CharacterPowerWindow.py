# -*- coding: utf-8 -*-
from UI.Utility.BasicWindow import *
from UI.Utility.CharacterSelector import CharacterSelectorCanvas
from ModelUtility.CommonValue import *
from ModelUtility.DataObject import CharacterPower
from Model import CharacterPowerModel


class CharacterPowerWindow(BasicWindow):
    def __init__(self, master, character_power, callback, width=558, height=226, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('CharacterPower')
        self.character_power = character_power
        self.callback = callback
        self._init_widget()
        self._init_content()

    def _init_widget(self):
        current_y_diff = 28

        current_y = 20
        current_x = 23
        self.character_selector = CharacterSelectorCanvas(self, self.character_power.character)
        self.character_selector.place(x=current_x, y=current_y - 3)
        self.character_selector.bind('<Return>', lambda event: (
            self.fill_in_automatically_by_character(self.character_selector.get()), level_entry.focus_set()))

        current_x += 145
        Label(self, width=5, text='Level', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.level = StringVar()
        level_entry = Entry(self, width=5, textvariable=self.level, font=(SCP, 12), justify=CENTER)
        level_entry.place(x=current_x + 2, y=current_y + current_y_diff)
        level_entry.bind('<Return>', lambda x: atk_entry.focus_set())

        current_x += 62
        Label(self, width=5, text='Atk', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.atk = StringVar()
        atk_entry = Entry(self, width=5, textvariable=self.atk, font=(SCP, 12), justify=CENTER)
        atk_entry.place(x=current_x + 3, y=current_y + current_y_diff)
        atk_entry.bind('<Return>', lambda x: atk_raised_entry.focus_set())

        current_x += 70
        Label(self, width=25, text='Addition', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.addition = StringVar()
        addition_entry = Entry(self, width=25, textvariable=self.addition, font=(MS_JH, 12), justify=CENTER)
        addition_entry.place(x=current_x + 3, y=current_y + current_y_diff)
        addition_entry.bind('<Return>', lambda x: self.submitting())

        current_y += 14 + current_y_diff * 2
        current_x = 27
        Label(self, width=8, text='AtkRaised', font=(SCP, 10)).place(x=current_x + 1, y=current_y + 3)
        self.atk_raised = StringVar()
        atk_raised_entry = Entry(self, width=7, textvariable=self.atk_raised, font=(SCP, 12), justify=CENTER)
        atk_raised_entry.place(x=current_x, y=current_y + current_y_diff)
        atk_raised_entry.bind('<Return>', lambda x: hit_rate_entry.focus_set())

        current_x += 90
        Label(self, width=7, text='HitRate', font=(SCP, 11)).place(x=current_x, y=current_y)
        self.hit_rate = StringVar()
        hit_rate_entry = Entry(self, width=6, textvariable=self.hit_rate, font=(SCP, 12), justify=CENTER)
        hit_rate_entry.place(x=current_x + 2, y=current_y + current_y_diff)
        hit_rate_entry.bind('<Return>', lambda x: critical_ratio_entry.focus_set())

        current_x += 83
        Label(self, width=8, text='Cri.Ratio', font=(SCP, 10)).place(x=current_x, y=current_y + 3)
        self.critical_ratio = StringVar()
        critical_ratio_entry = Entry(self, width=6, textvariable=self.critical_ratio, font=(SCP, 12), justify=CENTER)
        critical_ratio_entry.place(x=current_x + 3, y=current_y + current_y_diff)
        critical_ratio_entry.bind('<Return>', lambda x: critical_factor_entry.focus_set())

        current_x += 85
        Label(self, width=9, text='Cri.Factor', font=(SCP, 9)).place(x=current_x, y=current_y + 4)
        self.critical_factor = StringVar()
        critical_factor_entry = Entry(self, width=6, textvariable=self.critical_factor, font=(SCP, 12), justify=CENTER)
        critical_factor_entry.place(x=current_x + 3, y=current_y + current_y_diff)
        critical_factor_entry.bind('<Return>', lambda x: active_factor_entry.focus_set())

        current_x += 84
        Label(self, width=9, text='Act.Factor', font=(SCP, 9)).place(x=current_x, y=current_y + 4)
        self.active_factor = StringVar()
        active_factor_entry = Entry(self, width=6, textvariable=self.active_factor, font=(SCP, 12), justify=CENTER)
        active_factor_entry.place(x=current_x + 4, y=current_y + current_y_diff)
        active_factor_entry.bind('<Return>', lambda x: active_cost_entry.focus_set())

        current_x += 86
        Label(self, width=8, text='Act.Cost', font=(SCP, 11)).place(x=current_x, y=current_y + 3)
        self.active_cost = StringVar()
        active_cost_entry = Entry(self, width=6, textvariable=self.active_cost, font=(SCP, 12), justify=CENTER)
        active_cost_entry.place(x=current_x + 5, y=current_y + current_y_diff)
        active_cost_entry.bind('<Return>', lambda x: addition_entry.focus_set())

        # 送出、取消的按鈕
        current_y += 25 + current_y_diff * 2
        Button(self, text="Submit", command=self.submitting, width=34, relief=RIDGE, font=(SCP, 11)).place(
            x=30, y=current_y)
        Button(self, text="Cancel", command=self.destroy, width=17, relief=RIDGE, font=(SCP, 11)).place(
            x=364, y=current_y)

    def _init_content(self):
        self.atk.set(self.character_power.atk)
        self.level.set(self.character_power.level)
        self.atk_raised.set(self.character_power.atk_raised)
        self.hit_rate.set(self.character_power.hit_rate)
        self.critical_ratio.set(self.character_power.critical_ratio)
        self.critical_factor.set(self.character_power.critical_factor)
        self.active_factor.set(self.character_power.active_factor)
        self.active_cost.set(self.character_power.active_cost)
        self.addition.set(self.character_power.addition)

    def submitting(self):
        self.character_power.character = self.character_selector.get()
        self.character_power.atk = int(self.atk.get())
        self.character_power.level = int(self.level.get())
        self.character_power.atk_raised = float(self.atk_raised.get())
        self.character_power.hit_rate = float(self.hit_rate.get())
        self.character_power.critical_ratio = float(self.critical_ratio.get())
        self.character_power.critical_factor = float(self.critical_factor.get())
        self.character_power.active_factor = float(self.active_factor.get())
        self.character_power.active_cost = int(self.active_cost.get())
        self.character_power.addition = self.addition.get()
        self.callback()
        self.destroy()

    def fill_in_automatically_by_character(self, character):
        self.hit_rate.set(character.atk_speed)
        self.critical_ratio.set(character.critical_rate)
        self.active_cost.set(character.active_cost)


# 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_new_character_power_window(master, callback):
    cp = CharacterPower.create_empty_character_power()
    popup = CharacterPowerWindow(master, cp, lambda: (
        CharacterPowerModel.insert_character_power_into_db(cp), callback(cp)))
    master.wait_window(popup)


# 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_character_power_window(master, character_power, callback):
    original_c_id = character_power.c_id
    original_level = character_power.level
    popup = CharacterPowerWindow(master, character_power, lambda: (
        CharacterPowerModel.update_character_power_into_db(character_power, original_c_id, original_level), callback()))
    master.wait_window(popup)
