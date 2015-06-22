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

__author__ = 'Dario Incalza'

from PySide import QtGui, QtCore
from devicewindow_ui import Ui_Dialog
import os
from droidsec.core.logger import Logger
from dumpey import dumpey


class DeviceTable(QtGui.QDialog):

    def __init__(self, mainview, parent=None):
        super(DeviceTable, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.mainview = mainview
        self.ui.setupUi(self)
        self.device_data = self.get_device_data()
        self.fill_table(self.device_data)
        self.ui.tableWidget.setWindowTitle("Choose an Android Device")
        self.ui.tableWidget.itemDoubleClicked.connect(self.device_clicked)

    def get_device_data(self):
        data = {}
        for device in dumpey.attached_devices():
            data[device] = dumpey.api_version(device)
        return data

    def device_clicked(self, tableItem):
        self.device = self.ui.tableWidget.itemAt(tableItem.row(), 0).text()
        self.ui.tableWidget.hide()
        self.show_package_list(self.device, dumpey.package_list([self.device]))

    def fill_table(self, data):
        row = 0
        self.ui.tableWidget.setRowCount(len(data))
        for key in data:
            key_item = QtGui.QTableWidgetItem(key)
            value_item = QtGui.QTableWidgetItem(data[key])
            self.ui.tableWidget.setItem(row, 0, key_item)
            self.ui.tableWidget.setItem(row, 1, value_item)
            row += 1

    def show_package_list(self, device, package_list):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        self.ui.tableWidget.setGeometry(QtCore.QRect(10, 10, 381, 221))
        self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setWindowTitle("Choose an installed app")
        item = QtGui.QTableWidgetItem("Installed Apps")
        self.ui.tableWidget.setHorizontalHeaderItem(0, item)
        row = 0
        self.ui.tableWidget.setRowCount(len(package_list[device]))
        for package in package_list[device]:
            item = QtGui.QTableWidgetItem(str(package))
            self.ui.tableWidget.setItem(row, 0, item)
            row += 1
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.itemDoubleClicked.disconnect()
        self.ui.tableWidget.itemDoubleClicked.connect(self.pull_package)
        self.ui.tableWidget.show()

    def pull_package(self, tableItem):
        package = tableItem.text()
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory to save APK"))
        self.hide()
        if file is not None:
            print "Pulling apk in : "+file
            self._pull_apk(package, self.device, file)

    def _pull_apk(self,package, device, local_dir):
        self.mainview.get_logger().log(Logger.INFO,"Please wait, APK is dumped from "+device)
        paths = dumpey.adb(['shell', 'pm', 'path', package], device, dumpey._decor_package)
        path = paths[0]
        name = dumpey._generate_name(device, os.path.basename(path), "apk")
        local = os.path.join(local_dir, name)
        dumpey.pull(path, local, device)
        self.mainview.get_logger().log(Logger.INFO,"APK dumped succesfully: "+local)
        self.mainview.load_apk(local)
