# -*- coding: utf-8 -*-
import json
from ModelUtility.DBAccessor import *
from ModelUtility.DataObject import *
from Model import CharacterModel

CGDT_DEFAULT_PATH = 'data/CCGameDBTW.txt'


class CCGameDBTWDataOwner:
    def __init__(self, file_path=CGDT_DEFAULT_PATH):
        self.data = load_json(file_path)

    def find_character_by_id(self, the_id):
        for each_character in self.data:
            if int(each_character[0]) == the_id:
                return CGDTCharacter(each_character)
        raise KeyError('Character with ID {0} does not exist in CGDT.'.format(the_id))

    def find_character_by_full_name(self, full_name):
        for each_character in self.data:
            if (each_character[1] + each_character[2]) == full_name:
                return CGDTCharacter(each_character)
        raise KeyError('Character with FullName {0} does not exist in CGDT.'.format(full_name.encode('utf-8')))


# TODO
class MyDBInserter:
    def __init__(self, data_owner=None):
        self.data_owner = CCGameDBTWDataOwner() if data_owner is None else data_owner


class MyDBUpdater:
    def __init__(self, data_owner=None):
        self.data_owner = CCGameDBTWDataOwner() if data_owner is None else data_owner

    def update_new_character(self):
        # 新增的角色其 ID 會 <1000
        characters = DBAccessor.execute('select FullName from Character where ID<1000').fetchall()
        for character in characters:
            try:
                cgdt_character = self.data_owner.find_character_by_full_name(character[0])
                DBAccessor.execute('update Character{0} where FullName={1}'.format(
                    convert_data_to_update_command(['ID'], [cgdt_character.c_id]),
                    convert_datum_to_command(character[0])))
                CharacterModel.update_character_into_db(Character.create_by_cgdt_character(cgdt_character), commit_followed=False)
            # 若資料取得發生問題，則記錄後就略過
            except StandardError as e:
                print e
        DBAccessor.commit()

    def update_belonged_info(self, overwrite=False):
        def get_belonged_info(char_id, find_method=self.data_owner.find_character_by_id):
            return find_method(char_id).belonged
        self.__update_specific_info('Belonged', overwrite, get_belonged_info)

    # 針對已存在我資料庫中的角色，根據特定規則，以 CGDT 的資料更新
    @staticmethod
    def __update_specific_info(column_name, overwrite, get_info_method):
        # 若 ID>=6000，代表是國服的角色，此處不處理
        characters = DBAccessor.execute('select ID, {0} from Character where ID<6000'.format(column_name)).fetchall()
        for character in characters:
            MyDBUpdater.__update_character_specific_info(character, column_name, overwrite, get_info_method)
        DBAccessor.commit()

    @staticmethod
    def __update_character_specific_info(character, column_name, overwrite, get_info_method):
        # 是否要直接覆蓋？或是原本無該資料則需更新。
        if overwrite or character[1] is None:
            try:
                specific_info = get_info_method(character[0])
                DBAccessor.execute('update Character{0} where ID={1}'.format(
                    convert_data_to_update_command([column_name], [specific_info]), character[0]))
            # 若資料取得發生問題，則記錄後就略過
            except StandardError as e:
                print e


# 取出該 DB 檔案中的資訊
def load_json(filename):
    with open('%s' % filename) as json_data:
        return json.loads(json_data.read().decode('utf-8-sig'))
