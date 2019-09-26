import json
from sys import argv
import socket  # 客户端不需要执行导入gevent的socket和monkey

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QVBoxLayout, QListWidgetItem

from client.Flag import Flag as F
from client.Ui_ChatSocket import Ui_ChatSocket
from client.Ui_Login import Ui_Login
from client.Ui_Edit import Ui_Edit

import cgitb

cgitb.enable(format='text')


class ChatClient(QThread):
    def __init__(self, friendSingnal, recvSingnal, closeSingnal, loginSingnal, loginData):
        super().__init__()
        self.friendSingnal = friendSingnal
        self.recvSingnal = recvSingnal
        self.closeSingnal = closeSingnal
        self.loginSingnal = loginSingnal
        self.loginData = loginData

    def run(self):
        try:
            # 创建套接字，不能在init中，必须在此方法内。可以跟创建线程时就初始化套接字有关，
            # 好像是线程没start时，不可以创建套接字。
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(2)
            self.client.connect(self.loginData['addr'])  # 建立连接
        except Exception as e:
            # 处理*未连接*服务器时，发出“错误弹窗”,已连接的异常捕获在else语句里
            self.loginSingnal.emit({"flag": F.Error, "error": str(e)})  # 单发一个字典
            self.exit()  # 退出线程
        else:
            # 客户端连接服务器成功后，发送登录数据，然后下面接收数据循环内，得到服务器对比数据库后的认证反馈
            self.client.send(bytes(json.dumps(self.loginData), encoding='utf-8'))

            while True:
                try:
                    data = self.client.recv(1024)  # 接收消息

                    if not data:
                        break
                    dataLoads = json.loads(data.decode())  # 先解码数据，再用json方法转化为字典
                    flag = dataLoads['flag']
                    if flag == F.MsgText:  # 把这条件放在上面，已经认证通过登录后，处理最多的是聊天数据的发送。
                        self.recvSingnal.emit(dataLoads)
                    elif flag == F.NewFriend or flag == F.OnlineFriend or flag == F.FriendExit:
                        self.friendSingnal.emit(dataLoads)
                    elif flag == F.LoginSuccess:
                        self.loginSingnal.emit(dataLoads)  # 把客户数据资料全部传给客户
                    elif flag == F.LoginFailed:
                        self.loginSingnal.emit({"flag": F.LoginFailed})  # 单发一个字典

                except WindowsError as e:
                    if e.errno == 10038 or e.errno == 10054:
                        break
                    print("接收消息", e)
            # 这里的位置是否可以放在e.errno判断下
            self.closeSingnal.emit()


