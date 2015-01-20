# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from DBAccessor import *
from CommonString import *


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

    def update_to_db(self):
        self.update_to_db_without_commit()
        DBAccessor.commit()

    def update_to_db_without_commit(self):
        DBAccessor.execute('update Character{0} where ID={1}'.format(
            convert_data_to_update_command(CHARACTER_DB_TABLE, self.info_list), self._c_id))

    def __str__(self):
        return 'ID={0}, FullName={1}, Nickname={2}'.format(
            self._c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))

    @staticmethod
    def get_character_info(character_id):
        return DBAccessor.execute('select * from Character where ID={0}'.format(character_id)).fetchone()


class CGDTCharacter:
    # noinspection PyUnusedLocal
    def __init__(self, the_list):
        self.fields_number = -1  # 本身會自動被記入，故設 -1 以平衡

        properties = iter(the_list)
        self.c_id = int(next(properties))
        self.full_name = next(properties) + next(properties)
        self.nickname = next(properties)
        self.rank = int(next(properties))
        self.cost = int(next(properties))
        self.profession = PROFESSIONS[int(next(properties)) - 1]
        dropped = next(properties)  # Classification
        self.weapon = next(properties)
        dropped = next(properties)  # GrownSpeed
        dropped = next(properties)  # InitAtk
        dropped = next(properties)  # InitHP
        self.max_atk = int(next(properties))
        self.max_hp = int(next(properties))
        self.atk_grown = self.convert_grown(self.max_atk, int(next(properties)))
        self.hp_grown = self.convert_grown(self.max_hp, int(next(properties)))
        dropped = next(properties)  # OwnedWay
        self.active_cost = int(next(properties))
        self.active = next(properties)
        self.passive_1_level = int(next(properties))
        self.passive_1 = next(properties)
        self.passive_2_level = int(next(properties))
        self.passive_2 = next(properties)
        self.hit_rate = int(next(properties)) / 100.0
        dropped = next(properties)  # Unknown1
        dropped = next(properties)  # BulletSpeed
        self.critical_rate = int(next(properties)) / 100.0
        dropped = next(properties)  # Artist
        dropped = next(properties)  # CharacterVoice
        dropped = next(properties)  # Tag
        dropped = next(properties)  # ActiveName
        dropped = next(properties)  # Passive1Name
        dropped = next(properties)  # Passive2Name
        self.exp_grown = next(properties)
        dropped = next(properties)  # Unknown2
        dropped = next(properties)  # Unknown3
        self.__init_belonged(next(properties))
        self.attachment = next(properties)
        dropped = next(properties)  # AttachmentName
        self.attached_cost = int(next(properties))

    # Make fields read-only
    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
        self.__dict__['fields_number'] += 1

    @staticmethod
    def convert_grown(origin_max, broken_max):
        return (broken_max - origin_max) / 4

    # 除了將其命名轉成我的格式以外，也檢查不可有我預期外的名稱出現
    def __init_belonged(self, name):
        replaced_name = name.replace(u'海風之港', u'海風').replace(u'賢者之塔', u'賢塔').\
            replace(u'迷宮山脈', u'山脈').replace(u'獸里', u'獸之里')

        if replaced_name in BELONGEDS:
            self.belonged = replaced_name
        else:
            raise ValueError('Invalid Belonged name {0} for {1}.'.format(
                name.encode('utf-8'), self.full_name.encode('utf-8')))

    def __str__(self):
        return 'ID={0}, FullName={1}, Nickname={2}'.format(
            self.c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))
