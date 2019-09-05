from multiprocessing import Process, Pipe
from os import system
from sys import argv

import gevent
from PyQt5.QtWidgets import QWidget, QApplication

from gevent import socket, monkey
from gevent.threading import Thread

from Ui_ChatSocket import Ui_ChatSocket

monkey.patch_all()

class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    def __init__(self):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("服务器")
        # self.t = t

        self.t = Process(target=self.server)
        self.t.daemon = True  # 默认状态False，主进程退出不影响子进程。True :子进程随着主进程结束

    def showEvent(self, e):
        self.t.start()

    # def closeEvent(self, e):
    #     cmd = 'taskkill /pid ' + str(self.t.pid) + ' /f'
    #     try:
    #         system(cmd)
    #     except Exception as e:
    #         print(e)


    @classmethod
    def handle_request(cls, client, addr):
        while True:
            data = client.recv(1024)
            if not data:
                client.close()
                break
            print(f"(接收)<<< {data.decode()}")
            print(addr)
            # cls.recv_textEdit.setText(data.decode())
            # conn.send(data.encode())

    @classmethod
    def server(cls):
        soc = socket.socket()
        soc.bind(("", 7777))
        soc.listen(5)
        print("运行中。。。")
        while True:
            client, addr = soc.accept()
            gevent.spawn(cls.handle_request, client, addr)


if __name__ == '__main__':

    # t = Process(target=server, args=(7777,))
    # t = Process(target=server)
    app = QApplication(argv)
    myServer = Ui_ChatServer_Logic()
    myServer.show()
    exit(app.exec_())



    # t2 = Thread(target=exit, args=(app.exec_(),))
    # t2.start()
