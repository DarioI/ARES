# This file is part of DroidSec.
#
# Copyright (C) 2015, Dario Incalza <dario.incalza at gmail.com>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

from PySide.QtGui import QTableWidgetItem
from PySide import QtGui,QtCore


class ResourceFileController(object):

    def __init__(self,apk,filetable,viewer,fileinfotext):
        self.apk = apk;
        self.filetable  = filetable
        self.viewer     = viewer
        self.fileinfotext = fileinfotext
        self.setup_table()
        self.fill_table()

    def setup_table(self):
        self.filetable.setEditTriggers(QtGui.QTableView.NoEditTriggers)
        self.filetable.setAlternatingRowColors(True)
        self.filetable.setAutoScroll(True)
        self.filetable.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.filetable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.filetable.itemDoubleClicked.connect(self.file_clicked)

    def file_clicked(self,item):
        file = self.apk.get_file(str(item.text()))
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(file)
        scaledPixmap = pixmap.scaled(self.viewer.size(), QtCore.Qt.KeepAspectRatio)
        self.viewer.setPixmap(scaledPixmap)

    def fill_table(self):
        i = 0
        files = self.apk.get_files()
        self.filetable.setRowCount(len(files))
        for file in self.apk.get_files():
            if self.file_allowed(str(file).lower()):
                item = QTableWidgetItem(str(file))
                self.filetable.setItem(0,i,item)
                i+=1

    def file_allowed(self,file):
        if str(file).endswith("png"):
            return True

        if str(file).endswith("xml"):
            return True

        if str(file).endswith("jpg"):
            return True

        return False