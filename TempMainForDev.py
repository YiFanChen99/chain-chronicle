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


        f_info = DBAccessor.select_specific_friend_info(2, 'JP')
        FriendInfoUpdaterWindow(self, f_info,
                                callback=lambda : None)

        # self.a = TableModelAdvance()
        # # self.a.set_columns(FriendInfo.DISPLAYED_COLUMNS, main_column='UsedNames')
        # self.a.set_columns(['1','2',u'我','4','5','6'])
        # self.tv = TableView(self)
        # self.tv.setModel(self.a)
        #
        # f_info = DBAccessor.select_friend_info_list('JP')[0]
        # print f_info
        #
        # # self.a.set_rows([f_info.get_displayed_info()])
        # self.a.set_rows([[1,2,3,'你',5,6]])
        #
        # self.tv.createTableFrame()
        # self.tv.redrawTable()
        # self.tv.adjustColumnWidths()
        # self.tv.bind('<Return>', lambda x:(self.the_print(), self.update()))

    def update(self):
        self.a.set_rows([[9, 3,6], [7, u'哈哈',666]])
        self.tv.createTableFrame()
        self.tv.redrawTable()
        self.tv.adjustColumnWidths()

    def the_print(self):
        print 1, 2, 5
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
