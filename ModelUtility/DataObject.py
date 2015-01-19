# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from DBAccessor import *


class Character(object):
    def __init__(self, character_id=None):
        if character_id is not None:
            self.c_id = character_id

    @property
    def c_id(self):
        return self._c_id

    @c_id.setter
    def c_id(self, value):
        if not isinstance(value, int):
            raise TypeError('Set Character ID with type {0}.'.format(type(value)))
        self._c_id = value
        self._init_info()

    def _init_info(self):
        self.info_list = []
        record = iter(self.get_character_info(self._c_id))

        dropped = next(record)  # ID
        self.info_list.append(self._c_id)
        self.full_name = next(record)
        self.info_list.append(self.full_name)
        self.nickname = next(record)
        self.info_list.append(self.nickname)
        self.profession = next(record)
        self.info_list.append(self.profession)
        self.rank = next(record)
        self.info_list.append(self.rank)
        self.active = next(record)
        self.info_list.append(self.active)
        self.active_cost = next(record)
        self.info_list.append(self.active_cost)
        self.passive1 = next(record)
        self.info_list.append(self.passive1)
        self.passive2 = next(record)
        self.info_list.append(self.passive2)
        self.attachment = next(record)
        self.info_list.append(self.attachment)
        self.weapon_type = next(record)
        self.info_list.append(self.weapon_type)
        self.exp_grown = next(record)
        self.info_list.append(self.exp_grown)
        self.attendance_cost = next(record)
        self.info_list.append(self.attendance_cost)
        self.max_atk = next(record)
        self.info_list.append(self.max_atk)
        self.max_hp = next(record)
        self.info_list.append(self.max_hp)
        self.atk_grown = next(record)
        self.info_list.append(self.atk_grown)
        self.hp_grown = next(record)
        self.info_list.append(self.hp_grown)
        self.atk_speed = next(record)
        self.info_list.append(self.atk_speed)
        self.critical_rate = next(record)
        self.info_list.append(self.critical_rate)
        self.note = next(record)
        self.info_list.append(self.note)
        self.belonged = next(record)
        self.info_list.append(self.belonged)

    def __str__(self):
        return 'ID={0}, FullName={1}, Nickname={2}'.format(
            self._c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))

    @staticmethod
    def get_character_info(character_id):
        return DBAccessor.execute('select * from Character where ID={0}'.format(character_id)).fetchone()
