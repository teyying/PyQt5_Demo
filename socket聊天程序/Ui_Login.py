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
        self.verticalLayout = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(Login)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout = QtWidgets.QGridLayout(self.page)
        self.gridLayout.setContentsMargins(45, -1, 45, -1)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditId = QtWidgets.QLineEdit(self.page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditId.sizePolicy().hasHeightForWidth())
        self.lineEditId.setSizePolicy(sizePolicy)
        self.lineEditId.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEditId.setFont(font)
        self.lineEditId.setMaxLength(8)
        self.lineEditId.setObjectName("lineEditId")
        self.gridLayout.addWidget(self.lineEditId, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditPswd_2 = QtWidgets.QLineEdit(self.page)
        self.lineEditPswd_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEditPswd_2.setFont(font)
        self.lineEditPswd_2.setMaxLength(15)
        self.lineEditPswd_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPswd_2.setObjectName("lineEditPswd_2")
        self.gridLayout.addWidget(self.lineEditPswd_2, 1, 1, 1, 1)
        self.btnGoSignIn = QtWidgets.QPushButton(self.page)
        self.btnGoSignIn.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnGoSignIn.setFont(font)
        self.btnGoSignIn.setObjectName("btnGoSignIn")
        self.gridLayout.addWidget(self.btnGoSignIn, 2, 0, 1, 1)
        self.btnLogin = QtWidgets.QPushButton(self.page)
        self.btnLogin.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.btnLogin.setFont(font)
        self.btnLogin.setObjectName("btnLogin")
        self.gridLayout.addWidget(self.btnLogin, 2, 1, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setPointSize(15)
        self.page_2.setFont(font)
        self.page_2.setObjectName("page_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.lineEditConfirmPswd = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditConfirmPswd.sizePolicy().hasHeightForWidth())
        self.lineEditConfirmPswd.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEditConfirmPswd.setFont(font)
        self.lineEditConfirmPswd.setObjectName("lineEditConfirmPswd")
        self.gridLayout_2.addWidget(self.lineEditConfirmPswd, 2, 1, 1, 1)
        self.lineEditPswd = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditPswd.sizePolicy().hasHeightForWidth())
        self.lineEditPswd.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEditPswd.setFont(font)
        self.lineEditPswd.setObjectName("lineEditPswd")
        self.gridLayout_2.addWidget(self.lineEditPswd, 1, 1, 1, 1)
        self.lineEditNickname = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditNickname.sizePolicy().hasHeightForWidth())
        self.lineEditNickname.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEditNickname.setFont(font)
        self.lineEditNickname.setObjectName("lineEditNickname")
        self.gridLayout_2.addWidget(self.lineEditNickname, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.btnBack = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBack.sizePolicy().hasHeightForWidth())
        self.btnBack.setSizePolicy(sizePolicy)
        self.btnBack.setObjectName("btnBack")
        self.gridLayout_2.addWidget(self.btnBack, 3, 0, 1, 1)
        self.btnSignIn = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSignIn.sizePolicy().hasHeightForWidth())
        self.btnSignIn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(19)
        self.btnSignIn.setFont(font)
        self.btnSignIn.setObjectName("btnSignIn")
        self.gridLayout_2.addWidget(self.btnSignIn, 3, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)

        self.retranslateUi(Login)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Form"))
        self.label.setText(_translate("Login", "账号："))
        self.lineEditId.setPlaceholderText(_translate("Login", "请输入账号"))
        self.label_2.setText(_translate("Login", "密码："))
        self.lineEditPswd_2.setPlaceholderText(_translate("Login", "请输入密码"))
        self.btnGoSignIn.setText(_translate("Login", "注册"))
        self.btnLogin.setText(_translate("Login", "登录"))
        self.label_5.setText(_translate("Login", "确认密码："))
        self.lineEditConfirmPswd.setPlaceholderText(_translate("Login", "再次输入密码"))
        self.lineEditPswd.setPlaceholderText(_translate("Login", "最多15位"))
        self.lineEditNickname.setPlaceholderText(_translate("Login", "最多8个字符"))
        self.label_4.setText(_translate("Login", "密码："))
        self.label_3.setText(_translate("Login", "昵称："))
        self.btnBack.setText(_translate("Login", "返回"))
        self.btnSignIn.setText(_translate("Login", "注册"))
