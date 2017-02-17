# This file is part of ARES.
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

import os

from PyQt4 import QtGui, QtCore

from devicetable_ui import Ui_Form
from ares.core.logger import Logger
from dumpey import dumpey


class DeviceTable(QtGui.QDialog):

    def __init__(self, mainview, parent=None):
        super(DeviceTable, self).__init__(parent)
        self.ui = Ui_Form()
        self.mainview = mainview
        self.ui.setupUi(self)
        self.device_data = self.get_device_data()
        self.set_title("Choose an Android Device")
        self.ui.treeView.setEditTriggers(QtGui.QTableView.NoEditTriggers)
        self.ui.treeView.setAlternatingRowColors(True)
        self.ui.treeView.setSelectionMode(QtGui.QTableView.SingleSelection)
        self.ui.treeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.treeView.doubleClicked.connect(self.device_clicked)
        self.setup_filtering()
        self.show_data()

    def setup_filtering(self):
        self.filterPatternLineEdit = self.ui.lineEdit
        self.filterPatternLabel = QtGui.QLabel("&Filter string pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

    def filterRegExpChanged(self, value):
        regExp = QtCore.QRegExp(value)
        self.stringswindow.proxyModel.setFilterRegExp(regExp)

    def get_device_info_model(self):
        device_info = self.get_device_data()
        self.model = QtGui.QStandardItemModel(len(device_info), 2, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Device Id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Android API")
        row = 0

        for key in device_info:
            self.model.setData(self.model.index(row, 0, QtCore.QModelIndex()), str(key))
            self.model.setData(self.model.index(row, 1, QtCore.QModelIndex()), str(device_info[key]))
            row += 1

        self.proxyModel.setSourceModel(self.model)
        self.ui.treeView.setModel(self.proxyModel)

    def filterRegExpChanged(self, value):
        regExp = QtCore.QRegExp(value)
        self.proxyModel.setFilterRegExp(regExp)

    def set_header(self,header_id,text):
        self.ui.treeView.setHorizontalHeaderItem(header_id,QtGui.QTableWidgetItem(text))

    def show_data(self):
        self.get_device_info_model()

    def set_title(self,text):
        self.setWindowTitle(text)

    def get_device_data(self):
        data = {}
        for device in dumpey.attached_devices():
            data[device] = dumpey.api_version(device)
        return data

    def device_clicked(self, mi):
        mi = self.proxyModel.mapToSource(mi)
        row = mi.row()
        self.device = mi.model().item(row,0).text()
        self.close()
        self.show_package_dialog(self.device, dumpey.package_list([self.device]))

    def show_package_dialog(self,device,package_list):
        package_list = package_list[device]
        table = PackageWindow(device,package_list,win=self.mainview)
        table.exec_()


class PackageWindow(QtGui.QDialog):
    def __init__(self,device, package_list, parent=None, win=None):
        super(PackageWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.mainwin = win
        self.package_list = package_list
        self.device = device
        self.title = "Choose an application"

        self.filterPatternLineEdit = QtGui.QLineEdit()
        self.filterPatternLabel = QtGui.QLabel("&Filter packages:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)

        self.packagewindow = PackageValueWindow(self.device,self.package_list,win= self.mainwin,parent=self)

        sourceLayout = QtGui.QVBoxLayout()
        sourceLayout.addWidget(self.packagewindow)
        sourceLayout.addWidget(self.filterPatternLabel)
        sourceLayout.addWidget(self.filterPatternLineEdit)

        self.setLayout(sourceLayout)

    def filterRegExpChanged(self, value):
        regExp = QtCore.QRegExp(value)
        self.packagewindow.proxyModel.setFilterRegExp(regExp)

class PackageValueWindow(QtGui.QTreeView):
    def __init__(self, device, package_list,parent=None, win=None):
        super(PackageValueWindow, self).__init__(parent)
        self.mainview = win
        self.parent = parent
        self.package_list = package_list
        self.device = device
        self.title = "Choose an application"
        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.model = QtGui.QStandardItemModel(len(self.package_list), 1, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Applications")

        row = 0
        for package in self.package_list:
            self.model.setData(self.model.index(row, 0, QtCore.QModelIndex()), str(package))
            row += 1

        self.proxyModel.setSourceModel(self.model)
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setModel(self.proxyModel)
        self.setSortingEnabled(True)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.doubleClicked.connect(self.pull_package)

    def pull_package(self, mi):
        mi = self.proxyModel.mapToSource(mi)
        row = mi.row()
        package = mi.model().item(row,0).text()
        self.parent.close()
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory to save APK"))
        self.close()
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

