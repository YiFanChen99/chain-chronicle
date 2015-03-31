# -*- coding: utf-8 -*-
from UI.Utility.BasicWindow import *
from UI.Utility.CharacterSelector import CharacterSelectorCanvas
from UI.Utility.Entry import IntEntry
from ModelUtility.CommonValue import *
from ModelUtility.DataObject import CharacterWeapon
from Model import CharacterWeaponModel


class CharacterWeaponWindow(BasicWindow):
    def __init__(self, master, character_weapon, callback, width=454, height=209, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('CharacterWeapon')
        self.character_weapon = character_weapon
        self.callback = callback
        self._init_widget()
        self._init_content()

    def _init_widget(self):
        current_y_diff = 27

        self.character_selector = CharacterSelectorCanvas(self)
        self.character_selector.place(x=23, y=42)
        self.character_selector.bind('<Return>', lambda event: self.max_atk.focus_set())

        current_y = 10
        current_x = 171
        Label(self, width=7, text='MaxAtk', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.max_atk = IntEntry(self, width=5, font=(SCP, 12))
        self.max_atk.place(x=current_x + 10, y=current_y + current_y_diff)
        self.max_atk.bind('<Return>', lambda event: self.max_critical.focus_set())

        current_x += 87
        Label(self, width=8, text='MaxCrit.', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.max_critical = IntEntry(self, width=5, font=(SCP, 12))
        self.max_critical.place(x=current_x + 16, y=current_y + current_y_diff)
        self.max_critical.bind('<Return>', lambda event: self.max_armor.focus_set())

        current_x += 92
        Label(self, width=8, text='MaxArmor', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.max_armor = IntEntry(self, width=5, font=(SCP, 12))
        self.max_armor.place(x=current_x + 16, y=current_y + current_y_diff)
        self.max_armor.bind('<Return>', lambda event: self.current_atk.focus_set())
        self.max_armor.bind('<Control-Return>', lambda event: self.auto_fill())

        current_y += 65
        current_x = 171
        Label(self, width=7, text='CurAtk', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.current_atk = IntEntry(self, width=5, font=(SCP, 12))
        self.current_atk.place(x=current_x + 10, y=current_y + current_y_diff)
        self.current_atk.bind('<Return>', lambda event: self.current_critical.focus_set())

        current_x += 87
        Label(self, width=8, text='CurCrit.', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.current_critical = IntEntry(self, width=5, font=(SCP, 12))
        self.current_critical.place(x=current_x + 16, y=current_y + current_y_diff)
        self.current_critical.bind('<Return>', lambda event: self.current_armor.focus_set())

        current_x += 92
        Label(self, width=8, text='CurArmor', font=(SCP, 12)).place(x=current_x, y=current_y)
        self.current_armor = IntEntry(self, width=5, font=(SCP, 12))
        self.current_armor.place(x=current_x + 16, y=current_y + current_y_diff)
        self.current_armor.bind('<Return>', lambda event: self.submitting())

        # 送出、取消的按鈕
        current_y += 81
        Button(self, text="Submit", command=self.submitting, width=25, relief=RIDGE, font=(SCP, 11)).place(
            x=34, y=current_y)
        Button(self, text="Cancel", command=self.destroy, width=12, relief=RIDGE, font=(SCP, 11)).place(
            x=297, y=current_y)

    def _init_content(self):
        self.character_selector.set(self.character_weapon.character)
        self.max_atk.set(self.character_weapon.max_atk)
        self.max_critical.set(self.character_weapon.max_critical)
        self.max_armor.set(self.character_weapon.max_armor)
        self.current_atk.set(self.character_weapon.current_atk)
        self.current_critical.set(self.character_weapon.current_critical)
        self.current_armor.set(self.character_weapon.current_armor)

    def submitting(self):
        if self.current_atk.get() > self.max_atk.get() or self.current_critical.get() > self.max_critical.get() or \
                self.current_armor.get() > self.max_armor.get():
            raise ValueError('Current value over then max value.')

        self.character_weapon.character = self.character_selector.get()
        self.character_weapon.max_atk = self.max_atk.get()
        self.character_weapon.max_critical = self.max_critical.get()
        self.character_weapon.max_armor = self.max_armor.get()
        self.character_weapon.current_atk = self.current_atk.get()
        self.character_weapon.current_critical = self.current_critical.get()
        self.character_weapon.current_armor = self.current_armor.get()
        self.callback()
        self.destroy()

    def auto_fill(self):
        self.current_atk.set(self.max_atk.get())
        self.current_critical.set(self.max_critical.get())
        self.current_armor.set(self.max_armor.get())
        self.current_armor.focus_set()


# 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_new_character_weapon_window(master, callback):
    cw = CharacterWeapon.create_empty_character_weapon()
    popup = CharacterWeaponWindow(master, cw, lambda: (
        CharacterWeaponModel.insert_character_weapon_into_db(cw), callback(cw)))
    master.wait_window(popup)


# 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_character_weapon_window(master, character_weapon, callback):
    original_c_id = character_weapon.c_id
    popup = CharacterWeaponWindow(master, character_weapon, lambda: (
        CharacterWeaponModel.update_character_weapon_into_db(character_weapon, original_c_id), callback()))
    master.wait_window(popup)
