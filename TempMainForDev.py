# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Window.CharacterWindow import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        ss = StringVar()
        popup = CharacterSelectionWindow(self, ss.set, DBAccessor.select_character_by_specific_column('ID', 5002))
        popup.geometry('+732+270')
        self.wait_window(popup)
        print ss.get()
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
