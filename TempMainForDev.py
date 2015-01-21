# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from ModelUtility.DataObject import *
from Window.CharacterWindow import CharacterInfoWindow
from Window.BasicWindow import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        popup = BasicWindow(self, width=300, height=600)

        helpText=Label(popup,text="Help")
        helpText.place(x=10, y=10)
        print 'aa'
        root.wait_window(popup)
        print 'bb'
        print 'cc'
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
