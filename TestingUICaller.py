# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Window.CharacterWindow import CharacterSelectionWindow
from ModelUtility.DBAccessor import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        # self.win = CharacterSelectionWindow(None)
        # self.wait_window(self.win)



        print DBAccessor.execute('select FriendID, min(RecordedDate) from FriendRecordJP').fetchall()
        # t2command = ' where FriendID = (select FriendID from FriendRecordJP where FriendID=3)'
        # t2command = ''
        # t2command = ' where FriendID = (select FriendID, RecordedDate from FriendRecordJP where (RecordedDate in min(RecordedDate)))'
        # date = convert_str_to_datetime(
        #     DBAccessor.execute('select FriendID, max(RecordedDate) from FriendRecordJP' + t2command).fetchone()[0])
        aa= 'select max({2}) from {0} where {1} = (select {1} from {0} where {2} = (select min({2}) from {0}))'.format('FriendRecordJP', 'FriendID', 'RecordedDate')
        print DBAccessor.execute(aa).fetchone()[0]



    def callback(self, pro):
        print pro


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

