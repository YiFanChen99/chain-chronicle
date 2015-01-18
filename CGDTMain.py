# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'
''' 根據 CCGameDBTW 進行處理 '''

import os
from configparser3 import configparser
from MainFrameNew.BaseFrame import *
from ModelUtility.CCGameDBTW import *

README_PATH = 'data\CCGameDBTW_Readme.txt'


class Main(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        master.title("ChainChronicle DB")
        self.set_table_place(34, 38)

        self.data_owner = CCGameDBTWDataOwner()
        self.__init_widgets()

    def __init_widgets(self):
        self.version = StringVar()
        label = Label(self, textvariable=self.version, width=20, font=(MS_JH, 11), relief=RIDGE)
        label.place(x=370, y=5)
        label.bind('<ButtonRelease-1>', self.updating_version)
        label.bind('<ButtonRelease-3>', lambda x: os.startfile(README_PATH))
        self.updating_version()

        button = Button(self, text='Insert', width=15, font=(MS_JH, 12))
        button.place(x=18, y=20)
        button['command'] = self.insert

        button = Button(self, text='Update', width=15, font=(MS_JH, 12))
        button.place(x=192, y=20)
        button['command'] = self.update

    # noinspection PyUnusedLocal
    def insert(self, event=None):
        inserter = MyDBUpdater(self.data_owner)

    # noinspection PyUnusedLocal
    def update(self, event=None):
        updater = MyDBUpdater(self.data_owner)
        # updater.update_belonged_info(overwrite=True)

    # noinspection PyUnusedLocal
    def updating_version(self, event=None):
        config_parser = configparser.ConfigParser()
        config_parser.read(README_PATH, "utf8")
        self.version.set('Ver. ' + config_parser.get('Version', u'目前版本'))


if __name__ == "__main__":
    root = Tk()
    root.geometry('580x300' + '+800+350')
    app = Main(master=root)
    app.mainloop()
