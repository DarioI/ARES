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
from PySide import QtCore,QtGui
class XMLHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(XMLHighlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkMagenta)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        keywordPatterns = ["\\b?xml\\b", "/>", ">", "<"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        xmlElementFormat = QtGui.QTextCharFormat()
        xmlElementFormat.setFontWeight(QtGui.QFont.Bold)
        xmlElementFormat.setForeground(QtCore.Qt.green)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=[\s/>])"), xmlElementFormat))

        xmlAttributeFormat = QtGui.QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QtCore.Qt.blue)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\=)"), xmlAttributeFormat))

        self.valueFormat = QtGui.QTextCharFormat()
        self.valueFormat.setForeground(QtCore.Qt.red)

        self.valueStartExpression = QtCore.QRegExp("\"")
        self.valueEndExpression = QtCore.QRegExp("\"(?=[\s></])")

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.gray)
        self.highlightingRules.append(QtCore.QRegExp("<!--[^\n]*-->"), singleLineCommentFormat)

    def highlightBlock(self, text):

        for pattern, format in self.highlightingRules:

            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)

            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.valueStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.valueEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.valueEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength, self.valueFormat)

            startIndex = self.valueStartExpression.indexIn(text, startIndex + commentLength);

class ByteCodeHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(ByteCodeHighlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkMagenta)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)
        keywordPatterns = ["^#\s*<init>\s*\([^()]*\)[A-Z]$","#\s\w*","\(.*?\)","\(([A-Za-z0-9_]+)\)"]
        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat) for pattern in keywordPatterns]

        xmlElementFormat = QtGui.QTextCharFormat()
        xmlElementFormat.setFontWeight(QtGui.QFont.Bold)
        xmlElementFormat.setForeground(QtCore.Qt.green)
        bytecodeKeywords=["iget-object",
                          "iget","iput","throw",
                          "move","new-array",
                          "aput-object",
                          "invoke-virtual",
                          "move-result-object","invoke-direct",
                          "invoke-static","new-instance",
                          "invoke-interface"]
        for keyword in bytecodeKeywords:
            self.highlightingRules.append((QtCore.QRegExp(keyword), xmlElementFormat))

        constantsFormat2 = QtGui.QTextCharFormat()
        constantsFormat2.setFontWeight(QtGui.QFont.Bold)
        constantsFormat2.setForeground(QtCore.Qt.red)
        constantKeys=["\w+(?:-\w+)+"]
        for const in constantKeys:
            self.highlightingRules.append((QtCore.QRegExp(const),constantsFormat2))

        constantsFormat3 = QtGui.QTextCharFormat()
        constantsFormat3.setFontWeight(QtGui.QFont.Bold)
        constantsFormat3.setForeground(QtCore.Qt.darkGreen)
        constantKeys=["goto\s*","return-void","return-object","return"]
        for const in constantKeys:
            self.highlightingRules.append((QtCore.QRegExp(const),constantsFormat3))

        constantsFormat = QtGui.QTextCharFormat()
        constantsFormat.setFontWeight(QtGui.QFont.Bold)
        constantsFormat.setForeground(QtCore.Qt.darkYellow)
        constantKeys=["const","const-class","const-string"]
        for const in constantKeys:
            self.highlightingRules.append((QtCore.QRegExp(const),constantsFormat))

        self.valueStartExpression = QtCore.QRegExp("#")
        self.valueEndExpression = QtCore.QRegExp("\"(?=[\s></])")

    def highlightBlock(self, text):

        for pattern, format in self.highlightingRules:

            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)

            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
