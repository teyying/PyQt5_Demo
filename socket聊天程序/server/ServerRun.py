import json
from sys import argv

from PyQt5.QtGui import QIntValidator
from gevent import socket, monkey, spawn, _socket3

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QListWidgetItem, QVBoxLayout

from server.Flag import Flag as F
from server.Ui_ChatSocket import Ui_ChatSocket
from server.Ui_Login import Ui_Login
from server.Ui_Edit import Ui_Edit

import cgitb

cgitb.enable(format='text')

monkey.patch_all()


class ChatServer(QThread):
    flagClose = True  # 关闭服务器时需要的标记

    def __init__(self, newClientSingnal, recvSingnal, closeSingnal, loginSingnal, addr):
        super().__init__()
        self.newClientSingnal = newClientSingnal
        self.recvSingnal = recvSingnal
        self.closeSingnal = closeSingnal
        self.loginSingnal = loginSingnal
        self.addr = addr

        # 线程终止后执行指定函数
        self.finished.connect(self.closeServer)

    def closeServer(self):
        """我是先强制结束线程，结束之后会执行finished信号进入此函数里"""
        self.flagClose = False  # 先关线程中的循环
        self.server.close()  # 再关闭套接字

    def run(self):
        # 创建套接字，不能在init中，必须在此方法内。可以跟创建线程时就初始化套接字有关，
        # 好像是线程没start时，不可以创建套接字。
        self.flagClose = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间，这样客户端断开连接捕获到错误时，服务器还能accept
        self.server.settimeout(2)

        try:
            self.server.bind(self.addr)  # ("", 7777)

        except WindowsError as e:  # 捕获异常：地址错误或者端口被占用
            self.loginSingnal.emit(str(e))
            # 直接返回，不然会执行下面self.server.listen(5)而报错。不把listen写在异常捕获里面，
            # 是因为监听后会执行下面的循环，而再次报错就会在self.server.accept()语句上，服务器
            # 没连连，肯定会再次报错
            return
        else:
            self.loginSingnal.emit('')
            self.server.listen(5)

        while self.flagClose:  # 关闭服务器时，必须先break掉循环，再关闭服务器，最后终止线程
            try:
                client, addr = self.server.accept()  # 不停的接收新客户端，最大数量看listen设置的是多少

                # 原本新客户端连接是这个位置接受到连接信号的，因为客户端代码写了一连接就发送专用数据"=:__"，
                # 所以不需要在这里处理其它功能方法了
                # self.newClientSingnal.emit(client, addr)

                # 如果监听到新的客户端，就添加到协程，协程里循环一遍每个spawn(客户端)是否发来数据，
                # 然后跳出，继续self.server.accept()监听是否有新客户端，以此不停循环。
                spawn(self.handle_request, client, addr)
            except WindowsError as e:
                print("---", e)

    def handle_request(self, client, addr):
        """
        此函数相当于有多少客户端连接就用协程开了多少个此函数，gevent源代码内部会把每个此函数添加
        进一个列表，然后遍历一次列表（每一个此函数）。
        """
        while self.flagClose:  # 关闭服务器时，必须先break掉循环，再关闭服务器，最后终止线程
            try:
                data = client.recv(1024)

                # 客户端在主动关闭套接字(非断网或者直接退出程序)时，会不能发送空数据，然后服务器
                # 里的协程的此会不停的接受空数据，也就是此上面的data，造成程序崩溃，所以需要把此
                # 客户端在服务器端再关闭一次，判断接收的是否空数据，如果是就关闭客户端。突然觉得
                # 好像gevent库的作者本身就是这样设计的。
                if not data:  # 客户端点击断开连接时，执行这里，直接点X关闭界面，执行下面的closeSingnal
                    self.closeSingnal.emit(client)
                    break
                dataLoads = json.loads(data.decode())  # 先解码数据，再用json方法转化为字典
                flag = dataLoads['flag']

                if flag == F.Login:
                    sql = json.load(open('sql.json', 'r', encoding='utf-8'))
                    k_id = sql.get(dataLoads['id'])
                    if k_id and dataLoads['password'] == k_id['password']:
                        k_id['flag'] = F.LoginSuccess
                        k_id['id'] = dataLoads['id']
                        client.send(bytes(json.dumps(k_id), encoding='utf-8'))
                        clientData = k_id
                        clientData['socket'] = client
                        clientData['addr'] = addr
                        self.newClientSingnal.emit(clientData)

                        # 有人登陆就发给所有客户
                        # self.server.send(bytes(json.dumps(k_id), encoding='utf-8'))
                    else:
                        flag = {"flag": F.LoginFailed}
                        client.send(bytes(json.dumps(flag), encoding='utf-8'))

                elif flag == F.MsgText:
                    self.recvSingnal.emit(client, dataLoads)

            except WindowsError as e:
                if e.errno == 10054:  # 异常:远程主机强迫关闭了一个现有的连接。
                    # 这里可以传一个谁退出的记录
                    # 客户端直接点X关闭界面时，执行这里。点击断开连接时，执行上面的closeSingnal
                    self.closeSingnal.emit(client)
                    break


