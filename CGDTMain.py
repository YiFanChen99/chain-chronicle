# -*- coding: utf-8 -*-
__author__ = 'Ricky Chen'
''' 根據 CCGameDBTW 進行處理 '''

import os
from configparser3 import configparser
from MainFrameNew.BaseFrame import *
from Model.CCGameDBTWModel import *

README_PATH = 'data\CCGameDBTW_Readme.txt'


class Main(MainFrameWithTable):
    def __init__(self, master, **kwargs):
        MainFrameWithTable.__init__(self, master, **kwargs)
        master.title("ChainChronicle DB")
        self.set_table_place(34, 38)

        self.data_owner = CCGameDBTWDataOwner()
        self._init_widgets()

    def _init_widgets(self):
        self.version = StringVar()
        label = Label(self, textvariable=self.version, width=20, font=(MS_JH, 11), relief=RIDGE)
        label.place(x=370, y=5)
        label.bind('<ButtonRelease-1>', lambda event: self.update_version())
        label.bind('<ButtonRelease-3>', lambda event: os.startfile(README_PATH))
        self.update_version()

        button = Button(self, text='Insert', width=15, font=(MS_JH, 12))
        button.place(x=18, y=20)
        button['command'] = lambda: self.insert()

        button = Button(self, text='Update', width=15, font=(MS_JH, 12))
        button.place(x=192, y=20)
        button['command'] = lambda: self.update()

        button = Button(self, text='TempMethod', width=15, font=(MS_JH, 12))
        button.place(x=105, y=65)
        button['command'] = lambda: self.executeTemp()

    def insert(self):
        inserter = MyDBInserter(self, self.data_owner)
        inserter.insert_new_characters()

    def update(self):
        updater = MyDBUpdater(self, self.data_owner)
        updater.update_new_characters()

    def executeTemp(self):
        updater = MyDBUpdater(self, self.data_owner)
        updater.update_new_characters()

    def update_version(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(README_PATH, "utf8")
        self.version.set('Ver. ' + config_parser.get('Version', u'目前版本'))


if __name__ == "__main__":
    root = Tk()
    root.geometry('580x300' + '+800+350')
    app = Main(master=root)
    app.mainloop()
