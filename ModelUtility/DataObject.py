# -*- coding: utf-8 -*-
from datetime import datetime
from CommonString import *

DRAW_LOTS_DB_TABLE = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']


class Character(object):
    DB_TABLE = ['ID', 'FullName', 'Nickname', 'Profession', 'Rank', 'Active', 'ActiveCost', 'Passive1', 'Passive2',
                'Attachment', 'WeaponType', 'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP', 'AtkGrown', 'HPGrown',
                'AtkSpeed', 'CriticalRate', 'Note', 'Belonged']
    DISPLAYED_COLUMNS = [DB_TABLE[0]] + DB_TABLE[2:11] + DB_TABLE[13:15] + DB_TABLE[19:21]

    def __init__(self, infos=None, cgdt_character=None):
        if infos is not None:
            self._init_info_list(infos)
        elif cgdt_character is not None:
            if isinstance(cgdt_character, CGDTCharacter):
                self._init_info_list_by_cgdt(cgdt_character)
            else:
                raise TypeError('Character object types {0}, not CGDTCharacter.'.format(type(cgdt_character)))
        else:
            raise LookupError('None infos and cgdt_character input.')

    def _init_info_list(self, infos):
        self.info_list = list(infos)
        inputs = iter(infos)

        self.c_id = next(inputs)
        self.info_list.append(self.c_id)
        self.full_name = next(inputs)
        self.info_list.append(self.full_name)
        self.nickname = next(inputs)
        self.info_list.append(self.nickname)
        self.profession = next(inputs)
        self.info_list.append(self.profession)
        self.rank = next(inputs)
        self.info_list.append(self.rank)
        self.active = next(inputs)
        self.info_list.append(self.active)
        self.active_cost = next(inputs)
        self.info_list.append(self.active_cost)
        self.passive1 = next(inputs)
        self.info_list.append(self.passive1)
        self.passive2 = next(inputs)
        self.info_list.append(self.passive2)
        self.attachment = next(inputs)
        self.info_list.append(self.attachment)
        self.weapon_type = next(inputs)
        self.info_list.append(self.weapon_type)
        self.exp_grown = next(inputs)
        self.info_list.append(self.exp_grown)
        self.attendance_cost = next(inputs)
        self.info_list.append(self.attendance_cost)
        self.max_atk = next(inputs)
        self.info_list.append(self.max_atk)
        self.max_hp = next(inputs)
        self.info_list.append(self.max_hp)
        self.atk_grown = next(inputs)
        self.info_list.append(self.atk_grown)
        self.hp_grown = next(inputs)
        self.info_list.append(self.hp_grown)
        self.atk_speed = next(inputs)
        self.info_list.append(self.atk_speed)
        self.critical_rate = next(inputs)
        self.info_list.append(self.critical_rate)
        self.note = next(inputs)
        self.info_list.append(self.note)
        self.belonged = next(inputs)
        self.info_list.append(self.belonged)

    def _init_info_list_by_cgdt(self, cgdt_character):
        self.info_list = []

        self.c_id = cgdt_character.c_id
        self.info_list.append(self.c_id)
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
        return 'Character: ID={0}, FullName={1}, Nickname={2}'.format(
            self.c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))


class CGDTCharacter(object):
    # BulletSpeed 弓統基本15，法10
    # Tag [male][Log Horizon]等，應是對應網站中提供的標籤篩選功能
    # @Unknown1 總是15，懷疑是跑速，但寶石也一樣；@Unknown2 總是2；@Unknown3 總是0
    DB_TABLE = ['ID', 'Title', 'Name', 'Nickname', 'Rank', 'Cost', 'ProfessionID', 'Classification', 'Weapon',
                'GrownSpeed', 'InitAtk', 'InitHP', 'MaxAtk', 'MaxHP', 'MaxBrokenAtk', 'MaxBrokenHP', 'OwnedWay',
                'ActiveCost', 'Active', 'Passive1Level', 'Passive1', 'Passive2Level', 'Passive2', 'HitRate',
                '@Unknown1', 'BulletSpeed', 'CriticalRate', 'Artist', 'CharacterVoice', 'Tag', 'ActiveName',
                'Passive1Name', 'Passive2Name', 'ExpGrown', '@Unknown2', '@Unknown3',
                'Belonged', 'Attachment', 'AttachmentName', 'AttachedCost']

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
        self._init_belonged(next(properties))
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
    def _init_belonged(self, name):
        replaced_name = name.replace(u'海風之港', u'海風').replace(u'賢者之塔', u'賢塔'). \
            replace(u'迷宮山脈', u'山脈').replace(u'獸里', u'獸之里')

        if replaced_name in BELONGEDS:
            self.belonged = replaced_name
        else:
            raise ValueError('Invalid Belonged name {0} for {1}.'.format(
                name.encode('utf-8'), self.full_name.encode('utf-8')))

    def __str__(self):
        return 'CGDTCharacter: ID={0}, FullName={1}, Nickname={2}'.format(
            self.c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))


