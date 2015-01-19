# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from ModelUtility.DataObject import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        ch = Character()
        # print ch.records
        ch.c_id = 5002
        print ch
        # ch.c_id = '80'
        # print ch.c_id
        # ch.c_id = None
        # print ch.c_id
        # ch.c_id = '901'
        # print ch.c_id


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

# popup = CharacterInfoWindow(1039)
# root.wait_window(popup)
