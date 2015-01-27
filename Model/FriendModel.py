# -*- coding: utf-8 -*-
from ModelUtility.CommonState import *
# from datetime import timedelta
# from ModelUtility.CommonString import *
# from Window.FriendWindow import FriendInfoUpdaterWindow, FriendRecordUpdaterWindow
from ModelUtility.DBAccessor import DBAccessor
# from ModelUtility.Utility import bind_check_box_and_label


# 重新統計 FriendRecord 並寫入 Friend Table 內
def re_do_statistic_to_update_friend_info():
    # 對每個好友進行處理
    for info in DBAccessor.execute('select ID from Friend' + get_db_suffix() + ' where UsedNames!=\'\'').fetchall():
        re_do_statistic_to_update_friend_info_by_specific_id(info[0])
    DBAccessor.commit()


# TODO 資料結構未定，等 friend_info 完成再看看
# 更新特定好友的資訊到記憶體的 DB 中，而先不 commit
def re_do_statistic_to_update_friend_info_by_specific_id(friend_id):
    pass
    # friend_info = FriendInfo(the_id=friend_id)
    #
    # # 取出該 ID 對應的所有記錄，從最近排序到最久以前
    # records = DBAccessor.execute('select ' + ','.join(FriendRecord.DB_TABLE[1:5]) +
    #                              ' from FriendRecord' + get_db_suffix() +
    #                              ' where FriendID={1} order by RecordedDate DESC'.format(friend_id)).fetchall()
    #
    # # 新好友可能會尚無記錄可供更新，則不必處理
    # if len(records) == 0:
    #     return
    #
    # # 最新一筆資料即為新的 Rank LastProfession LastCharacter
    # friend_info.rank = records[0][3]
    # friend_info.
    # self.last_character = records[0][1]
    # self.last_profession = DATABASE.execute('select Profession from Character where Nickname=' +
    #                                         convert_datum_to_command(self.last_character)).fetchone()[0]
    # self.rank = records[0][3]
    #
    # # 找出 UsedCharacters RaisedIn3Weeks RaisedIn2Months
    # self.raised_recorder = RaisedRecorder()
    # self.character_recorder = CharacterRecorder()
    # for record in records:
    #     # 更新範圍內日期的 Rank，以取得範圍內的改變量
    #     self.raised_recorder.record_if_in_duration(record)
    #     # 將有使用的角色彙整
    #     self.character_recorder.record_if_not_existed(record)
    # self.raised_in_3_weeks = self.raised_recorder.get_raised_in_3_weeks()
    # self.raised_in_2_months = self.raised_recorder.get_raised_in_2_months()
    # self.used_characters = self.character_recorder.get_used_characters()
    #
    # DATABASE.execute('update Friend' + get_db_suffix() + convert_data_to_update_command(
    #     UPDATED_BY_RECORD_COLUMN, [self.used_characters, self.rank, self.raised_in_3_weeks,
    #                                self.raised_in_2_months, self.last_profession, self.last_character]) +
    #                  ' where ID=' + str(friend_id))


#
# class RaisedRecorder:
#     def __init__(self):
#         self.date_of_3_weeks = datetime.now() - timedelta(weeks=2)
#         self.date_of_2_months = datetime.now() - timedelta(days=61)
#         self.newest_rank = 0
#
#     # 此方法被呼叫時必須保持由新到舊的順序傳入記錄，才可取得真正的區間內變化
#     # noinspection PyAttributeOutsideInit
#     def record_if_in_duration(self, record):
#         # 記錄最新的 Rank，結算時使用
#         if self.newest_rank == 0:
#             self.newest_rank = record[3]
#
#         recorded_date = convert_str_to_datetime(record[0])
#         if self.date_of_3_weeks <= recorded_date:
#             self.rank_3_weeks_ago = record[3]
#         if self.date_of_2_months <= recorded_date:
#             self.rank_2_months_ago = record[3]
#
#     def get_raised_in_3_weeks(self):
#         return self.newest_rank - self.rank_3_weeks_ago
#
#     def get_raised_in_2_months(self):
#         return self.newest_rank - self.rank_2_months_ago
#
#
# class CharacterRecorder:
#     def __init__(self):
#         self.used_characters = {}
#
#     # 此方法被呼叫時必須保持由新到舊的順序傳入記錄，才可取得各角色的最高等級
#     def record_if_not_existed(self, record):
#         nickname = convert_to_str(record[1])
#         if not nickname in self.used_characters:
#             self.used_characters[nickname] = record[2]
#
#     def get_used_characters(self):
#         result = ''
#         for name, level in self.used_characters.iteritems():
#             result += name + str(level) + '、'
#         return result