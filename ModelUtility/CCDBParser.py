# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

import json

FILE_PATH = '../data/CCGameDBTW.txt'
# BulletSpeed 弓統基本15，法10
# Tag [male][Log Horizon]等，應是對應網站中提供的標籤篩選功能
# @Unknown1 總是15，懷疑是跑速，但寶石也一樣；@Unknown2 總是2；@Unknown3 總是0
COLUMNS = ['ID', 'Title', 'Name', 'Nickname', 'Rank', 'Cost', 'ProfessionID', 'Classification',
           'Weapon', 'GrownSpeed', 'InitAtk', 'InitHP', 'MaxAtk', 'MaxHP', 'MaxBrokenAtk', 'MaxBrokenHP',
           'OwnedWay', 'ActiveCost', 'Active', 'Passive1Level', 'Passive1', 'Passive2Level', 'Passive2',
           'HitRate', '@Unknown1', 'BulletSpeed', 'CriticalRate', 'Artist', 'CharacterVoice', 'Tag',
           'ActiveName', 'Passive1Name', 'Passive2Name', 'ExpGrown', '@Unknown2', '@Unknown3',
           'Birthplace ', 'Attachment', 'AttachmentName', 'AttachmentCost']
COLUMN_COUNT = len(COLUMNS)


class CCDBManager:
    def __init__(self):
        self.data = load_json(FILE_PATH)

    def find_characters(self, full_name):
        for each_character in self.data:
            if (each_character[1] + each_character[2]) == full_name:
                return dict(zip(COLUMNS, each_character))


# 取出該 DB 檔案中的資訊，並作初步的欄位比對檢查
def load_json(filename):
    with open('%s' % filename) as json_data:
        data = json.loads(json_data.read().decode('utf-8-sig'))

    # verify columns
    if len(data[0]) == COLUMN_COUNT:
        return data
    else:
        for i in range(0, COLUMN_COUNT):
            print COLUMNS[i], ': ', data[i]
        raise Exception('Columns 比對錯誤： CCDB 共 %d 欄，COLUMNS 共 %d 欄' % (len(data[0]), COLUMN_COUNT))


# 確認角色個數與欄位正確性
if __name__ == "__main__":
    manager = CCDBManager()

    print 'Total character: ', len(manager.data)

    # For testing, 找角色
    for element, b in manager.find_characters(u'追憶の樹人トレランシア').items():
        print element, b,