class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    # 因为要接收客户端套接字，用type方法检查是gevent._socket3.socket类型
    newClientSingnal = pyqtSignal(dict)  # 有新客户端连接信号
    recvSingnal = pyqtSignal(_socket3.socket, dict)  # 接收消息信号
    closeSingnal = pyqtSignal(_socket3.socket)  # 断开服务器套接字信号

    def __init__(self, parent, addr):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.p = parent
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # 这个数据是全面的，下面两个相当于从这里面分化出来的，便于处理其它操作
        self.friendData = dict()
        # 主要用于客户端主动退出时，删除相应的控件，以及服务器切换登录时，关闭所有客户套接字{socket: [uiEdit, item]}
        self.closeData = dict()
        # 主要用于给刚登录的客户发送在线客户数据。{id: {'id': xxx, 'nickname': xxx, 'addr':xxx}
        self.onlineData = dict()

        # 设置分割界面的初始比例(索引0，2/(2+7),索引1，7/(2+7))
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 7)

        # 因为设计师创建的stackedWidget，自带了两个子widget。为了动态添加子页时，统一
        # 格式，所以要删除掉。
        self.p0.deleteLater()
        self.p1.deleteLater()
        del self.p0, self.p1

        # 自定义信号连接槽
        self.newClientSingnal.connect(self.slot_newClientSingnal)
        self.recvSingnal.connect(self.slot_recvSingnal)
        self.closeSingnal.connect(self.slot_closeSingnal)

        # 创建重写的线程类，并把要用到的自定义信号传进去
        self.chatServer = ChatServer(self.newClientSingnal, self.recvSingnal, self.closeSingnal,
                                     parent.loginSingnal, addr)
        self.chatServer.start()  # 线程开始

    @pyqtSlot()
    def on_btnSend_clicked(self):
        count = self.listWidget.count()
        row = self.listWidget.currentRow()
        if count == 1 and row == -1:
            QMessageBox.information(self, "发送错误", '请选择客户端。', QMessageBox.Ok)
        elif row == -1:
            QMessageBox.information(self, "发送错误", '还没有客户端连接。', QMessageBox.Ok)
        else:
            row = self.listWidget.currentRow()
            sendToId = self.listWidget.item(row).data(888)
            sendEdit = self.friendData[sendToId]['uiEdit'].textEditSend
            text = sendEdit.toPlainText()
            d = {'flag': F.MsgText, 'fromId': 'admin', 'msgText': text, 'sendToId': sendToId}
            self.friendData[sendToId]['socket'].send(bytes(json.dumps(d), encoding='utf-8'))
            sendEdit.clear()

    @pyqtSlot(int)
    def on_listWidget_currentRowChanged(self, index):
        """
        所有客户端聊天框(和stackedWidget中对应索引的widget)只有在点击listWidget对应的item项时，才创建实例，感觉这样省资源。
        客户端在主动或者被动退出时，已经处理删除对应的item了，并且还彻底删除了对应widget和他的实例变量了。
        """
        self.stackedWidget.setCurrentIndex(index)

    @pyqtSlot()
    def on_btnChangeId_clicked(self):
        reply = QMessageBox.information(self, "断开连接", "你确定要断开服务器，返回登录界面吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == 65536:
            return
        # 强制终止线程。不用exit()方法，是因为socket的accept还在继续循环着，如果不使其循环break，线程就
        # 无法发出自带的finished信号
        self.chatServer.terminate()
        self.chatServer.wait()  # 确保线程终止

        # 删除服务器和所有客户端的item
        for soc in self.closeData.keys():
            soc.close()  # 关闭所有客户端(这样客户端能收到无数据信号，以便提醒服务器已关闭)

        # 返回登录界面
        self.p.show()  # 自定义线程的生命周期还在login界面，因为聊天界面就是login界面创建的实例
        self.deleteLater()  # 彻底删除聊天界面，也就关闭了，close方法可能不会彻底删除吧
        del self  # 彻底删除后，里面的字典数据就不存在了，不用一个个清空了

    def slot_newClientSingnal(self, adminData):
        """
        1、给新登录的客户端添加聊天界面。 2、通知其它在线的好友
        3、给此客户端发送在线好友的信息，以便他添加进好友列表。4 、添加此客户端的数据到特定的字典里
        """
        uiEdit = Ui_Edit_Logic(self.stackedWidget)
        self.stackedWidget.addWidget(uiEdit)
        d = {
            'id': adminData['id'],
            'nickname': adminData['nickname'],
            'addr': adminData['addr'],
            "flag": F.NewFriend
        }
        for soc in self.closeData.keys():  # 给在线的客户端发刚刚登录的新客户端数据
            soc.send(bytes(json.dumps(d), encoding='utf-8'))

        if self.onlineData:  # 如果有在线的客户端，就全部发给新登录的客户端
            d2 = {'flag': F.OnlineFriend, 'onlineFriend': self.onlineData}
            adminData['socket'].send(bytes(json.dumps(d2), encoding='utf-8'))

        # 创建item对象，绑定好数据，添加进列表控件
        item = QListWidgetItem(adminData['nickname'])
        item.setData(888, adminData['id'])  # 绑定数据：客户端Id
        self.listWidget.addItem(item)  # 添加进列表

        # 为了方便通过id号找到socket发送消息
        self.friendData[adminData['id']] = {
            'socket': adminData['socket'],
            'nickname': adminData['nickname'],
            'addr': adminData['addr'],
            'uiEdit': uiEdit,
        }

        # 又添加一个字典是因为客户端点"X"退出时，得不到"id"账号，没法删除相应的控件
        # 执行完删除后，不但要清理closeData，还要通过此item的data(888)得到id号，然后
        # 再清理friendData中的此客户端，有点啰嗦，先这样吧。
        self.closeData[adminData['socket']] = (uiEdit, item)

        # 把此时登录的客户端id, nickname, addr数据专门存入在线好友字典，以方便后面
        # 登录的客户端的把这些在线好友添加进聊天列表。在最后存入是因为不能把自己也
        # 添加进自己的好友列表。
        d3 = {
            'id': adminData['id'],
            'nickname': adminData['nickname'],
            'addr': adminData['addr']
        }
        self.onlineData[adminData['id']] = d3

    def slot_recvSingnal(self, client, data):
        flag = data["flag"]
        if flag == F.MsgText:  # 再判断if  data['msgText'] == 1
            text = f"{self.friendData[data['fromId']]['nickname']}\n{data['msgText']}\n\n"
            if data['sendToId'] == 'admin':
                editRecv = self.friendData[data['fromId']]['uiEdit'].textEditRecv
                editRecv.insertPlainText(text)
                editRecv.verticalScrollBar().setSliderPosition(editRecv.verticalScrollBar().maximum())
            else:
                self.friendData[data['sendToId']]['socket'].send(bytes(json.dumps(data), encoding="utf-8"))

    def slot_closeSingnal(self, client):
        """客户端退出后，清除服务器ui界面对应客户端部件"""
        uiEdit, item = self.closeData[client]
        clientId = item.data(888)
        self.stackedWidget.removeWidget(uiEdit)  # 删除此客户的聊天页面
        uiEdit.deleteLater()
        del uiEdit  # 彻底删除编辑界面
        self.friendData.pop(clientId)  # 删除此客户的键值，下面closeData字典也要pop一次此客户的键值
        self.listWidget.takeItem(self.listWidget.row(item))  # 删除此行
        self.closeData.pop(client)  # 专门用于删除控件的字典，删除对应key
        self.onlineData.pop(clientId)  # 删除在线数据里的此客户端

        d = {'flag': F.FriendExit, 'fromId': clientId}
        for soc in self.closeData.keys():  # 通知其它客户端哪个ID下线了
            soc.send(bytes(json.dumps(d), encoding="utf-8"))


class Ui_Edit_Logic(QWidget, Ui_Edit):
    def __init__(self, parent):
        super(Ui_Edit_Logic, self).__init__(parent)
        self.setupUi(self)
        self.p = parent
        parent.setLayout(QVBoxLayout())
        parent.layout().addWidget(self)

        # 重写发送框的键盘事件
        self.textEditSend_orgin_keyPressEvent = self.textEditSend.keyPressEvent
        self.textEditSend.keyPressEvent = self.textEditSend_keyPressEvent

    def textEditSend_keyPressEvent(self, e):
        """重写发送框的键盘事件，点击回车键执行发送按钮点击信号。"""
        if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.p.nativeParentWidget().on_btnSend_clicked()
        return self.textEditSend_orgin_keyPressEvent(e)


class Ui_Login_Logic(QWidget, Ui_Login):
    loginSingnal = pyqtSignal(str)  # 两种状态:异常错误，成功连接

    def __init__(self):
        super(Ui_Login_Logic, self).__init__()
        self.setupUi(self)
        self.loginSingnal.connect(self.slot_loginSingnal)

        self.lineEditPort.setValidator(QIntValidator(1, 9999))  # (0, 65535)

        # 这4行仅方便测试用，项目完成时删掉即可
        self.lineEditIp.setText('192.168.31 .112')
        self.lineEditPort.setText('7777')

    @pyqtSlot()
    def on_btnLogin_clicked(self):
        ip = self.lineEditIp.text()
        port = self.lineEditPort.text()

        if ip == "...":
            ip = ""
        if not port:
            QMessageBox.information(self, "输入错误", '请填写完整。', QMessageBox.Ok)
            return
        addr = (ip, int(port))
        self.uiChatServerLogic = Ui_ChatServer_Logic(self, addr)

    def slot_loginSingnal(self, error):
        if not error:  # 连接成功
            self.uiChatServerLogic.show()
            self.close()
        else:  # 连接出现异常错误
            QMessageBox.critical(self, "连接失败", error, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(argv)
    window = Ui_Login_Logic()
    window.show()
    exit(app.exec_())