class Ui_ChatServer_Logic(QWidget, Ui_ChatSocket):
    friendSingnal = pyqtSignal(dict)  # 详细文档看此信号槽
    recvSingnal = pyqtSignal(dict)  # 接收消息信号
    closeSingnal = pyqtSignal()  # 断开客户端套接字信号

    def __init__(self, parent, loginData):
        super(Ui_ChatServer_Logic, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.p = parent
        self.loginData = loginData
        self.friendsData = dict()

        # 设置分割界面的初始比例(索引0，2/(2+5),索引1，5/(2+5))
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 8)

        # 因为设计师创建的stackedWidget，自带了两个子widget。为了动态添加子页时，统一
        # 格式，所以要删除掉。
        self.p0.deleteLater()
        self.p1.deleteLater()
        del self.p0, self.p1

        # 自定义信号连接槽
        self.friendSingnal.connect(self.slot_friendSingnal)
        self.recvSingnal.connect(self.slot_recvSingnal)
        self.closeSingnal.connect(self.slot_closeSingnal)

        # 创建线程。线程里启动socket连接
        self.chatClient = ChatClient(self.friendSingnal, self.recvSingnal, self.closeSingnal, parent.loginSingnal,
                                     loginData)
        self.chatClient.start()  # 线程开始

    @pyqtSlot()
    def on_btnSend_clicked(self):
        try:
            print("+++++++++++", self.friendsData)
            # print("+++++++++++", self.loginData)
            row = self.listWidget.currentRow()
            sendToId = self.listWidget.item(row).data(888)
            sendEdit = self.friendsData[sendToId]['uiEdit'].textEditSend
            text = sendEdit.toPlainText()
            d = {
                'flag': F.MsgText,
                'fromId': self.loginData['id'],
                'sendToId': sendToId,
                'msgText': text
            }
            print(d)
            # 空数据套接字会自动屏蔽，所以不用再做判断了。
            self.chatClient.client.send(bytes(json.dumps(d), encoding='utf-8'))  # 发送消息
        except Exception as e:
            QMessageBox.critical(self, "发送失败", str(e), QMessageBox.Ok)
        else:
            sendEdit.clear()

    @pyqtSlot(int)
    def on_listWidget_currentRowChanged(self, index):
        """
        所有客户端聊天框(和stackedWidget中对应索引的widget)只有在点击listWidget对应的item项时，才创建实例，感觉这样省资源。
        客户端在主动或者被动退出时，已经处理删除对应的item了，并且还彻底删除了对应widget和他的实例变量了。
        """
        # item = self.listWidget.item(index)  # 通过行号得到QListWidgetItem对象
        # self.lineEditIp.setText(item.data(886))  # 取出存入的枚举886(ip地址)数据
        # self.lineEditPort.setText(item.data(887))  # 枚举887(port号)
        self.stackedWidget.setCurrentIndex(index)

    @pyqtSlot()
    def on_btnChangeId_clicked(self):
        reply = QMessageBox.information(self, "断开连接", "你确定要断开服务器，返回登录界面吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == 65536:
            return

        # 客户端在主动关闭套接字(非断网或者直接退出程序)时，会不停发送空数据，然后服务器
        # 里的协程的此会不停的接受空数据，也就是此上面的data，造成程序崩溃，所以需要把此
        # 客户端在服务器端再关闭一次，判断接收的是否空数据，如果是就关闭客户端。突然觉得
        # 好像gevent库的作者本身就是这样设计的。
        self.chatClient.client.close()  # 客户端关闭套接字，会不停的发送空数据。
        self.chatClient.exit()  # 退出线程
        self.chatClient.deleteLater()  # 删掉实例化的线程对象

        self.listWidget.clear()
        self.p.show()
        self.close()

    def slot_friendSingnal(self, friendData):
        def setEdit(data):
            # 给每个好友创建单独的聊天界面
            uiEdit = Ui_Edit_Logic(self.stackedWidget)
            self.stackedWidget.addWidget(uiEdit)
            item = QListWidgetItem(data['nickname'])
            item.setData(888, data['id'])  # 聊天框对象
            self.listWidget.addItem(item)

            self.friendsData[data['id']] = {
                'uiEdit': uiEdit,
                'item': item,
                'nickname': data['nickname'],
                'addr': data['addr']
            }

        flag = friendData['flag']
        if flag == F.NewFriend:  # 自己是在线状态时，接收服务器发来的新客户端信息
            setEdit(friendData)
        elif flag == F.OnlineFriend:  # 自己刚登录时，接收服务器发来的已经在线好友的信息
            for v in friendData['onlineFriend'].values():
                setEdit(v)
        elif flag == F.FriendExit:  # 自己是在线状态时，接收服务器发来的某个好友退出的id号
            socId = friendData['fromId']
            uiEdit = self.friendsData[socId]['uiEdit']
            item = self.friendsData[socId]['item']
            self.stackedWidget.removeWidget(uiEdit)  # 删除此客户的聊天页面
            self.listWidget.takeItem(self.listWidget.row(item))  # 删除此行
            uiEdit.deleteLater()
            del uiEdit  # 彻底删除编辑界面
            self.friendsData.pop(socId)  # 删除此客户的键值

    def slot_recvSingnal(self, data):
        flag = data["flag"]
        if flag == F.MsgText:  # 再判断if  data['msgText'] == 1
            idData = self.friendsData[data['fromId']]
            text = f"{idData['nickname']}\n{data['msgText']}\n\n"
            editRecv = idData['uiEdit'].textEditRecv
            editRecv.insertPlainText(text)
            editRecv.verticalScrollBar().setSliderPosition(editRecv.verticalScrollBar().maximum())

    def slot_closeSingnal(self):
        QMessageBox.critical(self, "连接断开", "连接意外断开，请再次尝试连接服务器", QMessageBox.Ok)
        self.p.show()
        self.deleteLater()  # 彻底删除聊天界面，也就关闭了，close方法可能不会彻底删除吧
        del self  # 彻底删除后，里面的字典数据就不存在了，不用一个个清空了

    @pyqtSlot()
    def on_btnAddFriend_clicked(self):
        # 以后想写这功能了再说吧，目前是把局域网内在线的客户端，全部显示在好友列表
        pass


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
    loginSingnal = pyqtSignal(dict)  # 连接服务器,服务器检查账号密码。在Ui_ChatServer_Logic的init中创建线程时传入。
    serverIp = '192.168.31.112'
    serverPort = '7777'

    def __init__(self):
        super(Ui_Login_Logic, self).__init__()
        self.setupUi(self)
        self.lineEditPort.setValidator(QIntValidator(1, 9999))

        self.loginSingnal.connect(self.slot_loginSingnal)
        self.btnGoSignIn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btnBack.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        # 这五行仅方便测试用，项目完成时删掉即可
        self.lineEditIp.setText(self.serverIp)
        self.lineEditPort.setText(self.serverPort)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.lineEditId.setText('1')
        self.lineEditPswd.setText('123')

    @pyqtSlot()
    def on_btnLogin_clicked(self):  # 登录账号
        ip = self.lineEditIp.text()
        port = self.lineEditPort.text()
        _id = self.lineEditId.text()
        pswd = self.lineEditPswd.text()

        # 如果信息没有填写完整就返回
        if not ip or not port or not _id or not pswd:
            QMessageBox.information(self, "输入错误", '请填写完整。', QMessageBox.Ok)
            return

        # 信息填写完整时，把登录数据传给聊天界面，让它在聊天界面init的时候与服务器进行交互取得认证，
        # 在聊天界面创建线程连接服务器时，把登录界面自定义的信号loginSingnal传入线程，认证完成就通
        # 过此信号的槽slot_loginSingnal判断认证通过与否的后续处理。
        loginData = {
            "addr": (ip, int(port)),
            "id": _id,
            "password": pswd,
            'flag': F.Login
        }
        self.uiChatServerLogic = Ui_ChatServer_Logic(self, loginData)

    def slot_loginSingnal(self, userData):
        if userData['flag'] == F.Error:  # 异常提示，客户端网络中断，或者服务器未开启
            QMessageBox.critical(self, "连接失败", userData["error"], QMessageBox.Ok)
        elif userData['flag'] == F.LoginSuccess:  # 认证通过就关闭登录界面，show出聊天界面
            self.uiChatServerLogic.slot_friendSingnal(
                {'id': 'admin', 'nickname': '管理员', 'addr': ('192.168.31.112', 7777), 'flag': F.NewFriend})
            self.uiChatServerLogic.listWidget.setCurrentRow(0)  # 设置listWidget第0行被选中(这样符号stackedWidget第0页部件创建显示出来时的视频逻辑)
            self.uiChatServerLogic.setWindowTitle(userData["nickname"])
            self.uiChatServerLogic.show()
            self.close()
        elif userData['flag'] == F.LoginFailed:  # 认证失败，弹出提示
            QMessageBox.critical(self, "登录失败", '账号或密码错误', QMessageBox.Ok)

    @pyqtSlot()
    def on_btnSignIn_clicked(self):  # 开始注册账号
        print('注册好了')


if __name__ == '__main__':
    app = QApplication(argv)
    window = Ui_Login_Logic()
    window.show()
    exit(app.exec_())
