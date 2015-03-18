# -*- coding: utf-8 -*-
from UI.MenuFrame import *
from ModelUtility.DBAccessor import *
from ModelUtility.DataObject import *
from ModelUtility.CommonState import *
from UI.DrawLots.DrawLotsFrame import *
from UI.DrawLots.EventOfDrawLotsWindow import *
from Model import DrawLotsModel


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        set_account('Fuji')
        events = DrawLotsModel.select_event_list()
        a = EventWindow(self, events[2], None)
        a.geometry('+1000+500')
        # set_account('Yama')
        # a = DrawLotsFrame(self, bg='green')
        # a.place(x=0, y=0)


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
    init_size = str(760) + 'x' + str(460)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

# popup = CharacterInfoWindow(1039)
# root.wait_window(popup)
