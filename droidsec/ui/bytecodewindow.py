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

from PySide import QtGui,QtCore
from highlighter import ByteCodeHighlighter
from droidsec.core.constants import DEX_BYTECODE_SET

class BytecodeWindow(QtGui.QTextEdit):

    def __init__(self,bytecode,mainwin,parent=None):
        super(BytecodeWindow, self).__init__(parent)
        self.bytecode = bytecode
        self.mainwin = mainwin
        self.hl = ByteCodeHighlighter(self)
        self.setPlainText(str(self.bytecode).strip())
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.custom_contextmenu_handler)

    def custom_contextmenu_handler(self):
        menu = QtGui.QMenu(self)
        menu.addAction(QtGui.QAction("Bytecode lookup ...", self,
                statusTip="Get the description of the selected bytecode",
                triggered=self.action_bytecode_lookup))
        menu.exec_(QtGui.QCursor.pos())

    def action_bytecode_lookup(self):
        cursor = self.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        bytecode = cursor.selectedText()

        if bytecode not in DEX_BYTECODE_SET:
            self.mainwin.showStatus("Bytecode description not available. No info for: '%s'." % bytecode)
            return

        description = DEX_BYTECODE_SET[bytecode]

        self.mainwin.showStatus("Bytecode description: '%s'." % description)
