# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from Tkinter import *
from UIUtility.Combobox import *
from MainFrameNew.CharacterFrame import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        aa = FilterCombobox(self)
        aa['values'] = [1, 3, 5]
        aa.place(x=10, y=5)



if __name__ == "__main__":
    root = Tk()
    init_size = str(800) + 'x' + str(500)
    root.geometry(init_size + '+800+350')
    app = Main(root)
    app.mainloop()

# popup = CharacterInfoWindow(1039)
# root.wait_window(popup)
