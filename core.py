__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

import sys
from PyQt4 import QtGui
from MainView import MainView

if __name__ == '__main__':
    sys.setrecursionlimit(50000)
    app = QtGui.QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec_())