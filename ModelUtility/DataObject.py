# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from DBAccessor import *
from ModelUtility.CCGameDBTW import CGDTCharacter


class Character(object):
    def __init__(self, character_id=None, cgdt_character=None):
        if character_id is not None:
            self.c_id = character_id
            return
        if cgdt_character is not None:
            if isinstance(cgdt_character, CGDTCharacter):
                self._init_info_by_cgdt(cgdt_character)
            else:
                raise TypeError('Character object types {0}, not CGDTCharacter.'.format(type(cgdt_character)))

    @property
    def c_id(self):
        return self._c_id

    # noinspection PyAttributeOutsideInit
    @c_id.setter
    def c_id(self, value):
        if not isinstance(value, int):
            raise TypeError('Set Character ID with type {0}.'.format(type(value)))
        self._c_id = value
        self._init_info()

    # noinspection PyUnusedLocal
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

    def _init_info_by_cgdt(self, cgdt_character):
        self.info_list = []

        self._c_id = cgdt_character.c_id
        self.info_list.append(self._c_id)
        self.full_name = cgdt_character.full_name
        self.info_list.append(self.full_name)
        self.nickname = cgdt_character.nickname
        self.info_list.append(self.nickname)
        self.profession = cgdt_character.profession
        self.info_list.append(self.profession)
        self.rank = cgdt_character.rank
        self.info_list.append(self.rank)
        self.active = cgdt_character.active
        self.info_list.append(self.active)
        self.active_cost = cgdt_character.active_cost
        self.info_list.append(self.active_cost)
        self.passive1 = cgdt_character.passive_1
        self.info_list.append(self.passive1)
        self.passive2 = cgdt_character.passive_2
        self.info_list.append(self.passive2)
        self.attachment = cgdt_character.attachment
        self.info_list.append(self.attachment)
        self.weapon_type = cgdt_character.weapon
        self.info_list.append(self.weapon_type)
        self.exp_grown = cgdt_character.exp_grown
        self.info_list.append(self.exp_grown)
        self.attendance_cost = cgdt_character.cost
        self.info_list.append(self.attendance_cost)
        self.max_atk = cgdt_character.max_atk
        self.info_list.append(self.max_atk)
        self.max_hp = cgdt_character.max_hp
        self.info_list.append(self.max_hp)
        self.atk_grown = cgdt_character.atk_grown
        self.info_list.append(self.atk_grown)
        self.hp_grown = cgdt_character.hp_grown
        self.info_list.append(self.hp_grown)
        self.atk_speed = cgdt_character.hit_rate
        self.info_list.append(self.atk_speed)
        self.critical_rate = cgdt_character.critical_rate
        self.info_list.append(self.critical_rate)
        self.note = ''
        self.info_list.append('')
        self.belonged = cgdt_character.belonged
        self.info_list.append(self.belonged)

    def __str__(self):
        return 'ID={0}, FullName={1}, Nickname={2}'.format(
            self._c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))

    @staticmethod
    def get_character_info(character_id):
        return DBAccessor.execute('select * from Character where ID={0}'.format(character_id)).fetchone()
