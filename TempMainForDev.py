# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from ModelUtility.DataObject import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        a = u'海風之港'
        a = a.replace(u'海風之港', u'海風')
        print a


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

# popup = CharacterInfoWindow(1039)
# root.wait_window(popup)
