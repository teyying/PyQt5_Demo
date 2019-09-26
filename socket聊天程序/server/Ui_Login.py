# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Login.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 250)
        self.formLayout_3 = QtWidgets.QFormLayout(Login)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_3.setContentsMargins(50, 0, 50, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(Login)
        self.label_4.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEditIp = QtWidgets.QLineEdit(Login)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditIp.sizePolicy().hasHeightForWidth())
        self.lineEditIp.setSizePolicy(sizePolicy)
        self.lineEditIp.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEditIp.setFont(font)
        self.lineEditIp.setStyleSheet("color: rgb(195, 0, 0);")
        self.lineEditIp.setMaxLength(15)
        self.lineEditIp.setObjectName("lineEditIp")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditIp)
        self.label_3 = QtWidgets.QLabel(Login)
        self.label_3.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEditPort = QtWidgets.QLineEdit(Login)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditPort.sizePolicy().hasHeightForWidth())
        self.lineEditPort.setSizePolicy(sizePolicy)
        self.lineEditPort.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEditPort.setFont(font)
        self.lineEditPort.setStyleSheet("color: rgb(195, 0, 0);")
        self.lineEditPort.setMaxLength(8)
        self.lineEditPort.setObjectName("lineEditPort")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditPort)
        self.btnLogin = QtWidgets.QPushButton(Login)
        self.btnLogin.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.btnLogin.setFont(font)
        self.btnLogin.setObjectName("btnLogin")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.btnLogin)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "聊天服务器登录"))
        self.label_4.setText(_translate("Login", "地址："))
        self.lineEditIp.setInputMask(_translate("Login", "000.000.000.000"))
        self.lineEditIp.setPlaceholderText(_translate("Login", "请输入ip地址"))
        self.label_3.setText(_translate("Login", "端口："))
        self.lineEditPort.setPlaceholderText(_translate("Login", "请输入port端口"))
        self.btnLogin.setText(_translate("Login", "启动服务器"))
