# -*- coding: utf-8 -*-
from Tkinter import *
from Window.FriendWindow import *
from MainFrameNew.FriendFrame import FriendRecordFrame
from MainFrameNew.BaseFrame import TableModelAdvance, TableView
from ModelUtility.CommonState import *
from ModelUtility.Filter import FilterRuleManager



class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        DB_TABLE = ['ID', 'UsedNames', 'Excellence', 'Defect', 'Relation', 'Offline', 'UsedCharacters', 'Rank',
                'RaisedIn3Weeks', 'RaisedIn2Months', 'AddedDate', 'LastProfession', 'LastCharacter']
        result = DB_TABLE[1:3]
        print result
        # tv = TableView(self)
        # a = TableModelAdvance()
        # a.set_columns(['I', 'you', 'she'])
        # # a.addRow(I=10, she=3,you=9)
        # a.set_Rows([])
        # # a.set_Rows([[9, 3,6], [7, u'哈哈',666]])
        #
        # tv.setModel(a)
        # tv.createTableFrame()
        # tv.redrawTable()
        # tv.adjustColumnWidths()

    def the_print(self):
        return 1, 2, 5
        # popup.mainloop()
        # popup = BasicWindow1(self, width=30 , height=60)
        # popup.transient(self)
        # popup.focus()
        #
        # root.wait_window(popup)
        # popup = BasicWindow1(self, width=30 , height=60)
        # root.wait_window(popup)


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

# popup = CharacterInfoWindow(1039)
# root.wait_window(popup)
