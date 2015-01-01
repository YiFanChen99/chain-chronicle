# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from UIUtility.Selector import ProfessionSelector, RankSelector


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        self.win = ProfessionSelector(self, self.callback, height=43)
        self.win.place(x=10, y=30)

        self.win = RankSelector(self, self.callback, height=43)
        self.win.place(x=10, y=80)

    def callback(self, pro):
        print pro


if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

