from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIntValidator
import socket  # 客户端不需要执行导入gevent的socket和monkey
from sys import argv

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from Ui_ChatSocket import Ui_ChatSocket

import cgitb

from Ui_Login import Ui_Login

cgitb.enable(format='text')


class ChatClient(QThread):
    def __init__(self, recvSingnal, closeSingnal, errorSignal, succeedSingnal, addr):
        super().__init__()
        self.recvSingnal = recvSingnal
        self.closeSingnal = closeSingnal
        self.errorSingnal = errorSignal
        self.succeedSingnal = succeedSingnal
        self.addr = addr

    def run(self):
        try:
            # 创建套接字，不能在init中，必须在此方法内。可以跟创建线程时就初始化套接字有关，
            # 好像是线程没start时，不可以创建套接字。
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(2)
            self.client.connect(self.addr)  # 建立连接
        except Exception as e:
            # 处理*未连接*服务器时，发出“错误弹窗”,已连接的异常捕获在else语句里
            self.errorSingnal.emit(str(e))
            self.exit()  # 退出线程
        else:
            self.succeedSingnal.emit()
            while True:
                try:
                    msg = self.client.recv(1024)  # 接收消息
                    if msg == b"Close from server":
                        break
                    self.recvSingnal.emit(msg.decode())
                except WindowsError as e:
                    if e.errno == 10038 or e.errno == 10054:
                        break
                # except Exception as e:
                #     print(e)
            self.closeSingnal.emit()


class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    recvSingnal = pyqtSignal(str)
    closeSingnal = pyqtSignal()
    errorSingnal = pyqtSignal(str)
    succeedSingnal = pyqtSignal()

    def __init__(self):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("客户端")

        self.addr = ()  # ‘连接服务器’时取得值

        self.btnServer.setText('连接服务器')
        # self.ipLineEdit.setText('192.168.31.112')
        self.ipLineEdit.setText('192.168.1.108')
        self.portLineEdit.setText('7777')
        self.portLineEdit.setValidator(QIntValidator(1, 99999))

        self.recvSingnal.connect(self.slot_recvSingnal)
        self.closeSingnal.connect(self.slot_closeSingnal)
        self.errorSingnal.connect(self.slot_errorSingnal)
        self.succeedSingnal.connect(self.slot_succeedSingnal)

        self.btnSend.clicked.connect(self.slot_btnSend)
        self.btnServer.clicked.connect(self.slot_btnServer)

    def slot_btnSend(self):
        try:
            userInput = self.send_textEdit.toPlainText()
            # 空数据套接字会自动屏蔽，所以不用再做判断了。
            self.chatClient.client.send(bytes(userInput, encoding='utf-8'))  # 发送消息
        except Exception as e:
            QMessageBox.critical(self, "发送失败", str(e), QMessageBox.Ok)
        else:
            self.send_textEdit.clear()

    def slot_singnal(self, flag, *args):
        pass

    def slot_recvSingnal(self, data):
        strTmp = f"{self.addr[0]}:{self.addr[1]}\n{data}"
        if self.recv_textEdit.toPlainText():
            self.recv_textEdit.insertPlainText(f"\n{strTmp}")
        else:
            self.recv_textEdit.insertPlainText(strTmp)

    def slot_closeSingnal(self):
        self.btnServer.setText('连接服务器')
        self.btnServer.setStyleSheet('color: red')
        QMessageBox.critical(self, "连接断开", "连接意外断开，请再次尝试连接服务器", QMessageBox.Ok)

    def slot_errorSingnal(self, error):
        QMessageBox.critical(self, "连接失败", str(error), QMessageBox.Ok)

    def slot_succeedSingnal(self):
        self.btnServer.setText('断开连接')
        self.btnServer.setStyleSheet('color: green')

    def slot_btnServer(self):
        text = self.btnServer.text()
        if text == '连接服务器':
            if not self.portLineEdit.text():
                QMessageBox.information(self, "连接错误", 'IP或PORT未填写。', QMessageBox.Ok)
                return
            self.addr = (self.ipLineEdit.text(), int(self.portLineEdit.text()))
            self.chatClient = ChatClient(self.recvSingnal, self.closeSingnal, self.errorSingnal, self.succeedSingnal,
                                         self.addr)
            self.chatClient.started.connect(self.fn)
            self.chatClient.start()  # 线程开始
        else:
            # 客户端在主动关闭套接字(非断网或者直接退出程序)时，会不能发送空数据，然后服务器
            # 里的协程的此会不停的接受空数据，也就是此上面的data，造成程序崩溃，所以需要把此
            # 客户端在服务器端再关闭一次，判断接收的是否空数据，如果是就关闭客户端。突然觉得
            # 好像gevent库的作者本身就是这样设计的。
            self.chatClient.client.close()  # 客户端关闭套接字，会不停的发送空数据。
            self.chatClient.exit()  # 退出线程
            self.chatClient.deleteLater()  # 删掉实例化的线程对象
            self.btnServer.setText('连接服务器')
            self.btnServer.setStyleSheet('color: red')
    def fn(self):
        print(999999999)
        print(self.chatClient)
        # print(self.chatClient.client)

class Ui_Login_Logic(QWidget, Ui_Login):
    def __init__(self):
        super(Ui_Login_Logic, self).__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_btnGoSignIn_clicked(self):  # 进入账号注册页
        self.stackedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_btnLogin_clicked(self):  # 登录账号
        self.ui = Ui_ChatServer_Logic()
        self.ui.show()
        self.close()

    @pyqtSlot()
    def on_btnSignIn_clicked(self):  # 开始注册账号
        print('注册好了')

    @pyqtSlot()
    def on_btnBack_clicked(self):  # 返回账号登录页
        self.stackedWidget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(argv)
    window = Ui_Login_Logic()
    window.show()
    exit(app.exec_())
