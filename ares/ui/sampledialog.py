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

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

from PySide import QtGui
from PySide.QtGui import QMessageBox,QDialog
from question_dialog import Ui_startDialog
from dumpey import dumpey
import traceback,sys

class SampleDialog(QtGui.QDialog):

    def __init__(self, mainview, parent=None):
        super(SampleDialog, self).__init__(parent)
        self.ui = Ui_startDialog()
        self.mainview = mainview
        self.ui.setupUi(self)
        self.ui.loadFileBtn.clicked.connect(self.mainview.load_apk)
        self.ui.loadDeviceBtn.clicked.connect(self.load_device_action)

    def load_device_action(self):
        try:
            dumpey.attached_devices()
            self.mainview.load_apk_from_device()
        except Exception:
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            QMessageBox.warning(self, "Error", "No device has been detected. Are you sure an Android device is connected? Make sure adb is on your path.")
            return