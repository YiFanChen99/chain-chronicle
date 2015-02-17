# -*- coding: utf-8 -*-
import tkMessageBox
from datetime import timedelta, date
from ModelUtility.CommonState import *
from ModelUtility.DBAccessor import *
from ModelUtility.DataObject import RecordOfDrawLots, EventOfDrawLots
from UI.DrawLots.RecordOfDrawLotsWindow import AddingRecordWindow, UpdatingRecordWindow
from CharacterModel import select_character_by_specific_column


def select_record_list():
    return [_convert_selected_columns_to_record(each) for each in
            DBAccessor.execute('select {0} from RecordOfDrawLots where {1}'.format(
                ','.join(RecordOfDrawLots.SELECTED_COLUMNS), _get_account_condition())).fetchall()]


def _select_last_record():
    return _convert_selected_columns_to_record(DBAccessor.execute(
        'select {0} from RecordOfDrawLots where {1} and Times=(select max(Times) from RecordOfDrawLots where {1})'.
        format(','.join(RecordOfDrawLots.SELECTED_COLUMNS), _get_account_condition())).fetchone())


def _convert_selected_columns_to_record(columns):
    return RecordOfDrawLots([columns[0], columns[3]], select_specific_event(columns[1]),
                            select_character_by_specific_column('ID', columns[2]))


# 確認新增要求後，才新增至 DB 並通知 caller
def open_adding_new_record_window(master, events, limitation, callback):
    next_record = RecordOfDrawLots.create_new_record_by_last_one(_select_last_record())
    AddingRecordWindow(master, next_record, get_suitable_events(events, limitation), lambda added_record: (
        _insert_record_into_db(added_record), callback(added_record)))


def _insert_record_into_db(record):
    DBAccessor.execute('insert into RecordOfDrawLots({0}){1}'.format(
        ','.join(['Account'] + RecordOfDrawLots.UPDATED_COLUMNS),
        convert_data_to_insert_command(get_account(), *record.get_updated_info())))
    DBAccessor.commit()


# 確認更新要求後，才更新至 DB 並通知 caller
def open_updating_record_window(master, record, events, callback):
    UpdatingRecordWindow(master, record, events, lambda: (_update_record_into_db(record), callback()))


def _update_record_into_db(record):
    DBAccessor.execute('update RecordOfDrawLots{0} where {1} and Times={2}'.format(
        convert_data_to_update_command(
            RecordOfDrawLots.UPDATED_COLUMNS, record.get_updated_info()), _get_account_condition(), record.times))
    DBAccessor.commit()


# 確認刪除後，才從 DB 刪除並通知 caller
def delete_record_with_conforming(master, record, callback):
    if tkMessageBox.askyesno('Deleting', 'Are you sure you want to delete record times 「{0}」？'.format(
            record.times), parent=master):
        DBAccessor.execute('delete from RecordOfDrawLots where {0} and Times={1}'.format(
            _get_account_condition(), record.times))
        DBAccessor.commit()
        callback()


def select_event_list():
    return [EventOfDrawLots(each) for each in
            DBAccessor.execute('select {0} from EventOfDrawLots where {1} order by StartedDay desc, ID desc'.format(
                ','.join(EventOfDrawLots.SELECTED_COLUMNS), _get_server_condition())).fetchall()]


def select_specific_event(e_id):
    return EventOfDrawLots(DBAccessor.execute('select {0} from EventOfDrawLots where ID={1} and {2}'.format(
        ','.join(EventOfDrawLots.SELECTED_COLUMNS), e_id, _get_server_condition())).fetchone())


# 若有要求只顯示恰當的酒廠，則會計算結束日期滿足條件才會加入
def get_suitable_events(events, limitation):
    event_duration_tolerance = 2
    if limitation:
        return [event for event in events
                if event.is_suitable_duration(date.today() - timedelta(days=event_duration_tolerance))]
    else:
        return events


def _get_account_condition():
    return 'Account=' + convert_datum_to_command(get_account())


def _get_server_condition():
    return 'Server=' + convert_datum_to_command(get_server())