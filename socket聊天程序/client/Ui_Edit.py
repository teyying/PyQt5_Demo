# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Edit.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Edit(object):
    def setupUi(self, Edit):
        Edit.setObjectName("Edit")
        Edit.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Edit.sizePolicy().hasHeightForWidth())
        Edit.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Edit)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEditRecv = QtWidgets.QTextEdit(Edit)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEditRecv.setFont(font)
        self.textEditRecv.setStyleSheet("color: rgb(0, 0, 195);")
        self.textEditRecv.setObjectName("textEditRecv")
        self.verticalLayout.addWidget(self.textEditRecv)
        self.textEditSend = QtWidgets.QTextEdit(Edit)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEditSend.setFont(font)
        self.textEditSend.setObjectName("textEditSend")
        self.verticalLayout.addWidget(self.textEditSend)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 2)

        self.retranslateUi(Edit)
        QtCore.QMetaObject.connectSlotsByName(Edit)

    def retranslateUi(self, Edit):
        _translate = QtCore.QCoreApplication.translate
        Edit.setWindowTitle(_translate("Edit", "Form"))
