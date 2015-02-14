# -*- coding: utf-8 -*-
from UI.MenuFrame import *


class Main(Frame):
    MAIN_FRAME_POS_Y = 68

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        self._current_width = MIN_WIDTH
        self._current_height = MIN_HEIGHT
        self.bind('<Configure>', lambda event: self.updating_width_and_height())

        self.main_frame = None
        self.sub_menu_frame = None
        self.menu_frame = MenuFrame(self)
        self.menu_frame.place(x=0, y=1)

    def change_sub_menu_frame(self, frame):
        if self.sub_menu_frame is not None:
            self.sub_menu_frame.destroy()

        self.sub_menu_frame = frame
        self.sub_menu_frame.place(x=0, y=34)

    def change_main_frame(self, frame):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = frame
        self.main_frame.place(x=0, y=self.MAIN_FRAME_POS_Y)
        self.adjust_size_of_main_frame()  # 根據現在版面設定大小

    def updating_width_and_height(self):
        if self.winfo_width() > MIN_WIDTH:
            self._current_width = self.winfo_width()
        else:
            self._current_width = MIN_WIDTH

        if self.winfo_height() > MIN_HEIGHT:
            self._current_height = self.winfo_height()
        else:
            self._current_height = MIN_HEIGHT

        self.adjust_size_of_main_frame()

    def adjust_size_of_main_frame(self):
        self.main_frame.adjust_size(self._current_width, self._current_height - self.MAIN_FRAME_POS_Y)


if __name__ == "__main__":
    root = Tk()
    init_size = str(MIN_WIDTH) + 'x' + str(MIN_HEIGHT)
    root.geometry(init_size + '+800+350')
    app = Main(master=root)
    app.mainloop()