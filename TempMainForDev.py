# -*- coding: utf-8 -*-
from UI.MenuFrame import *
from ModelUtility.DBAccessor import *
from ModelUtility.DataObject import *
from ModelUtility.CommonState import *
from UI.DrawLots.DrawLotsFrame import *
from UI.DrawLots.EventOfDrawLotsWindow import *
from Model import DrawLotsModel
from Model import CharacterWeaponModel
from UI.MyCharacter.CharacterWeaponWindow import *



class Main(Frame):
    def __init__(self, master=None, width=MIN_WIDTH, height=MIN_HEIGHT):
        Frame.__init__(self, master, width=width, height=height)
        master.title("ChainChronicle")
        master.geometry('+%d+%d' % (
            root.winfo_screenwidth() - MIN_WIDTH - 21, root.winfo_screenheight() - MIN_HEIGHT - 80))
        self.pack(fill=BOTH, expand=1)

        set_account('Yama')
        cw = CharacterWeapon.create_empty_character_weapon()
        popup = CharacterWeaponWindow(self, cw, lambda: self.the_print(cw))
        popup.geometry('+%d+%d' % (
            root.winfo_screenwidth() - MIN_WIDTH - 21, root.winfo_screenheight() - MIN_HEIGHT - 80))
        self.wait_window(popup)

    def the_print(self, obj):
        print obj.nickname


if __name__ == "__main__":
    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = Main(root)
    app.mainloop()
