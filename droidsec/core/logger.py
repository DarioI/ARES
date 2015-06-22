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

'''

This class enables the software to log every action the users perform in the program. For now three distinctions are made, Info, warning or error
messages.

@author: Incalza Dario
'''

from datetime import datetime

from PySide.QtGui import QColor
from PySide import QtGui


class Logger(object):
    INFO        = 0x0
    WARNING     = 0x1
    ERROR       = 0x2
    MAGENTA     = 0x3

    def __init__(self, console):
        self.__console = console
        self.__console.setTextBackgroundColor(QColor(0, 0, 0))

    '''
    Log a text to inform the user of a certain IO action. Given : the text that needs to be displayed. A timestamp will be printed before the text.
    '''

    def log(self, level, text):
        if level == 0x0:
            color = QColor(124, 252, 0)
            prefix = ' - [Info]'
        elif level == 0x1:
            color = QColor(255, 140, 0)
            prefix = ' - [Warning]'
        else:
            color = QColor(253, 0, 0)
            prefix = ' - [Error]'
        self.__console.setTextColor(color)
        now = datetime.now()
        time = str(now.strftime("%H:%M"))
        self.__console.append(time + prefix + " >> " + text)
        sb = self.__console.verticalScrollBar()
        sb.setValue(sb.maximum())
        QtGui.QApplication.processEvents()

    def log_with_color(self, level, text):
        if level == 0x0:
            color = QColor(124, 252, 0)
        elif level == 0x1:
            color = QColor(255, 140, 0)
        else:
            color = QColor(253, 0, 0)
        self.__console.setTextColor(color)
        self.__console.append(text)
        sb = self.__console.verticalScrollBar()
        sb.setValue(sb.maximum())
        QtGui.QApplication.processEvents()

    def log_with_title(self, title, text):

        color = QColor(124, 252, 0)
        magenta = QColor(255, 0, 255)
        self.__console.setTextColor(magenta)

        self.__console.append("\n==================================================================\n")
        self.__console.append("\t\t"+title+"\n")
        self.__console.append("==================================================================\n")
        self.__console.setTextColor(color)
        self.__console.append(text)
        sb = self.__console.verticalScrollBar()
        sb.setValue(sb.maximum())
        QtGui.QApplication.processEvents()

    def clearLog(self):

        self.__console.clear()
        self.log(Logger.INFO, "### DroidSec - dev version 0.01 ###")

    def saveLog(self):

        filename = "droidsec_log_" + str(datetime.now().strftime("%d%m%y-%H%M"))
        path = QtGui.QFileDialog.getSaveFileName(None, "Open file", filename, ".txt")
        if path == '':
            return
        path_str = ''.join(path)
        text_file = open(path_str, "w")
        text_file.write(self.__console.toPlainText())
        text_file.close()
        self.log(Logger.INFO, "Log saved succesfully in " + path_str)
