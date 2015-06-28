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

__author__ = 'Dario Incalza <dario.incalza@gmail.com>'

from PySide import QtGui, QtCore

from dumpey import dumpey
import util
from droidsec.ui.ui_utils import CustomTabBar
from droidsec.ui.droidsec_ui import Ui_MainWindow
from logger import Logger
from androguard.misc import *
from androguard.gui.apkloading import ApkLoadingThread
from androguard.gui.treewindow import TreeWindow
from androguard.gui.sourcewindow import SourceWindow
from droidsec.ui.devicetable import DeviceTable


class MainView(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__logger = Logger(self.ui.logArea)
        self.__logger.log(Logger.INFO, "### DroidSec - dev version 0.01 ###")
        self.init_actions()
        self.setupApkLoading()
        self.apk_path = ''
        self.apk = None
        self.x = self.d = self.a = None
        self.manifest = None

    def get_logger(self):
        return self.__logger;

    def setupApkLoading(self):
        self.apkLoadingThread = ApkLoadingThread()
        self.connect(self.apkLoadingThread, QtCore.SIGNAL("loadedApk(bool)"), self.loadedApk)

    def loadedApk(self, success):
        if not success:
            self.__logger.log(Logger.ERROR,"Analysis of %s failed :(" % str(self.apkLoadingThread.apk_path))
            self.set_loading_progressbar_disabled()
            return

        self.a = self.apkLoadingThread.a
        self.d = self.apkLoadingThread.d
        self.x = self.apkLoadingThread.x

        self.setupTree(self.d.get_classes())
        self.load_app_info_table()
        self.load_permissions()
        self.__logger.log(Logger.INFO,"Analysis of %s done!" % str(self.apk.get_app_name()))
        self.ui.loadedAPK_label.setText("Loaded: "+str(self.apk.get_app_name()))
        self.set_loading_progressbar_disabled()

    def disable_apk_loading_buttons(self):
        self.ui.chooseAPKBtn.setDisabled(True)
        self.ui.btnFromDevice.setDisabled(True)

    def setupTree(self,classes):
        try:
            self.ui.tree_area.layout().deleteLater()
        except AttributeError:
            pass
        self.tree = TreeWindow(self,self)
        self.tree.setWindowTitle("Tree model")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tree)
        self.ui.tree_area.setLayout(layout)
        self.tree.fill(classes)
        self.setupCentral()

    def setupCentral(self):
        self.central = QtGui.QTabWidget()
        self.central.setTabBar(CustomTabBar())
        self.central.setTabsClosable(True)
        self.central.tabCloseRequested.connect(self.tabCloseRequestedHandler)
        self.central.currentChanged.connect(self.currentTabChanged)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.central)
        self.ui.sourceTextWidget.setLayout(layout)

    def tabCloseRequestedHandler(self, index):
        self.central.removeTab(index)

    def currentTabChanged(self, index):
        if index == -1:
            return # all tab closed

    def openSourceWindow(self, path, method=""):
        '''Main function to open a .java source window
           It checks if it already opened and open that tab,
           otherwise, initialize a new window.
        '''
        sourcewin = self.getMeSourceWindowIfExists(path)
        if not sourcewin:
            sourcewin = SourceWindow(win=self, path=path)
            sourcewin.reload_java_sources()
            self.central.addTab(sourcewin, sourcewin.title)
            self.central.setTabToolTip(self.central.indexOf(sourcewin), sourcewin.path)
        if method:
            sourcewin.browse_to_method(method)
        self.central.setCurrentWidget(sourcewin)

    def getMeSourceWindowIfExists(self, path):
        '''Helper for openSourceWindow'''
        for idx in range(self.central.count()):
            if path == self.central.tabToolTip(idx):
                return self.central.widget(idx)
        return None

    def load_app_info_table(self):
        self.info = {}
        self.info["Application Name"]            = self.apk.get_app_name()
        self.info["Application Size"]            = util.sizeof_fmt(os.path.getsize(self.apk_path))
        self.info["Android Version Name"]        = self.apk.get_androidversion_name()
        self.info["Android Version Code"]        = self.apk.get_androidversion_code()
        self.info["Android Package Name"]        = self.apk.get_package()
        self.info["Uses Dynamic Code Loading"]   = str(is_dyn_code(self.x))
        self.info["Uses Reflection"]             = str(is_reflection_code(self.x))
        self.info["Uses Crypto"]                 = str(is_crypto_code(self.x))
        self.info["Number of Activities"]        = str(len(self.apk.get_activities()))
        self.info["Number of Libraries"]         = str(len(self.apk.get_libraries()))
        self.info["Number of Permissions"]       = str(len(self.get_uses_permissions()))

        self.info_actions = {}
        self.info_actions["Application Name"]            = None
        self.info_actions["Application Size"]            = None
        self.info_actions["Android Version Name"]        = None
        self.info_actions["Android Version Code"]        = None
        self.info_actions["Android Package Name"]        = None
        self.info_actions["Uses Dynamic Code Loading"]   = self.show_dyncode
        self.info_actions["Uses Reflection"]             = self.show_reflection
        self.info_actions["Uses Crypto"]                 = self.show_cryptocode
        self.info_actions["Number of Activities"]        = self.show_activities
        self.info_actions["Number of Libraries"]         = self.show_libraries
        self.info_actions["Number of Permissions"]       = self.show_permissions
        info_table = self.ui.appInfoTable
        info_table.setRowCount(len(self.info))
        info_table.setColumnWidth(1, 200)
        info_table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        row = 0
        for key in sorted(self.info):
            action = self.info_actions[key]
            action_button = None
            if action is not None:
                action_button = QtGui.QPushButton()
                action_button.setText("Show")
                action_button.clicked.connect(action)
            key_item = QtGui.QTableWidgetItem(key)
            value_item = QtGui.QTableWidgetItem(self.info[key])
            info_table.setItem(row,0,key_item)
            info_table.setItem(row,1,value_item)
            if action_button is not None:
                info_table.setCellWidget(row,2,action_button)
            row += 1

    def show_permissions(self):
        self.__logger.log(Logger.INFO,"Searching for permission usage, this can take a while depending on the size of the app.")
        p = self.x.get_permissions( [] )
        str_perms=""
        self.__logger.log_with_title("Permissions Usage","")
        for i in p:
            self.__logger.log_with_color(Logger.WARNING,"\n\t======="+i+"=======\n")
            for j in p[i]:
                self.__logger.log_with_color(Logger.INFO,"\t\t -"+self.show_Path(self.x.get_vm(), j )+"\n")

    def show_cryptocode(self):
        if is_crypto_code(self.x) is False:
            self.__logger.log(Logger.WARNING,"No crypto code was found!")
            return

        paths = []

        paths.extend(self.x.get_tainted_packages().search_methods("Ljavax/crypto/.",
                                                ".",
                                                "."))

        paths.extend(self.x.get_tainted_packages().search_methods("Ljava/security/spec/.",
                                                    ".",
                                                    "."))

        str_info_dyn="\t"
        for path in paths:
            str_info_dyn += (self.show_Path(self.x.get_vm(), path )+"\n\n\t")
        self.__logger.log_with_title("Usage of Crypto Code",str_info_dyn)

    def show_dyncode(self):
        if is_dyn_code(self.x) is False:
            self.__logger.log(Logger.WARNING,"No dynamic code was found!")
            return

        paths = []
        paths.extend(self.x.get_tainted_packages().search_methods("Ldalvik/system/BaseDexClassLoader;",
                                                    "<init>",
                                                    "."))

        paths.extend(self.x.get_tainted_packages().search_methods("Ldalvik/system/PathClassLoader;",
                                                    "<init>",
                                                    "."))

        paths.extend(self.x.get_tainted_packages().search_methods("Ldalvik/system/DexClassLoader;",
                                                    "<init>",
                                                    "."))

        paths.extend(self.x.get_tainted_packages().search_methods("Ldalvik/system/DexFile;",
                                                    "<init>",
                                                    "."))

        paths.extend(self.x.get_tainted_packages().search_methods("Ldalvik/system/DexFile;",
                                                    "loadDex",
                                                    "."))
        str_info_dyn="\t"
        for path in paths:
            str_info_dyn += (self.show_Path(self.x.get_vm(), path )+"\n\n\t")
        self.__logger.log_with_title("Usage of Dynamic Code",str_info_dyn)

    def show_reflection(self):
        if is_reflection_code(self.x) is False:
            self.__logger.log(Logger.WARNING,"No reflection code was found!")
            return
        paths = self.x.get_tainted_packages().search_methods("Ljava/lang/reflect/Method;", ".", ".")
        str_info_reflection=""
        for path in paths:
            str_info_reflection += (self.show_Path(self.x.get_vm(), path )+"\n\n\t")
        self.__logger.log_with_title("Usage of Reflection",str_info_reflection)

    def show_activities(self):
        self.__logger.log_with_title("Activities",'\n\t -'+'\n\t -'.join(self.apk.get_activities()))

    def show_libraries(self):
        if len(self.apk.get_libraries()) == 0:
            self.__logger.log(Logger.WARNING,"No libraries were found.")
            return
        self.__logger.log(Logger.INFO,"Libraries Used: "+str(self.apk.get_libraries()))

    def init_actions(self):

        self.ui.chooseAPKBtn.clicked.connect(self.load_apk)
        self.ui.btnFromDevice.clicked.connect(self.load_apk_from_device)
        self.ui.saveLogBtn.clicked.connect(self.__logger.saveLog)
        self.ui.clearLogBtn.clicked.connect(self.__logger.clearLog)

    def load_apk_from_device(self):
        try:
            dumpey.attached_devices()
        except Exception:
            self.__logger.log(Logger.ERROR,"No device has been detected. Are you sure an Android device is connected?"+
                                           " Make sure adb is on your path.")
            return
        table = DeviceTable(self)
        table.exec_()

    def load_apk(self,path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    '', "APK Files (*.apk);;Androguard Session (*.ag)")
            path = str(path[0])
        self.apk_path = path
        if path:
            self.set_loading_progressbar("Analyzing APK","Please wait while the APK is being dissected")
            self.__logger.log(Logger.INFO,"Analyzing %s..." % str(path))
            self.apk = apk.APK(path)
            self.manifest = self.apk.get_AndroidManifest().getElementsByTagName("manifest")[0]
            self.apkLoadingThread.load(path)
            self.disable_apk_loading_buttons()

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

    def show_Path(self,vm, path):
      cm = vm.get_class_manager()

      if isinstance(path, PathVar):
        dst_class_name, dst_method_name, dst_descriptor =  path.get_dst( cm )
        info_var = path.get_var_info()
        return  "%s %s (0x%x) ---> %s->%s%s " % (path.get_access_flag(),
                                              info_var,
                                              path.get_idx(),
                                              dst_class_name,
                                              dst_method_name,
                                              dst_descriptor)
      else:
        if path.get_access_flag() == TAINTED_PACKAGE_CALL:
          src_class_name, src_method_name, src_descriptor =  path.get_src( cm )
          dst_class_name, dst_method_name, dst_descriptor =  path.get_dst( cm )

          return "%d %s->%s%s (0x%x) ---> %s->%s%s" % (path.get_access_flag(),
                                                      src_class_name,
                                                      src_method_name,
                                                      src_descriptor,
                                                      path.get_idx(),
                                                      dst_class_name,
                                                      dst_method_name,
                                                      dst_descriptor)
        else:
          src_class_name, src_method_name, src_descriptor =  path.get_src( cm )
          return "%d %s->%s%s (0x%x)" % (path.get_access_flag(),
                                        src_class_name,
                                        src_method_name,
                                        src_descriptor,
                                        path.get_idx())