class FriendInfo(object):
    DB_TABLE = ['ID', 'UsedNames', 'Excellence', 'Defect', 'Relation', 'Offline', 'UsedCharacters', 'Rank',
                'RaisedIn3Weeks', 'RaisedIn2Months', 'AddedDate', 'LastProfession', 'LastCharacter']
    CLEANED_UP_COLUMNS = DB_TABLE[1:len(DB_TABLE)]  # 除了 ID 外的所有欄位
    DISPLAYED_COLUMNS = DB_TABLE[0:12]
    UPDATED_COLUMNS = DB_TABLE[1:6] + [DB_TABLE[10]]
    # UPDATED_BY_STATISTIC_COLUMNS = DB_TABLE[6:10] + DB_TABLE[11:13]  #TODO

    def __init__(self, infos):
        if infos is None:
            raise ValueError('Input infos is None.')

        properties = iter(infos)

        self.f_id = next(properties)
        self.used_names = next(properties)
        self.excellence = next(properties)
        self.defect = next(properties)
        self.relation = next(properties)
        self.offline = next(properties)
        self.used_characters = next(properties)
        self.rank = next(properties)
        self.raised_in_3_weeks = next(properties)
        self.raised_in_2_months = next(properties)
        self._added_date = next(properties)
        self.last_profession = next(properties)

    # 資料已存在時使用原資料，若為新好友則回傳當天日期
    @property
    def added_date(self):
        return self._added_date if self._added_date else datetime.now().date()

    @added_date.setter
    def added_date(self, value):
        self._added_date = value

    def get_displayed_info(self):
        return [self.f_id, self.used_names.encode('utf-8'), self.excellence.encode('utf-8'),
                self.defect.encode('utf-8'), self.relation.encode('utf-8'), self.offline,
                self.used_characters.encode('utf-8'), self.rank, self.raised_in_3_weeks,
                self.raised_in_2_months, self._added_date, self.last_profession.encode('utf-8')]

    def get_updated_info(self):
        if not self.used_names:
            raise ValueError('Used names is empty')
        return [self.used_names.encode('utf-8'), self.excellence.encode('utf-8'), self.defect.encode('utf-8'),
                self.relation.encode('utf-8'), self.offline, self.added_date]

    def __getitem__(*args, **kwargs):
        return getattr(*args, **kwargs)

    def __str__(self):
        return 'FriendInfo: ID={0}, UsedNames={1}'.format(self.f_id, self.used_names.encode('utf-8'))


class FriendRecord(object):
    DB_TABLE = ['FriendID', 'RecordedDate', 'Character', 'CharacterLevel', 'Rank']
    FRIEND_INFO_SELECTED_COLUMNS = ['ID', 'UsedNames', 'Rank', 'LastProfession', 'LastCharacter']
    DISPLAYED_COLUMNS = FRIEND_INFO_SELECTED_COLUMNS[0:2] + DB_TABLE[2:5] + FRIEND_INFO_SELECTED_COLUMNS[2:4]

    def __init__(self, infos):
        self.f_id = infos[0]
        self.used_names = infos[1]
        self.character_nickname = None
        self.character_level = None
        self.rank = None
        self.last_rank = infos[2]
        self.last_profession = infos[3]
        self.last_character = infos[4]

        self.status = UNRECORDED

    # 簡單檢查資料，若通過則更新記錄，並調整狀態為「已記錄」
    def record(self, nickname, level, rank):
        # 檢查 level/rank 是否大於 0
        if level < 1 or rank < 1:
            raise ValueError('Level/Rank < 1')
        # 檢查 rank 是否不小於前記錄
        if rank < self.last_rank:
            raise ValueError('Rank {0} too small, last rank is {1}'.format(rank, self.last_rank))

        self.character_nickname = nickname
        self.character_level = level
        self.rank = rank
        self.status = RECORDED

    # 該 rank 之變化是否異常（成長過快 / 負成長）
    def is_unusual_rank(self, the_rank):
        return the_rank > self.last_rank + 3 or the_rank < self.last_rank

    # 角色名稱已指定時便套用，否則套用前角色名稱
    @property
    def current_character(self):
        return self.character_nickname if self.character_nickname is not None else \
            self.last_character if self.last_character is not None else ''

    # 角色等級未選擇時為空（方便直接填新值），已選擇便用已選擇
    @property
    def current_character_level(self):
        return self.character_level if self.character_level is not None else ''

    # Rank 等級未選擇時為空（方便直接填新值），已選擇便用已選擇
    @property
    def current_rank(self):
        return self.rank if self.rank is not None else ''

    def get_displayed_info(self):
        return [self.f_id, self.used_names.encode('utf-8'), self.current_character.encode('utf-8'),
                self.current_character_level, self.current_rank, self.last_rank, self.last_profession.encode('utf-8')]

    def get_inserted_info(self, date):
        return self.f_id, date, self.character_nickname, self.character_level, self.rank

    def __getitem__(*args, **kwargs):
        return getattr(*args, **kwargs)

    def __str__(self):
        return 'FriendRecord: ID={0}, UsedNames={1}, Status={2}'.format(
            self.f_id, self.used_names.encode('utf-8'), self.status)
