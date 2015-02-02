# -*- coding: utf-8 -*-
import json
from Window.CharacterWindow import *
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


class MyDBInserter(object):
    def __init__(self, view, data_owner=None):
        self.view = view
        self.data_owner = CCGameDBTWDataOwner() if data_owner is None else data_owner
        self.total_count = 0
        self.inserted_count = 0

    def insert_new_characters(self):
        self.total_count = 0
        self.inserted_count = 0

        for character_id in self._get_not_existed_ids():
            self.total_count += 1
            try:
                # 逐一根據其 ID 開啟新增視窗
                character = Character.create_by_cgdt_character(
                    self.data_owner.find_character_by_id(character_id))
                popup = CharacterWindow(self.view, character, lambda: self._insert_new_character(character))
                self.view.wait_window(popup)
            # 若資料取得發生問題，則記錄後就略過
            except StandardError as e:
                print e

        tkMessageBox.showinfo('Completed', '總計 {0} 筆新資料，其中 {1} 筆新增完成'.format(
            self.total_count, self.inserted_count), parent=self.view)

    def _get_not_existed_ids(self):
        # 若 id>=6000，代表是國服的角色，不用檢查
        recorded_ids = [record[0] for record in
                        DBAccessor.execute('select ID from Character where ID<6000').fetchall()]

        return [int(record[0]) for record in self.data_owner.data if not int(record[0]) in recorded_ids]

    # 插入該角色的資訊
    def _insert_new_character(self, character):
        CharacterModel.insert_character_into_db(character)

        self.inserted_count += 1


class MyDBUpdater(object):
    def __init__(self, view, data_owner=None):
        self.view = view
        self.data_owner = CCGameDBTWDataOwner() if data_owner is None else data_owner
        self.total_count = 0
        self.updated_count = 0

    def update_new_characters(self):
        self.total_count = 0
        self.updated_count = 0

        for character_name in self._get_new_character_names():
            self.total_count += 1
            try:
                # 逐一根據其 FullName 開啟更新視窗
                character = Character.create_by_cgdt_character(
                    self.data_owner.find_character_by_full_name(character_name))
                popup = CharacterWindow(self.view, character, lambda: self._update_new_character_with_its_id(character))
                self.view.wait_window(popup)
            # 若資料取得發生問題，則記錄後就略過
            except StandardError as e:
                print e

        tkMessageBox.showinfo('Completed', '總計 {0} 筆新資料，其中 {1} 筆更新完成'.format(
            self.total_count, self.updated_count), parent=self.view)

    @staticmethod
    def _get_new_character_names():
        # 新增的角色其 ID 會 <1000
        return [record[0] for record in
                DBAccessor.execute('select FullName from Character where ID<1000').fetchall()]

    # 先將原本的暫用 ID 更新，再更新其他資訊
    def _update_new_character_with_its_id(self, character):
        DBAccessor.execute('update Character{0} where FullName={1}'.format(
            convert_data_to_update_command(['ID'], [character.c_id]), convert_datum_to_command(character.full_name)))
        CharacterModel.update_character_into_db(character)

        self.updated_count += 1

    # 範例用，新增欄位時可根據此修改
    def update_belonged_info(self, overwrite=False):
        def get_belonged_info(char_id, find_method=self.data_owner.find_character_by_id):
            return find_method(char_id).belonged
        self._update_specific_info('Belonged', overwrite, get_belonged_info)

    # 針對已存在我資料庫中的角色，根據特定規則，以 CGDT 的資料更新
    @staticmethod
    def _update_specific_info(column_name, overwrite, get_info_method):
        # 若 ID>=6000，代表是國服的角色，此處不處理
        characters = DBAccessor.execute('select ID, {0} from Character where ID<6000'.format(column_name)).fetchall()
        for character in characters:
            MyDBUpdater._update_character_specific_info(character, column_name, overwrite, get_info_method)
        DBAccessor.commit()

    @staticmethod
    def _update_character_specific_info(character, column_name, overwrite, get_info_method):
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
