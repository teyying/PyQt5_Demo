from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QIntValidator
from gevent import socket
from sys import argv

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from Ui_ChatSocket import Ui_ChatSocket


class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    def __init__(self):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("客户端")

        self.btnServer.setText('连接服务器')
        self.ipLineEdit.setText('127.0.0.1')
        self.portLineEdit.setText('7777')
        self.portLineEdit.setValidator(QIntValidator(1, 99999))


        # recvdata = clientsock.recv(1024)  # 接收消息 recvdata 是bytes形式的
        # print(str(recvdata,encoding='utf-8')) # 我们看不懂bytes，所以转化为 str
        #

        self.btnSend.clicked.connect(self.slot_btnSend)
        self.btnServer.clicked.connect(self.slot_btnServer)

    def slot_btnSend(self):
        try:
            userInput = self.send_textEdit.toPlainText()
            self.clientsock.send(bytes(userInput, encoding='utf-8'))  # 发送消息
        except Exception as e:
            QMessageBox.critical(self, "发送失败", str(e), QMessageBox.Ok)
        else:
            self.send_textEdit.clear()

    def slot_btnServer(self):
        text = self.btnServer.text()
        if text == '连接服务器':
            try:
                if not self.portLineEdit.text():
                    QMessageBox.information(self, "连接错误", 'IP或PORT未填写。', QMessageBox.Ok)
                    return
                # addr = ('127.0.0.1', 7777)
                addr = (self.ipLineEdit.text(), int(self.portLineEdit.text()))
                self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientsock.connect(addr)  # 建立连接
            except Exception as e:
                QMessageBox.critical(self, "连接失败", str(e), QMessageBox.Ok)
            else:
                self.btnServer.setText('断开连接')
                self.btnServer.setStyleSheet('color: green')
        else:
            self.clientsock.close()
            self.btnServer.setText('连接服务器')
            self.btnServer.setStyleSheet('color: red')

if __name__ == '__main__':
    app = QApplication(argv)
    myServer = Ui_ChatServer_Logic()
    myServer.show()
    exit(app.exec_())
