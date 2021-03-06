# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Config.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Config(object):
    def setupUi(self, Config):
        Config.setObjectName("Config")
        Config.setWindowModality(QtCore.Qt.ApplicationModal)
        Config.resize(241, 142)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        Config.setFont(font)
        Config.setModal(False)
        self.gridLayout_2 = QtWidgets.QGridLayout(Config)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnSaveConfig = QtWidgets.QPushButton(Config)
        self.btnSaveConfig.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.btnSaveConfig.setFont(font)
        self.btnSaveConfig.setObjectName("btnSaveConfig")
        self.horizontalLayout_2.addWidget(self.btnSaveConfig)
        self.btnCancel = QtWidgets.QPushButton(Config)
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.btnCancel.setFont(font)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.stkWidget = QtWidgets.QStackedWidget(Config)
        self.stkWidget.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        self.stkWidget.setFont(font)
        self.stkWidget.setMouseTracking(False)
        self.stkWidget.setTabletTracking(False)
        self.stkWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stkWidget.setObjectName("stkWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ccBoxSaveDesktop = QtWidgets.QCheckBox(self.page)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ccBoxSaveDesktop.setFont(font)
        self.ccBoxSaveDesktop.setChecked(False)
        self.ccBoxSaveDesktop.setObjectName("ccBoxSaveDesktop")
        self.verticalLayout_4.addWidget(self.ccBoxSaveDesktop)
        self.lineEdFilePath = QtWidgets.QLineEdit(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdFilePath.sizePolicy().hasHeightForWidth())
        self.lineEdFilePath.setSizePolicy(sizePolicy)
        self.lineEdFilePath.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdFilePath.setObjectName("lineEdFilePath")
        self.verticalLayout_4.addWidget(self.lineEdFilePath)
        self.stkWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.lineEdShortcutSlice = QtWidgets.QLineEdit(self.page_2)
        self.lineEdShortcutSlice.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdShortcutSlice.setObjectName("lineEdShortcutSlice")
        self.gridLayout.addWidget(self.lineEdShortcutSlice, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.lineEdShortcutFull = QtWidgets.QLineEdit(self.page_2)
        self.lineEdShortcutFull.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdShortcutFull.setObjectName("lineEdShortcutFull")
        self.gridLayout.addWidget(self.lineEdShortcutFull, 1, 1, 1, 1)
        self.lineEdShortcutSave = QtWidgets.QLineEdit(self.page_2)
        self.lineEdShortcutSave.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdShortcutSave.setObjectName("lineEdShortcutSave")
        self.gridLayout.addWidget(self.lineEdShortcutSave, 3, 1, 1, 1)
        self.stkWidget.addWidget(self.page_2)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ccBoxAppHide = QtWidgets.QCheckBox(self.page_5)
        self.ccBoxAppHide.setObjectName("ccBoxAppHide")
        self.verticalLayout_2.addWidget(self.ccBoxAppHide)
        self.ccBoxAppShow = QtWidgets.QCheckBox(self.page_5)
        self.ccBoxAppShow.setObjectName("ccBoxAppShow")
        self.verticalLayout_2.addWidget(self.ccBoxAppShow)
        self.stkWidget.addWidget(self.page_5)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ccBoxAutoExec = QtWidgets.QCheckBox(self.page_3)
        self.ccBoxAutoExec.setObjectName("ccBoxAutoExec")
        self.verticalLayout.addWidget(self.ccBoxAutoExec)
        self.ccBoxWindowOnTop = QtWidgets.QCheckBox(self.page_3)
        self.ccBoxWindowOnTop.setObjectName("ccBoxWindowOnTop")
        self.verticalLayout.addWidget(self.ccBoxWindowOnTop)
        self.ccBoxMiniToTray = QtWidgets.QCheckBox(self.page_3)
        self.ccBoxMiniToTray.setObjectName("ccBoxMiniToTray")
        self.verticalLayout.addWidget(self.ccBoxMiniToTray)
        self.stkWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.page_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.page_4)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.stkWidget.addWidget(self.page_4)
        self.gridLayout_2.addWidget(self.stkWidget, 0, 1, 2, 1)
        self.listWidget = QtWidgets.QListWidget(Config)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.listWidget.setFont(font)
        self.listWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.listWidget.setMouseTracking(False)
        self.listWidget.setLineWidth(1)
        self.listWidget.setDragEnabled(False)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout_2.addWidget(self.listWidget, 0, 0, 3, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 3)

        self.retranslateUi(Config)
        self.stkWidget.setCurrentIndex(0)
        self.listWidget.setCurrentRow(-1)
        self.listWidget.currentRowChanged['int'].connect(self.stkWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(Config)

    def retranslateUi(self, Config):
        _translate = QtCore.QCoreApplication.translate
        Config.setWindowTitle(_translate("Config", "Dialog"))
        self.btnSaveConfig.setText(_translate("Config", "保存"))
        self.btnCancel.setText(_translate("Config", "取消"))
        self.ccBoxSaveDesktop.setText(_translate("Config", "存到桌面文件夹"))
        self.label_2.setText(_translate("Config", "切片截图："))
        self.label_5.setText(_translate("Config", "全屏截图："))
        self.lineEdShortcutSlice.setText(_translate("Config", "Alt + Q"))
        self.label_6.setText(_translate("Config", "保存截图："))
        self.lineEdShortcutFull.setText(_translate("Config", "Alt + W"))
        self.lineEdShortcutSave.setText(_translate("Config", "Ctrl + S"))
        self.ccBoxAppHide.setText(_translate("Config", "截图时隐藏窗口"))
        self.ccBoxAppShow.setText(_translate("Config", "截图完成恢复窗口"))
        self.ccBoxAutoExec.setText(_translate("Config", "开机自动启动"))
        self.ccBoxWindowOnTop.setText(_translate("Config", "启动主窗口总在最前"))
        self.ccBoxMiniToTray.setText(_translate("Config", "最小化到托盘"))
        self.textEdit.setHtml(_translate("Config", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'微软雅黑 Light\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">aaaaaaaaaaa</p></body></html>"))
        self.listWidget.setSortingEnabled(False)
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Config", "存储路径"))
        item = self.listWidget.item(1)
        item.setText(_translate("Config", "快捷键"))
        item = self.listWidget.item(2)
        item.setText(_translate("Config", "截图"))
        item = self.listWidget.item(3)
        item.setText(_translate("Config", "启动"))
        item = self.listWidget.item(4)
        item.setText(_translate("Config", "关于"))
        self.listWidget.setSortingEnabled(__sortingEnabled)

