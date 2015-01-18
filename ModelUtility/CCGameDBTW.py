# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import json
from ModelUtility.CommonString import *
from ModelUtility.DBAccessor import *

DEFAULT_PATH = 'data/CCGameDBTW.txt'
# BulletSpeed 弓統基本15，法10
# Tag [male][Log Horizon]等，應是對應網站中提供的標籤篩選功能
# @Unknown1 總是15，懷疑是跑速，但寶石也一樣；@Unknown2 總是2；@Unknown3 總是0
COLUMNS = ['ID', 'Title', 'Name', 'Nickname', 'Rank', 'Cost', 'ProfessionID', 'Classification',
           'Weapon', 'GrownSpeed', 'InitAtk', 'InitHP', 'MaxAtk', 'MaxHP', 'MaxBrokenAtk', 'MaxBrokenHP',
           'OwnedWay', 'ActiveCost', 'Active', 'Passive1Level', 'Passive1', 'Passive2Level', 'Passive2',
           'HitRate', '@Unknown1', 'BulletSpeed', 'CriticalRate', 'Artist', 'CharacterVoice', 'Tag',
           'ActiveName', 'Passive1Name', 'Passive2Name', 'ExpGrown', '@Unknown2', '@Unknown3',
           'Belonged', 'Attachment', 'AttachmentName', 'AttachedCost']
COLUMN_COUNT = len(COLUMNS)


class CCGameDBTWDataOwner:
    def __init__(self, file_path=DEFAULT_PATH):
        self.data = load_json(file_path)

    def find_character_by_id(self, the_id):
        for each_character in self.data:
            if int(each_character[0]) == the_id:
                return CharacterInfo(each_character)

    def find_character_by_full_name(self, full_name):
        for each_character in self.data:
            if (each_character[1] + each_character[2]) == full_name:
                return CharacterInfo(each_character)

    def get_specific_character_info(self, column_name, the_id=None, full_name=None):
        if the_id is None and full_name is None:
            raise Exception('Both id and full_name is None.')

        index = COLUMNS.index(column_name)

        if the_id is None:
            for each_character in self.data:
                if (each_character[1] + each_character[2]) == full_name:
                    return each_character[index]
        else:
            for each_character in self.data:
                if int(each_character[0]) == the_id:
                    return each_character[index]


class CharacterInfo:
    # noinspection PyUnusedLocal
    def __init__(self, the_list):
        properties = iter(the_list)
        self.id = int(next(properties))
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
        self.belonged = self.convert_belonged(next(properties))
        self.attachment = next(properties)
        dropped = next(properties)  # AttachmentName
        self.attached_cost = int(next(properties))

    # Make fields read-only
    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value

    @staticmethod
    def convert_grown(origin_max, broken_max):
        return (broken_max - origin_max) / 4

    @staticmethod
    def convert_belonged(origin):
        if origin == u'海風之港':
            return u'海風'
        elif origin == u'賢者之塔':
            return u'賢塔'
        elif origin == u'迷宮山脈':
            return u'山脈'
        else:
            return origin

    def __str__(self):
        return 'ID={0}, FullName={1}, Nickname={2}'.format(
            self.id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))


# TODO
class MyDBInserter:
    def __init__(self, data_owner=None):
        self.data_owner = CCGameDBTWDataOwner() if data_owner is None else data_owner


class MyDBUpdater:
    def __init__(self, data_owner=None):
        self.data_owner = CCGameDBTWDataOwner() if data_owner is None else data_owner

    def update_belonged_info(self, overwrite=False):
        def get_belonged_info(char_id, data_owner=self.data_owner):
            character_info = data_owner.find_character_by_id(char_id)
            return None if character_info is None else character_info.belonged
        self.__update_specific_character_info('Belonged', overwrite, get_belonged_info)

    # 針對已存在我資料庫中的角色，根據特定欄位的資料，以 CGDT 的資料更新
    def __update_specific_character_info(self, column_name, overwrite, get_info_method):
        characters = DBAccessor.execute('select ID, {0} from Character'.format(column_name)).fetchall()
        for character in characters:
            the_id = character[0]
            # 若 id>=6000，代表是國服的角色。
            # 是否要強制覆蓋？或是原本無該資料則需更新。
            if (the_id < 6000) and (overwrite or character[1] is None):
                # 若角色不存在 CGDT 中，記錄後就略過
                specific_info = get_info_method(the_id)
                if specific_info is None:
                    print 'Character with ID {0} does not exist in CGDT.'.format(the_id)
                    continue

                DBAccessor.execute('update Character{0} where ID={1}'.format(
                    convert_data_to_update_command([column_name], [specific_info]), the_id))
        DBAccessor.commit()


# 取出該 DB 檔案中的資訊，並作初步的欄位比對檢查
def load_json(filename):
    with open('%s' % filename) as json_data:
        my_data = json.loads(json_data.read().decode('utf-8-sig'))

    # verify columns
    if len(my_data[0]) == COLUMN_COUNT:
        return my_data
    else:
        for i in range(0, COLUMN_COUNT):
            print COLUMNS[i], ': ', my_data[i]
        raise Exception('Columns 比對錯誤： CCDB 共 %d 欄，COLUMNS 共 %d 欄' % (len(my_data[0]), COLUMN_COUNT))
