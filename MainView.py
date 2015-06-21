__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

from PySide import QtGui, QtCore
from droidsec_ui import Ui_MainWindow
from logger import Logger
from androguard.misc import *
from androguard.gui.apkloading import ApkLoadingThread

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
            Logger.log(Logger.ERROR,"Analysis of %s failed :(" % str(self.apkLoadingThread.apk_path))
            return

        self.a = self.apkLoadingThread.a
        self.d = self.apkLoadingThread.d
        self.x = self.apkLoadingThread.x

        self.load_app_info_table()
        self.load_permissions()
        self.__logger.log(Logger.INFO,"Analysis of %s done!" % str(self.apk.get_app_name()))
        self.set_loading_progressbar_disabled()

    def load_app_info_table(self):
        self.info = {}
        self.info["Application Name"]            = self.apk.get_app_name()
        self.info["Android Version Name"]        = self.apk.get_androidversion_name()
        self.info["Android Version Code"]        = self.apk.get_androidversion_code()
        self.info["Uses Dynamic Code Loading"]   = str(is_dyn_code(self.x))
        self.info["Uses Reflection"]             = str(is_reflection_code(self.x))
        self.info["Uses Crypto"]                 = str(is_crypto_code(self.x))
        self.info["Number of Activities"]        = str(len(self.apk.get_activities()))
        self.info["Number of Libraries"]         = str(len(self.apk.get_libraries()))

        self.info_actions = {}
        self.info_actions["Application Name"]            = None
        self.info_actions["Android Version Name"]        = None
        self.info_actions["Android Version Code"]        = None
        self.info_actions["Uses Dynamic Code Loading"]   = self.show_dyncode
        self.info_actions["Uses Reflection"]             = self.show_reflection
        self.info_actions["Uses Crypto"]                 = None
        self.info_actions["Number of Activities"]        = self.show_activities
        self.info_actions["Number of Libraries"]         = self.show_libraries
        info_table = self.ui.appInfoTable
        info_table.setRowCount(len(self.info))
        info_table.horizontalHeader().setStretchLastSection(True)
        row = 0
        for key in sorted(self.info):
            action = self.info_actions[key]
            action_item = None
            if action is not None:
                action_button = QtGui.QPushButton()
                action_button.setText("Show")
                action_button.clicked.connect(action)
            key_item = QtGui.QTableWidgetItem(key)
            value_item = QtGui.QTableWidgetItem(self.info[key])
            info_table.setItem(row,0,key_item)
            info_table.setItem(row,1,value_item)
            if action_item is not None:
                info_table.setCellWidget(row,3,action_button)
            row += 1

    def show_dyncode(self):
        self.__logger.log(Logger.INFO,"Dynamic Code Usage:"+show_DynCode(self.x))

    def show_reflection(self):
        self.__logger.log(Logger.INFO,"Dynamic Code Usage:"+show_DynCode(self.x))

    def show_activities(self):
        self.__logger.log(Logger.INFO,"Dynamic Code Usage:"+show_DynCode(self.x))

    def show_libraries(self):
        self.__logger.log(Logger.INFO,"Libraries Used: "+self.apk.get_libraries())

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
            self.set_loading_progressbar("Analyzing APK","Please wait while the APK is being dissected")
            self.__logger.log(Logger.INFO,"Analyzing %s..." % str(path))
            self.apk = apk.APK(path)
            self.manifest = self.apk.get_AndroidManifest().getElementsByTagName("manifest")[0]
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

    def set_loading_progressbar(self,title,text):
        self.dialog = QtGui.QProgressDialog(self)
        self.dialog.setMinimum(0)
        self.dialog.setLabelText(text)
        self.dialog.setMaximum(0)
        self.dialog.setWindowTitle(title)
        self.dialog.setCancelButton(None)
        self.dialog.setModal(True)
        self.dialog.show()


    def set_loading_progressbar_disabled(self):
        self.dialog.hide()
