__author__ = 'Dario Incalza'

from PySide import QtCore,QtGui

class CustomTabBar(QtGui.QTabBar):
    '''Subclass QTabBar to implement middle-click closing of tabs'''

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.tabCloseRequested.emit(self.tabAt(event.pos()))
        super(QtGui.QTabBar, self).mouseReleaseEvent(event)
