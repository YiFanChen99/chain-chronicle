# -*- coding: utf-8 -*-
import tkMessageBox
from datetime import timedelta, date
from ModelUtility.CommonState import *
from ModelUtility.DBAccessor import *
from ModelUtility.CommonString import *
from ModelUtility.Utility import convert_str_to_date
from ModelUtility.DataObject import FriendInfo, FriendRecord


def commit():
    DBAccessor.commit()


def select_friend_info_list():
    return [FriendInfo(each) for each in
            DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames!=\'\''.format(
                ','.join(FriendInfo.SELECTED_COLUMNS), get_db_suffix()))]


def select_specific_friend_info(requested_id):
    return FriendInfo(DBAccessor.execute('select {0} from FriendInfo{1} where ID=={2}'.format(
        ','.join(FriendInfo.SELECTED_COLUMNS), get_db_suffix(), requested_id)).fetchone())


def select_unused_friend_info():
    return FriendInfo(DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames==\'\''.format(
        ','.join(FriendInfo.SELECTED_COLUMNS), get_db_suffix())).fetchone())


def update_friend_info_into_db(friend_info, commit_followed):
    DBAccessor.execute('update FriendInfo{0}{1} where ID={2}'.format(get_db_suffix(), convert_data_to_update_command(
        FriendInfo.UPDATED_COLUMNS, friend_info.get_updated_info()), friend_info.f_id))
    DBAccessor.commit_if_requested(commit_followed)


def select_new_friend_record_list():
    return [FriendRecord(each) for each in
            DBAccessor.execute('select {0} from FriendInfo{1} where UsedNames!=\'\''.format(
                ','.join(FriendRecord.FRIEND_INFO_SELECTED_COLUMNS), get_db_suffix()))]


def insert_friend_record_into_db(record, the_date, commit_followed):
    DBAccessor.execute('insert into FriendRecord{0} ({1}){2}'.format(
        get_db_suffix(), ','.join(FriendRecord.DB_TABLE),
        convert_data_to_insert_command(*record.get_inserted_info(the_date))))
    DBAccessor.commit_if_requested(commit_followed)


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_friend_with_conforming(master, friend_info, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete friend 「{0}」？'.format(
            friend_info.used_names.encode('utf-8')), parent=master):
        _delete_friend_from_db(friend_info)
        callback()


def _delete_friend_from_db(friend_info):
    # 將 FriendInfo table 中該 ID 的其他欄位全數清空
    columns = FriendInfo.CLEANED_UP_COLUMNS
    DBAccessor.execute('update FriendInfo{0}{1} where ID={2}'.format(
        get_db_suffix(), convert_data_to_update_command(columns, [''] * len(columns)), friend_info.f_id))
    # 將 FriendRecord table 中對應其 ID 的記錄全數刪除
    DBAccessor.execute('delete from FriendRecord{0} where FriendID={1}'.format(get_db_suffix(), friend_info.f_id))
    DBAccessor.commit()


# 欲取得最後更新全體記錄的時間，但只用了效果類似的手段（抓倒數第 25 筆更新的時間）
def get_since_all_record_date():
    all_record_date = convert_str_to_date(DBAccessor.execute(
        'select {1} from {0} order by {1} desc limit 1 offset 25'.format(
            'FriendRecord' + get_db_suffix(), 'RecordedDate')).fetchone()[0])
    return str((date.today() - all_record_date).days) if all_record_date is not None else '?'


# 重新統計 FriendRecord 並寫入 FriendInfo 內
def take_statistic_to_update_friend_info():
    # 對每個目前好友進行處理
    for friend in DBAccessor.execute('select ID from FriendInfo{0} where UsedNames!=\'\''.format(
            get_db_suffix())).fetchall():
        f_id = friend[0]
        statistic_taker = FriendStatisticTaker(f_id)
        # 取出該 ID 對應的所有記錄，從最近排序到最久以前
        records = DBAccessor.execute('select {0} from FriendRecord{1} where FriendID={2}'.format(
            ','.join(FriendStatisticTaker.FRIEND_RECORD_SELECTED_COLUMNS),
            get_db_suffix(), f_id) + ' order by RecordedDate DESC').fetchall()
        # 最新的好友，尚無記錄，則不用處理
        if len(records) == 0:
            continue

        statistic_taker.take_statistic(records)
        statistic_taker.update_into_memory_db()
    DBAccessor.commit()


# noinspection PyAttributeOutsideInit
class FriendStatisticTaker(object):
    FRIEND_INFO_UPDATED_COLUMNS = FriendInfo.DB_TABLE[6:10] + FriendInfo.DB_TABLE[11:13]
    FRIEND_RECORD_SELECTED_COLUMNS = FriendRecord.DB_TABLE[1:5]

    def __init__(self, f_id):
        self.f_id = f_id
        self._status = UNRECORDED
        self.date_of_3_weeks = date.today() - timedelta(weeks=2)
        self.date_of_2_months = date.today() - timedelta(days=61)
        self.used_characters = {}

    # 此方法被使用時必須保持由新到舊的順序傳入記錄，才會取得正確的資料
    def take_statistic(self, records):
        self._pre_process(records)

        # 最先傳入的資料即為新的 Rank LastProfession LastCharacter
        self.rank = records[0][3]
        self.last_profession = DBAccessor.execute('select Profession from Character where Nickname=' +
                                                  convert_datum_to_command(records[0][1])).fetchone()[0]
        self.last_character = records[0][1]

        # 當沒有 in 3weeks, in 2months 的資料時，使 raised 為 0 的處理
        self.rank_3_weeks_ago = records[0][3]
        self.rank_2_months_ago = records[0][3]

        for record in records:
            recorded_date = convert_str_to_date(record[0])
            if recorded_date > self.date_of_3_weeks:
                self.rank_3_weeks_ago = record[3]
            if recorded_date > self.date_of_2_months:
                self.rank_2_months_ago = record[3]
            if not record[1] in self.used_characters:
                self.used_characters[record[1]] = record[2]

        self._post_process()

    # 檢查一下的確有記錄需要處理
    @staticmethod
    def _pre_process(records):
        if len(records) == 0:
            raise ValueError('Zero record input!')

    def _post_process(self):
        self.raised_in_3_weeks = self.rank - self.rank_3_weeks_ago
        self.raised_in_2_months = self.rank - self.rank_2_months_ago
        self._status = RECORDED

    def update_into_memory_db(self):
        DBAccessor.execute('update FriendInfo{0}{1} where ID={2}'.format(
            get_db_suffix(), convert_data_to_update_command(
                self.FRIEND_INFO_UPDATED_COLUMNS, self.get_updated_info()), self.f_id))

    def get_updated_info(self):
        if self._status != RECORDED:
            raise Exception('Haven\'t call \'take_statistic\' yet!')

        used_characters_str = ', '.join([name + str(level) for name, level in self.used_characters.iteritems()])
        return [used_characters_str, self.rank, self.raised_in_3_weeks,
                self.raised_in_2_months, self.last_profession, self.last_character]
