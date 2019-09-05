from sys import argv

import gevent
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

from gevent import socket, monkey

from Ui_ChatSocket import Ui_ChatSocket

import cgitb
cgitb.enable(format='text')

monkey.patch_all()


class ChatServer(QThread):
    sendSingnal = pyqtSignal(str, int, str)

    def __init__(self, recvSingnal):
        super().__init__()
        self.recvSingnal = recvSingnal
        self.sendSingnal.connect(self.fn)

    def run(self):
        self.connectServer()

    def fn(self, ip, port, data):
        print(ip, port, data)
        addr = (ip, port)
        print(addr)
        # self.server.sendto(bytes(data, encoding='utf-8'), addr)
        # self.server.send(bytes(data, encoding='utf-8'))
        # self.server.sendall(bytes(data, encoding='utf-8'))

    def handle_request(self, client, addr):
        while True:
            data = client.recv(1024)
            if not data:
                client.close()
                break
            ip, port = addr
            self.recvSingnal.emit(ip, port, f"{data.decode()}")

            # client.send(["a","b","c","d","e"])  #发送的数据
            # conn.send(data.encode())

    def connectServer(self):
        self.server = socket.socket()
        self.server.bind(("", 7777))
        self.server.listen(5)
        while True:
            client, addr = self.server.accept()
            gevent.spawn(self.handle_request, client, addr)


class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    recvSingnal = pyqtSignal(str, int, str)

    def __init__(self):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("服务器")

        self.ip = ''
        self.port = 0

        self.recvSingnal.connect(self.slot_recvSingnal)

        self.chatServer = ChatServer(self.recvSingnal)
        # self.chatServer.start()

        self.btnServer.clicked.connect(self.slot_btnServer)
        self.btnSend.clicked.connect(self.slot_btnSend)

    def slot_recvSingnal(self, ip, port, data):
        self.ip = ip
        self.port = port
        self.recv_textEdit.insertPlainText(f"\n{ip}:{port}\n{data}")

    def slot_btnServer(self):
        text = self.btnServer.text()
        if text == '启动服务器':
            self.chatServer.start()
            self.btnServer.setText('断开服务器')
            self.btnServer.setStyleSheet('color: green;')

    def slot_btnSend(self):
        adminInput = self.send_textEdit.toPlainText()
        # self.clientsock.send(bytes(adminInput, encoding='utf-8'))  # 发送消息
        if adminInput:
            self.chatServer.sendSingnal.emit(self.ip, self.port, adminInput)
            self.send_textEdit.clear()


if __name__ == '__main__':
    app = QApplication(argv)
    myServer = Ui_ChatServer_Logic()
    myServer.show()
    exit(app.exec_())
