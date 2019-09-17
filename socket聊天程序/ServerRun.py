from sys import argv

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from gevent import socket, monkey, spawn, _socket3

from Ui_ChatSocket import Ui_ChatSocket

import cgitb

from Ui_Login import Ui_Login

cgitb.enable(format='text')

monkey.patch_all()

# 应该专门给服务设计一个界面，或者把不用的控件删除，另存一个新ui文件，并编译导入

class ChatServer(QThread):

    def __init__(self, newClientSingnal, recvSingnal, closeSingnal):
        super().__init__()
        self.newClientSingnal = newClientSingnal
        self.recvSingnal = recvSingnal
        self.closeSingnal = closeSingnal

        # 线程终止后执行指定函数
        self.finished.connect(self.closeServer)
        # self.start.connect()

    def closeServer(self):
        self.flag = False
        self.server.close()

    def run(self):
        self.flag = True  # 关闭服务器时需要的标记
        # 创建套接字，不能在init中，必须在此方法内。可以跟创建线程时就初始化套接字有关，
        # 好像是线程没start时，不可以创建套接字。
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间，这样客户端断开连接捕获到错误时，服务器还能accept
        self.server.settimeout(2)
        self.server.bind(("", 7777))
        self.server.listen(5)
        while self.flag:  # 关闭服务器时，必须先break掉循环，再关闭服务器，最后终止线程
            try:
                # 不停的接收新客户端，最大数量看listen设置的是多少
                client, addr = self.server.accept()
                self.newClientSingnal.emit(client, addr)
                # 如果监听到新的客户端，就添加到协程，协程里循环一遍每个spawn(客户端)是否发来数据，
                # 然后跳出，继续self.server.accept()监听是否有新客户端，以此不停循环。
                spawn(self.handle_request, client, addr)
            except Exception as e:
                print("-----", e)

    def handle_request(self, client, addr):
        """
        此函数相当于有多少客户端连接就用协程开了多少个此函数，gevent源代码内部会把每个此函数添加
        进一个列表，然后遍历一次列表（每一个此函数）。
        """
        while self.flag:  # 关闭服务器时，必须先break掉循环，再关闭服务器，最后终止线程
            try:
                data = client.recv(1024)
                # 客户端在主动关闭套接字(非断网或者直接退出程序)时，会不能发送空数据，然后服务器
                # 里的协程的此会不停的接受空数据，也就是此上面的data，造成程序崩溃，所以需要把此
                # 客户端在服务器端再关闭一次，判断接收的是否空数据，如果是就关闭客户端。突然觉得
                # 好像gevent库的作者本身就是这样设计的。
                if not data:
                    client.close()
                    self.closeSingnal.emit(addr)
                    break
                self.recvSingnal.emit(addr, data.decode())
            except WindowsError as e:
                if e.errno == 10054:  # 异常:远程主机强迫关闭了一个现有的连接。
                    # 这里可以传一个谁退出的记录
                    client.close()
                    self.closeSingnal.emit(addr)
                    break
            except Exception as e:
                print('(((((', e)


class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    # 因为要接收客户端套接字，用type方法检查是gevent._socket3.socket类型
    newClientSingnal = pyqtSignal(_socket3.socket, tuple)
    recvSingnal = pyqtSignal(tuple, str)
    closeSingnal = pyqtSignal(tuple)

    def __init__(self):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("服务器")

        self.ip = ''
        self.port = 0
        self.clientDict = {}

        self.newClientSingnal.connect(self.slot_newClientSingnal)
        self.recvSingnal.connect(self.slot_recvSingnal)
        self.closeSingnal.connect(self.slot_closeSingnal)

        self.chatServer = ChatServer(self.newClientSingnal, self.recvSingnal, self.closeSingnal)
        self.chatServer.finished.connect(self.fn)

    def slot_newClientSingnal(self, newClient, addr):
        print("有新客户:", addr)
        self.clientDict[addr] = newClient
        self.listWidget.addItem(f"{addr[0]}:{addr[1]}")
        self.ipLineEdit.setText(addr[0])
        self.portLineEdit.setText(str(addr[1]))
        print(self.clientDict)

    def slot_recvSingnal(self, addr, data):
        if self.recv_textEdit.toPlainText():
            self.recv_textEdit.insertPlainText(f"\n{addr[0]}:{addr[1]}\n{data}")
        else:
            self.recv_textEdit.insertPlainText(f"{addr[0]}:{addr[1]}\n{data}")

    def slot_closeSingnal(self, addr):
        self.clientDict.pop(addr)
        a = (self.ipLineEdit.text(), self.portLineEdit.text())
        for i in range(1, self.listWidget.count()+1):
            itemText = self.listWidget.item(i).text()
            c, d = itemText.split(":")
            if a == (c, d):
                self.listWidget.takeItem(i)

        print(self.clientDict)

    @pyqtSlot()
    def on_btnServer_clicked(self):
        text = self.btnServer.text()
        if text == '启动服务器':
            self.chatServer.start()
            self.btnServer.setText('断开服务器')
            self.btnServer.setStyleSheet('color: green;')
        else:
            # for _, client in self.clientDict.items():
            #     client.send("Close from server".encode("utf-8"))
            # 强制终止线程。不用exit()方法，是因为socket的accept还在继续循环着，如果不使其循环break，线程就
            # 无法发出自带的finished信号
            self.chatServer.terminate()
            self.chatServer.wait()  # 确保线程终止

            self.clientDict = dict()
            self.btnServer.setText('启动服务器')
            self.btnServer.setStyleSheet('color: red;')

    def fn(self):
        print('我退出了')

    @pyqtSlot()
    def on_btnSend_clicked(self):
        if not self.clientDict:
            QMessageBox.information(self, "发送错误", '客户端连接为空。', QMessageBox.Ok)
            return

        serverInput = self.send_textEdit.toPlainText()
        for k, v in self.clientDict.items():
            # 空数据套接字会自动屏蔽，所以不用再做判断了。
            v.send(bytes(serverInput, encoding='utf-8'))
        # self.clientDict[addr].send(bytes('终于成功了', encoding='utf-8'))
        self.send_textEdit.clear()


class Ui_Login_Logic(QWidget, Ui_Login):
    def __init__(self):
        super(Ui_Login_Logic, self).__init__()
        self.setupUi(self)
        self.btnGoSignIn.hide()

    @pyqtSlot()
    def on_btnLogin_clicked(self):
        self.ui = Ui_ChatServer_Logic()
        self.ui.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    window = Ui_Login_Logic()
    window.show()
    exit(app.exec_())
