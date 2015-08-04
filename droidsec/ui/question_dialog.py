# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questionsample_dialog.ui'
#
# Created: Tue Aug  4 21:12:30 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_startDialog(object):
    def setupUi(self, startDialog):
        startDialog.setObjectName(_fromUtf8("startDialog"))
        startDialog.resize(527, 228)
        startDialog.setMinimumSize(QtCore.QSize(527, 228))
        startDialog.setMaximumSize(QtCore.QSize(527, 228))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        startDialog.setFont(font)
        self.label = QtGui.QLabel(startDialog)
        self.label.setGeometry(QtCore.QRect(130, 60, 271, 16))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.loadFileBtn = QtGui.QPushButton(startDialog)
        self.loadFileBtn.setGeometry(QtCore.QRect(130, 100, 101, 32))
        self.loadFileBtn.setObjectName(_fromUtf8("loadFileBtn"))
        self.loadDeviceBtn = QtGui.QPushButton(startDialog)
        self.loadDeviceBtn.setGeometry(QtCore.QRect(240, 100, 111, 32))
        self.loadDeviceBtn.setObjectName(_fromUtf8("loadDeviceBtn"))

        self.retranslateUi(startDialog)
        QtCore.QMetaObject.connectSlotsByName(startDialog)

    def retranslateUi(self, startDialog):
        startDialog.setWindowTitle(_translate("startDialog", "Choose Sample for Analysis", None))
        self.label.setText(_translate("startDialog", "Which sample do you want to analyse?", None))
        self.loadFileBtn.setText(_translate("startDialog", "File ...", None))
        self.loadDeviceBtn.setText(_translate("startDialog", "Device ...", None))

