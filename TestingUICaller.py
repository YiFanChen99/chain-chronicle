# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from Window import CharacterSelectionWindow


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        self.win = CharacterSelectionWindow.CharacterSelectionWindow(None)
        self.wait_window(self.win)


    def callback(self, pro):
        print pro


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

