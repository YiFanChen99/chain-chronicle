# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'

from MenuFrame import *


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("ChainChronicle")
        self.pack(fill=BOTH, expand=1)

        self.__current_width = MIN_WIDTH
        self.__current_height = MIN_HEIGHT
        self.bind('<Configure>', self.do_update_width_and_height)

        self.main_frame = None
        self.sub_menu_frame = None
        self.menu_frame = MenuFrame(self, height=31)
        self.menu_frame.place(x=0, y=1)

    def update_sub_menu_frame(self, sub_menu_frame):
        if self.sub_menu_frame is not None:
            self.sub_menu_frame.destroy()

        self.sub_menu_frame = sub_menu_frame
        self.sub_menu_frame.place(x=0, y=34)

    def update_main_frame(self, main_frame):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = main_frame
        self.main_frame.place(x=0, y=67)

    # TODO
    # noinspection PyUnusedLocal
    def do_update_width_and_height(self, event=None):
        if self.winfo_width() > MIN_WIDTH:
            self.__current_width = self.winfo_width()
        else:
            self.__current_width = MIN_WIDTH

        if self.winfo_height() > MIN_HEIGHT:
            self.__current_height = self.winfo_height()
        else:
            self.__current_height = MIN_HEIGHT

        self.adjust_size_of_sub_main_frame()

    # TODO
    def adjust_size_of_sub_main_frame(self):
        pass
        # widget_width = self.__current_width - 8
        # widget_height = self.__current_height - 59
        # self.note_book['width'] = widget_width
        # self.note_book['height'] = widget_height
        # for each_tab in self.tabs:
        #     each_tab.adjust_view(widget_width, widget_height)

if __name__ == "__main__":
    root = Tk()
    init_size = str(MIN_WIDTH) + 'x' + str(MIN_HEIGHT)
    root.geometry(init_size + '+510+265')
    app = Main(master=root)
    app.mainloop()