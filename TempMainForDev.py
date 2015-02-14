# -*- coding: utf-8 -*-
from UI.MenuFrame import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        self.sub_menu_frame = None
        self.main_frame = None
        s = MenuFrame(self)
        s.place(x=0, y=1)

    def change_sub_menu_frame(self, frame):
        if self.sub_menu_frame is not None:
            self.sub_menu_frame.destroy()

        self.sub_menu_frame = frame
        self.sub_menu_frame.place(x=0, y=34)

    def change_main_frame(self, frame):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = frame
        self.main_frame.place(x=0, y=68)

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
