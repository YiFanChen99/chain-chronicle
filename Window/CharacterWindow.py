# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from BasicWindow import *
from UIUtility.Selector import ProfessionSelector, RankSelector
from ModelUtility.DBAccessor import *
from ModelUtility.Comparator import *
from ModelUtility.Filter import FilterManager


class CharacterSelectionWindow(BasicWindow):
    def __init__(self, master, callback, character_selected, width=316, height=146, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.title('Character selection')

        self.records = None
        self.update_records()
        self.filter_manager = FilterManager()
        self.filter_manager.set_comparison_rule(0)
        self.filter_manager.set_comparison_rule(1)

        self._init_widgets()
        self._init_character_selected(character_selected)
        self.callback = callback

    def _init_widgets(self):
        self.profession_selector = ProfessionSelector(self, self.updating_request_profession)
        self.profession_selector.place(x=3, y=3)
        self.rank_selector = RankSelector(self, self.updating_request_rank)
        self.rank_selector.place(x=3, y=49)

        Label(self, text='篩選', width=5, font=("", 11)).place(x=208, y=3)
        self.name_request = StringVar(value='')
        entry = Entry(self, width=7, textvariable=self.name_request, font=("", 11))
        entry.place(x=226, y=22)
        entry.bind('<Return>', self.updating_character_selector)

        Label(self, text='Character', width=10, font=("", 12)).place(x=204, y=47)
        self.character_selector = ttk.Combobox(self, state='readonly', width=10, justify=CENTER)
        self.character_selector.place(x=209, y=68)

        y_position = 105
        # 送交的按鈕
        button = Button(self, text="選擇此角色", width=11, borderwidth=3)
        button.place(x=15, y=y_position)
        button["command"] = self.submitting

        # 新增角色的按鈕
        button = Button(self, text="新增角色", width=9, borderwidth=3)
        button.place(x=123, y=y_position)
        button["command"] = self.adding_new_character

        # 取消並結束的按鈕
        button = Button(self, text="放棄選擇", width=9, borderwidth=3)
        button.place(x=217, y=y_position)
        button["command"] = self.destroy

    def _init_character_selected(self, character_selected):
        if isinstance(character_selected, Character):
            self.profession_selector.select(character_selected.profession)
            self.rank_selector.select(character_selected.rank)
            self.updating_character_selector()
            self.character_selector.set(character_selected.nickname)
        else:
            raise TypeError('In CharacterSelectionWindow, arg: \"character_selected\"')

    def updating_request_profession(self, profession):
        self.filter_manager.set_specific_condition(2, profession)
        self.updating_character_selector()

    def updating_request_rank(self, rank):
        self.filter_manager.set_specific_condition(3, rank, match_requested_rank)
        self.updating_character_selector()

    # 清除原本的選擇，並更新可選擇的角色
    # noinspection PyUnusedLocal
    def updating_character_selector(self, event=None):
        self.character_selector.set('')
        character_matched = []
        for character_infos in self.filter_manager.filter(self.records, convert_to_str(self.name_request.get())):
            character_matched.append(character_infos[0])
        self.character_selector['values'] = character_matched
        self.character_selector.focus_set()

    # 有選擇的情況下才回傳，否則彈出錯誤視窗
    def submitting(self):
        if self.character_selector.get() != '':
            self.callback(DBAccessor.select_character_by_specific_column('Nickname', self.character_selector.get()))
            self.destroy()
        else:
            tkMessageBox.showwarning("Character haven't selected", '\"Character\" 未選\n', parent=self)

    def adding_new_character(self):
        popup = CharacterInfoWindow(self)
        self.wait_window(popup)
        self.update_records()
        self.updating_character_selector()

    def update_records(self):
        self.records = DBAccessor.execute('select Nickname, FullName, Profession, Rank from Character').fetchall()


class CharacterInfoWindow(BasicWindow):
    def __init__(self, master, character_id=None, width=558, height=285, **kwargs):
        BasicWindow.__init__(self, master, width=width, height=height, **kwargs)
        self.geometry('+840+300')

        self.__init_widget()
        self.__init_character_info(character_id)
        self.title('Character ID: {0}'.format(self.character_id))

    def __init_widget(self):
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
        self.profession.bind('<<ComboboxSelected>>', self.filling_in_automatically_by_professions)

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
        self.weapon_type.bind('<<ComboboxSelected>>', self.filling_in_automatically_by_weapon)

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
        current_y += 38
        Button(self, text="Submit", command=self.submitting, width=33, borderwidth=3).place(x=23, y=current_y)
        Button(self, text="Cancel", command=self.destroy, width=33, borderwidth=3).place(x=289, y=current_y)

    # noinspection PyUnusedLocal
    # 根據選擇職業，預設填入對應資訊
    def filling_in_automatically_by_professions(self, event=None):
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

    # noinspection PyUnusedLocal
    # 根據選擇武器，預設填入對應資訊
    def filling_in_automatically_by_weapon(self, event=None):
        weapon = self.weapon_type.get()
        if weapon == WEAPONS[7]:  # 銃/ 狙
            self.atk_speed.set(6)

    # 若四格都有輸入，則會計算出每突的成長值
    def transforming_grown(self):
        if (self.max_atk.get() != '') & (self.max_hp.get() != '') & \
                (self.max_atk_after_break.get() != '') & (self.max_hp_after_break.get() != ''):
            self.atk_grown.set(self.calculate_grown(self.max_atk.get(), self.max_atk_after_break.get()))
            self.hp_grown.set(self.calculate_grown(self.max_hp.get(), self.max_hp_after_break.get()))
        else:
            tkMessageBox.showerror('錯誤', '部分 Atk/HP 欄位未填', parent=self)

    @staticmethod
    def calculate_grown(max_value, max_after_break):
        return str((int(max_after_break) - int(max_value)) / 4)

    def submitting(self):
        # 將可能存在資料庫的資料先刪除，接續之後的插入就是更新動作了
        DBAccessor.execute('delete from Character where ID={0}'.format(self.character_id))

        DBAccessor.execute('insert into Character({0})'.format(','.join(CHARACTER_DB_TABLE)) +
                           convert_data_to_insert_command(self.character_id, self.full_name.get(), self.nickname.get(),
                                                          self.profession.get(), self.rank.get(),
                                                          self.active.get(), self.active_cost.get(),
                                                          self.passive1.get(), self.passive2.get(),
                                                          self.attachment.get(), self.weapon_type.get(),
                                                          self.exp_grown.get(), self.attendance_cost.get(),
                                                          self.max_atk.get(), self.max_hp.get(),
                                                          self.atk_grown.get(), self.hp_grown.get(),
                                                          self.atk_speed.get(), self.critical_rate.get(),
                                                          self.note.get(), self.belonged.get()))
        DBAccessor.commit()
        self.destroy()

    # 當有特定的 character 時，讀取其資料並更新各元件
    def __init_character_info(self, character_id):
        if character_id is not None:
            data = iter(self.select_character(character_id))
            self.character_id = next(data)
            self.full_name.set(convert_to_str(next(data)))
            self.nickname.set(convert_to_str(next(data)))
            self.profession.set(convert_to_str(next(data)))
            self.rank.set(next(data))
            self.active.set(convert_to_str(next(data)))
            self.active_cost.set(next(data))
            self.passive1.set(convert_to_str(next(data)))
            self.passive2.set(convert_to_str(next(data)))
            self.attachment.set(convert_to_str(next(data)))
            self.weapon_type.set(convert_to_str(next(data)))
            self.exp_grown.set(convert_to_str(next(data)))
            self.attendance_cost.set(next(data))
            self.max_atk.set(next(data))
            self.max_hp.set(next(data))
            self.atk_grown.set(next(data))
            self.hp_grown.set(next(data))
            self.atk_speed.set(next(data))
            self.critical_rate.set(next(data))
            self.note.set(convert_to_str(next(data)))
            self.belonged.set(convert_to_str(next(data)))
        else:
            self.__init_character_id()

    @staticmethod
    def select_character(character_id):
        return DBAccessor.execute('select * from Character where ID={0}'.format(character_id)).fetchone()

    def __init_character_id(self):
        min_id = DBAccessor.execute('select min(ID) from Character').fetchone()[0]
        self.character_id = 900 if min_id > 999 else min_id - 1
