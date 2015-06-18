__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

from PySide import QtGui, QtCore
from droidsec_ui import Ui_MainWindow
from logger import Logger
from androguard.misc import *
from androguard.gui.apkloading import ApkLoadingThread
from treewindow import TreeWindow

class MainView(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__logger = Logger(self.ui.logArea)
        self.__logger.log(Logger.INFO, "### DroidSec - dev version 0.01 ###")
        self.init_actions()
        self.setupApkLoading()
        self.init_UI()
        self.apk_path = ''
        self.apk = None
        self.x = self.d = self.a = None
        self.manifest = None

    def init_UI(self):
        pass

    def setupApkLoading(self):
        self.apkLoadingThread = ApkLoadingThread()
        self.connect(self.apkLoadingThread, QtCore.SIGNAL("loadedApk(bool)"), self.loadedApk)

    def loadedApk(self, success):
        if not success:
            Logger.log(Logger.WARNING,"Analysis of %s failed :(" %
                    str(self.apkLoadingThread.apk_path))
            return

        self.a = self.apkLoadingThread.a
        self.d = self.apkLoadingThread.d
        self.x = self.apkLoadingThread.x

        self.setupTree()

        Logger.log(Logger.INFO,"Analysis of %s done!" %
                str(self.apkLoadingThread.apk_path))

    def setupTree(self):
        tree_helper = TreeWindow(self.ui.treeWidget)
        self.ui.treeWidget.setWindowTitle("Tree Model")
        tree_helper.fill(self.d.get_classes())

    def init_actions(self):
        self.ui.chooseAPKBtn.clicked.connect(self.load_apk)
        self.ui.saveLogBtn.clicked.connect(self.__logger.saveLog)
        self.ui.clearLogBtn.clicked.connect(self.__logger.clearLog)

    def load_apk(self,path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    '', "APK Files (*.apk);;Androguard Session (*.ag)")
            path = str(path[0])

        if path:
            self.__logger.log(Logger.INFO,"Analyzing %s..." % str(path))
            self.apkLoadingThread.load(path)

    def load_permissions(self):
        perms = self.get_uses_permissions()
        self.ui.permsTable.setRowCount(len(perms))
        self.ui.permsTable.horizontalHeader().setStretchLastSection(True)
        for i, uses_permission in enumerate(perms):
            newitem = QtGui.QTableWidgetItem(uses_permission)
            self.ui.permsTable.setItem(0, i, newitem)

    def get_uses_permissions(self):
        permissions = []
        for uses_permission in self.manifest.getElementsByTagName("uses-permission"):
            permissions.append(uses_permission.attributes["android:name"].value)
        return permissions

