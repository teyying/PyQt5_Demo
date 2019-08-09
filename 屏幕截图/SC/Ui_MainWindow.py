# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(94, 60)
        MainWindow.setMinimumSize(QtCore.QSize(90, 60))
        MainWindow.setMaximumSize(QtCore.QSize(94, 60))
        MainWindow.setMouseTracking(True)
        self.frame = QtWidgets.QFrame(MainWindow)
        self.frame.setGeometry(QtCore.QRect(-1, -1, 90, 60))
        self.frame.setMinimumSize(QtCore.QSize(90, 60))
        self.frame.setMaximumSize(QtCore.QSize(90, 60))
        self.frame.setMouseTracking(True)
        self.frame.setObjectName("frame")
        self.btnConfig = QtWidgets.QPushButton(self.frame)
        self.btnConfig.setGeometry(QtCore.QRect(1, 1, 30, 30))
        self.btnConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.btnConfig.setMouseTracking(True)
        self.btnConfig.setText("")
        self.btnConfig.setObjectName("btnConfig")
        self.btnMini = QtWidgets.QPushButton(self.frame)
        self.btnMini.setGeometry(QtCore.QRect(31, 1, 30, 30))
        self.btnMini.setMaximumSize(QtCore.QSize(30, 30))
        self.btnMini.setMouseTracking(True)
        self.btnMini.setText("")
        self.btnMini.setObjectName("btnMini")
        self.btnClose = QtWidgets.QPushButton(self.frame)
        self.btnClose.setGeometry(QtCore.QRect(61, 1, 30, 30))
        self.btnClose.setMaximumSize(QtCore.QSize(30, 30))
        self.btnClose.setMouseTracking(True)
        self.btnClose.setText("")
        self.btnClose.setObjectName("btnClose")
        self.btnScShot = QtWidgets.QPushButton(self.frame)
        self.btnScShot.setGeometry(QtCore.QRect(1, 31, 60, 30))
        self.btnScShot.setMinimumSize(QtCore.QSize(60, 30))
        self.btnScShot.setMaximumSize(QtCore.QSize(60, 30))
        self.btnScShot.setMouseTracking(True)
        self.btnScShot.setText("")
        self.btnScShot.setObjectName("btnScShot")
        self.btnPrtSc = QtWidgets.QPushButton(self.frame)
        self.btnPrtSc.setGeometry(QtCore.QRect(61, 31, 30, 30))
        self.btnPrtSc.setMinimumSize(QtCore.QSize(0, 30))
        self.btnPrtSc.setMaximumSize(QtCore.QSize(30, 30))
        self.btnPrtSc.setMouseTracking(True)
        self.btnPrtSc.setText("")
        self.btnPrtSc.setObjectName("btnPrtSc")

        self.retranslateUi(MainWindow)
        self.btnClose.clicked.connect(MainWindow.close)
        self.btnMini.clicked.connect(MainWindow.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dialog"))
        self.btnConfig.setToolTip(_translate("MainWindow", "设置"))
        self.btnMini.setToolTip(_translate("MainWindow", "最小化"))
        self.btnClose.setToolTip(_translate("MainWindow", "关闭"))
        self.btnScShot.setToolTip(_translate("MainWindow", "切片截图"))
        self.btnScShot.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.btnPrtSc.setToolTip(_translate("MainWindow", "全屏截图"))
        self.btnPrtSc.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))

