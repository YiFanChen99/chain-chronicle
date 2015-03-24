# -*- coding: utf-8 -*-
from UI.MenuFrame import *


class Main(Frame):
    MAIN_FRAME_POS_Y = 68

    def __init__(self, master, width=MIN_WIDTH, height=MIN_HEIGHT, **kwargs):
        Frame.__init__(self, master, width=width, height=height, **kwargs)
        master.title("ChainChronicle")
        master.geometry('+%d+%d' % (  # Location
            root.winfo_screenwidth() - MIN_WIDTH - 21, root.winfo_screenheight() - MIN_HEIGHT - 80))
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
    root.columnconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    app = Main(master=root)
    app.mainloop()
