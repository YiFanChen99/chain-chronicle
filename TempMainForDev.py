# -*- coding: utf-8 -*-
from Tkinter import *
from Window.FriendWindow import *
from ModelUtility.CommonState import *

class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        print None
        # record = [UNRECORDED, 25, u'大家好',
        #                                 u'戰士' , '', None, None, 3, u'強運']
        # print record
        # aa = FriendRecordUpdaterWindow(self, record)
        # self.wait_window(aa)
        # print record
        # self.selector = FriendInfoUpdaterWindow(self, 'CN', friend_id=26)

    def the_print(self):
        print 30
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
