"""
开始: 2018.7.5
问题: 1.如果程序启动慢,应该可以把无关的控件在线程里面启动
      2 其实应该写两个类,有几个界面写内个类
      3.出现一次聊天记录框日期格式bug
      4.每月7, 14, 21, 28自动更新头像报错:FileExistsError: [WinError 183] 当文件已存在时，无法创建该文件。: '微信好友头像/〃那刻温存丶'
      5.发送和收到消息在聊天记录框的排版,可以写一个方法减少代码
      6.点击更新数据后添加好友时，出现已经添加过此好友，经测试，其它相当于添加两次此好友
"""
import itchat
from sys import argv, exit
from os import listdir, mkdir
from time import localtime, time, ctime
from datetime import datetime
from threading import Thread
from PyQt5.QtCore import Qt, QFile, QTimer, QBasicTimer, pyqtSignal, QRegExp, QMimeData, QUrl, QSize
from PyQt5.QtGui import QIcon, QMovie, QColor, QPalette, QBrush, QIntValidator, QPixmap, QRegExpValidator, QImage, \
    QTextCursor, QTextDocument, QTextFrameFormat, QFont
from PyQt5.QtWidgets import (qApp, QLabel, QMainWindow, QPushButton, QWidget, QFrame, QGridLayout, QGroupBox,
                             QDockWidget, QListWidget, QLineEdit, QAction, QComboBox, QFormLayout, QHBoxLayout,
                             QListView, QMessageBox, QApplication, QSplashScreen, QScrollArea, QCheckBox,
                             QDesktopWidget, QTextEdit, QVBoxLayout, QListWidgetItem)

class Ui_Widget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        # 导入QSS文件
        file = QFile('itchatQSS.qss')
        file.open(QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = str(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        # 绘制主界面
        self.setupUi()

    def setupUi(self):
        """主界面"""
        self.setWindowTitle("多人聊天")
        self.setWindowIcon(QIcon("images/0-1.png"))
        self.setFixedHeight(600)    # 进入聊天界面后程序固定高度设为630
        self.setMinimumWidth(343)
        self.setMaximumWidth(1360)  # 本来最大宽度也要设置成360,但不想添加聊天框时重复改成1360
        self.moveCenter(150)        # 因为上面设置最小宽度和最大宽度值不一样,程序得到宽值为640,所以只在这里用到参数150
        # 主界面容器
        mainUi = QFrame(self)
        mainUi.resize(343, 600)
        vbox = QVBoxLayout(self)
        mainUi.setLayout(vbox)
        vbox.setAlignment(Qt.AlignCenter)
        # 用户头像label
        self.headImg = QLabel()
        self.headImg.setScaledContents(True)
        self.headImg.setPixmap(QPixmap(f"微信好友头像/〃那刻温存丶/〃那刻温存丶.jpg")) # 如果改名字了,这里得手动改名字
        self.headImg.setFixedSize(150, 150)
        # 用户昵称label
        self.userName = QLabel()
        self.userName.setFixedSize(150, 150)
        # 登录微信button
        self.btnLogin = QPushButton('登录微信')
        self.btnLogin.clicked.connect(lambda:itchat.auto_login(hotReload=True, loginCallback=self.login))
        self.btnLogin.setFixedSize(150, 60)
        # 显示QDockWidget的按钮,登录微信后才显示
        self.showDock = QPushButton()
        self.showDock.setObjectName('showDock')
        self.showDock.setFixedSize(150, 150)
        # 其它账号登录button
        self.btnOtherLogin = QPushButton('其它账号登录')
        self.btnOtherLogin.clicked.connect(self.otherLogin)
        self.btnOtherLogin.setFixedSize(150, 30)
        # 更新数据button,登录微信后才显示
        self.weChatUpdata = QPushButton('更新数据')
        self.weChatUpdata.setFixedSize(150, 30)
        # 把上面创建的控件添加到垂直布局vbox里
        vbox.addWidget(self.headImg)
        vbox.addWidget(self.userName)
        vbox.addWidget(self.btnLogin)
        vbox.addWidget(self.showDock)
        vbox.addStretch(1) # 这里添加伸展系数就可以把后面添加的控件推到边上
        vbox.addWidget(self.btnOtherLogin)
        vbox.addWidget(self.weChatUpdata)
        # 设置一个QDockWidget控件,里面添加一个带图片列表的列表QListWidget
        self.dock = QDockWidget(self)
        widget = QWidget()
        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)
        self.search = QLineEdit()
        self.search.textChanged[str].connect(self.searchFriend)
        self.friendList = QListWidget()
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.friendList)
        widget.setLayout(self.layout)
        self.dock.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.showDock.clicked.connect(self.dock.show)    # 槽函数为PyQt自带的show方法
        # 初始界面需要隐藏的控件
        self.dock.hide()
        self.userName.hide()
        self.showDock.hide()
        self.weChatUpdata.hide()
        # 聊天界面QFrame,第一次双击好友添加聊天框时,设置为中心窗口
        self.chatUi = QFrame()                   # 创建聊天界面框架
        self.chatUi.setMaximumWidth(1360)        # 保证了内层frame中滚动条右边的箭头能显示,对应设置主界面的最大宽度
        self.frameGrid = QFrame()                # 内层frame
        self.frameGrid.setObjectName("frameGrid")
        self.frameGrid.setMinimumWidth(333)      # 滚动条水平空间,值越大空间越大,后面动态控制,为了屏幕能显示全部时,不出现水平滚动条
        self.frameGrid.setFixedHeight(592)       # 这个值保证垂直滚动条显示不出来,
        self.grid = QGridLayout()                # 创建一个网格布局
        self.grid.setAlignment(Qt.AlignLeft)     # 让QGridLayout添加的控件靠左显示,不然默认居中均匀分布
        self.grid.setSpacing(2)                  # 设置了网格之间的间距
        self.grid.setContentsMargins(0, 0, 0, 0) # 设置网格布局的外边距
        self.frameGrid.setLayout(self.grid)      # 内层frame设置布局为创建好的网格布局
        scroll = QScrollArea()                   # 创建一个滚动条
        scroll.setWidget(self.frameGrid)         # 把滚动条设置在内层frame上
        vbox = QVBoxLayout()                     # 创建一个垂直布局(好像这里创建什么布局都行)
        vbox.addWidget(scroll)                   # 把滚动条添加到垂直布局里
        self.chatUi.setLayout(vbox)              # Ui框架(聊天界面frame)设置创建好的垂直布局
        # 后面代码要用到的动态数据
        self._count = 0      # 计数用(添加删除聊天框时)
        self._widget = 0     # 用于动态设置界面的宽, 238 + 100

        self.frameD = dict() # {"职梦君": {"replay": "QTextEdit()","sendMsg": "QTextEdit()"} ...}

    def login(self):
        """微信登录的回调函数:loginCallback=self.login"""
        day = localtime(time())[2]               # 某月的第几天
        dayList = [7, 14, 21, 28]
        # 判断是否需要启动线程更新数据
        self.friendsInfo = itchat.get_friends()[0:]         # 得到用户微信的所有信息
        self.nickNameSelf = self.friendsInfo[0]['NickName'] # 得到用户的微信昵称
        tempPath = listdir('微信好友头像/')
        if self.nickNameSelf not in tempPath:               # 如果没有这个用户的头像目录, 就创建一个,并下载头像数据
            try:
                t1 = Thread(target=self.threadUpdata)
                t1.start()
            except Exception as e:
                self.weChatUpdata.setText(f"程序更新错误!")
        # elif  day in dayList:                               # 每月7, 14, 21, 28号更新一次数据
        #     t1 = Thread(target=self.threadUpdata)
        #     t1.start()
        # 如果手机上更改了头像,这里又更新了数据,就很有必要把头像再设置一遍
        self.headImg.setPixmap(QPixmap(f"微信好友头像/{self.nickNameSelf}/{self.nickNameSelf}.jpg"))
        self.userName.setText(f"<h1>{self.nickNameSelf}</h1>")
        # 执行给QDockWidget添加数据列表的方法,登录了才会有数据.并把它显示出来.
        self.dockAddData()
        self.dock.show()
        # 实例化一个更新头像数据的线程,添加到更新数据button的槽
        self.tUpdata = Thread(target=self.threadUpdata, args=(True,)) # 专为更新按钮设置的线程
        self.weChatUpdata.clicked.connect(self.tUpdata.start)         # 更新按钮绑定点击事件为线程的开始方法
        # 隐藏登录button,显示头像label,昵称label,QDockWidget,数据更新button
        self.btnLogin.hide()
        self.headImg.show()
        self.userName.show()
        self.showDock.show()
        self.weChatUpdata.show()
        # 给itchat.run()方法一个线程,添加好友聊天时启动,前提要先加载下面的装饰函数,run()方法所需要的
        self.tRun = Thread(target=itchat.run)
        self.tRun.setDaemon(True)

        @itchat.msg_register(itchat.content.TEXT)
        def friend_replay(msg):
            # 得到时间
            now = datetime.now()
            _time = f"{now.hour}:{now.minute}:{now.second}"
            # 得到消息来源(此好友)的全部情报
            replay = msg["Text"]  # 好友的消息       msg["FromUserName"]:消息来源的UserName
            friend = itchat.search_friends(userName=msg["FromUserName"])
            # 如果有有备注名就用,否则用昵称
            if friend['RemarkName']:
                friendName = friend['RemarkName']
            else:
                friendName = friend['NickName']  # 从情报中得到好友的昵称
            # try:
            #     if friendName not in self.frameD.keys():
            #         self.friendChat(friendName)
            # except Exception as e:
            #     print(e)
            # 如果焦点不在此好友输入框内,此好友就排在好友列表第1位并显示背景透明红
            if self.focusWidget() != self.frameD[friendName]["sendMsg"]:
                item = self.friendList.findItems(friendName, Qt.MatchContains)[0]
                self.friendList.takeItem(self.friendList.row(item))
                self.friendList.insertItem(0, item)
                item.setBackground(QColor(QColor(255,0,0, 70)))
            # 好友消息在聊天记录框的排版
            self.frameD[friendName]["replay"].setAlignment(Qt.AlignLeft) # 好友的消息在聊天记录框的左侧显示
            self.frameD[friendName]["replay"].insertPlainText("\n")  # 插入空格,不然会在右边显示(因自己的消息设置靠右了)
            self.frameD[friendName]["replay"].append(                    # 插入好友的头像
                f'<img src=\"微信好友头像/{self.nickNameSelf}/{friendName}.jpg\" height="50" width="50" />')
            self.frameD[friendName]["replay"].append(f'{_time}')         # 在头像下面插入发送时间
            self.frameD[friendName]["replay"].append(f'<font style="background-color:rgba(255,0,0,50);" '
                                                     f'face="隶书" color="green" size="7">{replay}</font>')
            self.frameD[friendName]["replay"].insertPlainText("\n")  # 插入空格,不然会在右边显示(因自己的消息设置靠右了)
            self.frameD[friendName]["replay"].verticalScrollBar().setValue(
                self.frameD[friendName]["replay"].verticalScrollBar().maximum()) # 让聊天记录框每次移动到最后,这里不管用

            print(friend['NickName'], replay)

    def otherLogin(self):
        """其它用户登录按钮的槽函数"""
        itchat.logout() # 先执行退出,再登录(这里设置自动登录为False,登录返回函数还是itchatLogin)
        itchat.auto_login(hotReload=False, loginCallback=self.login)

    def friendChat(self, obj):
        """
        添加此好友聊天框,QListWidget的itemDoubleClicked信号的槽函数(双击好友时执行的方法)
        :param obj: 就是某一个item,item.text()就是好友的名字(obj.text())
        :return: QGridLayout添加此好友的聊天框
        """
        # print(obj.text(), "\n基数:", self._count, "\n_count:", self.grid.count())
        friendName = obj.text()
        self.setCentralWidget(self.chatUi) # 进入聊天界面
        self.setFixedHeight(630)           # 增加点程序的固定高度,在取消聊天界面后再恢复为600
        self.grid.addWidget(self.addFrame(friendName), 0, self._count) # 添加聊天框
        if self.tRun.isAlive() == False:   # 如果这个线程没有启动,就启动
            self.tRun.start()

    def addFrame(self, friendName):
        """双击好友添加此好友的聊天框"""
        # 防止重复添加同一个好友,如果重复直接返回,不再执行添加动作
        if friendName in self.frameD.keys():
            QMessageBox.information(self, "提示", f"好友[{friendName}]已存在!。")
            return

        self._count += 1
        self._widget += 353  # 333 + 10
        self.resize(self._widget, 630) # 让程序界面能跟着变宽,已经设置程序界面最大宽度为1360,所以不怕这个值无限变大
        self.frameGrid.setMinimumWidth(int(self._widget / 353) * 333) # 对应下面333,若变大添加第一个好友会显示水平滚动条
        self.moveCenter()              # 每次Ui界面宽度增加时都能让Ui界面在屏幕中间,要在Ui动态设置过宽度之后执行才能准确
        # 整个聊天框容器,里面用一个垂直布局,垂直布局中再添加四个水平布局构成
        frame = QFrame()
        frame.setObjectName(friendName)
        frame.setFixedSize(333, 600)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 10)
        vbox.setSpacing(1)
        frame.setLayout(vbox)
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        vbox.addLayout(hbox1, 6)                # 第二个参数是权重占比, 6/(6+1+2+1)
        vbox.addLayout(hbox2, 1)
        vbox.addLayout(hbox3, 2)
        vbox.addLayout(hbox4, 1)
        # 聊天记录框
        replay = QTextEdit()
        replay.setObjectName('replayChat')
        replay.setReadOnly(True)                 # 设置为只读模式
        hbox1.addWidget(replay)
        # 功能按钮
        # a = [self.delFrame, self.dock.show]
        for i in range(1, 7):
            btn = QPushButton()
            btn.setObjectName(f'btnFunc{str(i)}') # 设置类名,以便QSS中设计样式
            btn.setFixedSize(30, 30)
            if i == 5:
                btn.clicked.connect(lambda : self.delFrame(friendName))
                hbox2.addStretch(1)
            if i == 6:
                btn.clicked.connect(self.dock.show)
            hbox2.addWidget(btn)
        # 发送消息的输入框
        sendMsg = QTextEdit()
        sendMsg.setObjectName('sendMsg')
        sendMsg.installEventFilter(self) # 自己写回车事件
        hbox3.addWidget(sendMsg)
        # 左下角头像,编号,昵称三个label
        lab1 = QLabel()
        lab1.setFixedSize(30, 30)
        lab1.setScaledContents(True)
        lab1.setPixmap(QPixmap(f"微信好友头像/〃那刻温存丶/{friendName}.jpg"))
        lab2 = QLabel(str(self._count))
        lab3 = QLabel(friendName)
        hbox4.addWidget(lab1)
        hbox4.addWidget(lab2)
        hbox4.addWidget(lab3)
        # 发送按钮
        sendBtn = QPushButton()
        sendBtn.setObjectName('sendBtn')
        sendBtn.setFixedSize(60, 30)
        sendBtn.clicked.connect(lambda : self.sendMSG(friendName))
        hbox4.addStretch(1)
        hbox4.addWidget(sendBtn)
        # 给字典frameD添加一个key(friendName),value(另一个字典),并给内层字典添加key(自己定义的字符串),value(两个QTextEdit)
        self.frameD[friendName] = dict()
        self.frameD[friendName]["replay"] = replay
        self.frameD[friendName]["sendMsg"] = sendMsg
        return frame

    def delFrame(self, friendName):
        """点击减号删除此好友聊天框"""
        from sip import delete
        parent = self.sender().parent()  # 删除按钮的父级,也就是聊天框frame
        # self.grid.removeWidget(parent) # 删除控件,并用sip库中的delete方法再删除一次才能把frame下的子控件全清除 **下面
        # 的for循环把grid重新添加元素,就不用这句删除控件了,相当于更新了一下界面,所以就不存在这个元素了
        delete(parent) # 只用这一句就行,没下面for循环更新元素的话,还需要上面注释掉的代码

        # 如果等于353,让基数恢复0,就直接返回不再执行后面的语句.上面已经把控件删除过了.
        if self._count == 1: # 其实还可以判断len(self.frameGrid.children())是否等于1,如果是就take,看下面的注释
            try:
                self.takeCentralWidget() # self._widget变成706了,不知道怎么回事
                self.setFixedHeight(600)
                self._count = 0
                self._widget = 0
                self.frameD.clear()
                return
            except Exception as e:
                print(e)
        # self.frameGrid.children()[0]就是self.grid,self.frameGrid.children()[1:]就是每个好友的聊天框frame
        # 直接从self.grid找子元素显示为[],空的,所以从它的父级找到了每个聊天框,其实找到的都是ID,ID都是唯一的,不可能重复
        # 重新让self.grid横向从0顺序再排列一次,再从聊天框得到子元素序号label,跟着索引重新编号
        for index, widget in enumerate(self.frameGrid.children()[1:]):
            widget.children()[10].setText(str(index+1)) # 从聊天框得到子元素序号label,跟着索引重新编号
            self.grid.addWidget(widget, 0, index)     # 重新让self.grid横向从0顺序再排列一次
        self._count = index # 把循环内index的最终值给_count,这样在添加聊天框里再加1就能顺利把序号label编号了

        self._widget -= 353
        self.resize(self._widget, 630)
        self.frameGrid.setFixedWidth(int(self._widget / 353) * 333)
        self.moveCenter()              # 每次Ui界面宽度减少时都能让Ui界面在屏幕中间,要在Ui动态设置过宽度之后执行才能准确
        del self.frameD[friendName]    # 把字典中此好友的信息也删除,用于不能重复添加一个好友的聊天框

    def sendMSG(self, friendName):
        """发送按钮以及按回车事件的槽函数"""
        now = datetime.now()
        # date = now.date() # 2018-7-14
        _time = f"{now.hour}:{now.minute}:{now.second}"
        sendMsg = self.frameD[friendName]["sendMsg"].toPlainText()      # 得到发送框的内容

        self.frameD[friendName]["replay"].setAlignment(Qt.AlignRight)   # 让发送的消息在聊天记录框的右边显示
        self.frameD[friendName]["replay"].insertPlainText("\n")         # 插入一个空格,不然第一行总是会在左边显示
        self.frameD[friendName]["replay"].append(                       # 插入自己的头像
            f'<img src=\"微信好友头像/{self.nickNameSelf}/{self.nickNameSelf}.jpg\" height="50" width="50" />')
        self.frameD[friendName]["replay"].append(f'{_time}')   # 在头像下面插入发送时间
        self.frameD[friendName]["replay"].append(f'<font style="background-color:rgba(0,255,0,50);" '
                                                 f'face="隶书" color="black" size="7">{sendMsg}</font>')
        self.frameD[friendName]["replay"].insertPlainText("\n")         # 插入一个空格,不然第一行总是会在左边显示
        self.frameD[friendName]["replay"].verticalScrollBar().setValue(  # 让聊天记录框每次移动到最后
            self.frameD[friendName]["replay"].verticalScrollBar().maximum())

        friendInfo = itchat.search_friends(name=friendName)             # 搜索此好友的全部情报
        userName = friendInfo[0]['UserName']                            # 得到此好友的UserName值
        itchat.send(sendMsg, toUserName=userName)                       # 给此人发送消息
        self.frameD[friendName]["sendMsg"].clear()                      # 每次发送消息后清除发送框内容
        # self.frameD[friendName]["sendMsg"].moveCursor(QTextCursor.Start))
        # self.frameD[friendName]["replay"].scrollToBottom()


        print("发送:", sendMsg)

    def dockAddData(self):
        """为了每次更新数据时能把QDockWidget里面的数据也更新,所以把QDockWidget内部单独写进函数,方便更新时调用"""
        names = listdir(f'微信好友头像/{self.nickNameSelf}/')  # 路径
        self.dock.setWindowTitle(f'共 {len(names)} 位好友')    # self.friendList.count()也能统计列表项数
        self.friendList.setIconSize(QSize(40,40))
        # self.friendList.clear()
        for name in names:
            item = QListWidgetItem(QIcon(f"微信好友头像/{self.nickNameSelf}/{name}"), name[:-4]) # 温存.jpg
            self.friendList.addItem(item)
        self.friendList.sortItems()
        self.friendList.itemDoubleClicked.connect(self.friendChat)
        # self.showDock.clicked.connect(self.dock.show)

    def searchFriend(self, friendName):
        filterItems = self.friendList.findItems(friendName, Qt.MatchContains) # 遍历符合字符串的好友
        allItems = self.friendList.findItems('', Qt.MatchContains)      # 全部好友
        # all_items = self.list.findItems(text, Qt.MatchExactly)
        # all_items = self.list.findItems('', Qt.MatchRegExp)
        for item in allItems:
            if item in filterItems:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def eventFilter(self, obj, e):
        """发送消息框绑定的installEventFilter(self)事件"""
        if e.type() == e.FocusIn:
            try:
                friendName = obj.parent().objectName()
                item = self.friendList.findItems(friendName, Qt.MatchContains)[0]
                # self.friendList.takeItem(self.friendList.row(item))
                # self.friendList.insertItem(0, item)
                item.setBackground(Qt.transparent)
            except Exception as e:
                print(e)

        if obj != self and e.type() == e.KeyPress: # obj != self 根据网上obj == self改的,不知道具体涵义.KeyPress键盘事件
            if e.key() == Qt.Key_Return and e.modifiers() == Qt.AltModifier:
                obj.insertPlainText('\n')          # 按Alt+回车(Return指大键盘的回车,Key_Enter是小键盘的回车)时,插入换行
                return True
            elif e.key() == Qt.Key_Return:         # 如果只按回车键,发送消息
                self.sendMSG(obj.parent().objectName())
                return True                        # 这里返回True,解决了按回车发送消息之后,一直空一行
            else:
                return False                       # 这两个return不能忘记加上,不然报错
        else:
            return False
        #     if QEvent.key() == QEvent.FocusOut: # & (QEvent.modifiers() & Qt.ControlModifier):
        #         print(QObject.objectName())

    def threadUpdata(self, weChatUpdata=False):
        """线程:下载好友头像到指定文件夹,方便QListWidget列表框显示"""
        baseNum = 1                      # 基数,方便计算显示下载百分比
        totalNum = len(self.friendsInfo) # 好友总数
        # 点击更新数据按钮时,删除此用户的头像文件夹,再创建一个,下面重新下载头像数据
        if weChatUpdata == True:
            from shutil import rmtree # 这个库方法可以删除目录包括里面的文件,os中的rmdir只能删除空目录
            self.dock.hide()
            # self.friendList.reset()
            self.friendList.clear()   # 点击更新数据后添加好友时，出现已经添加过此好友，经测试，其它相当于添加两次此好友
            rmtree(f'微信好友头像\{self.nickNameSelf}')

        mkdir(f"微信好友头像/{self.nickNameSelf}")
        for i in self.friendsInfo:
            img = itchat.get_head_img(userName=i['UserName'])
            if i['RemarkName'] != '':
                path = f"微信好友头像/{self.nickNameSelf}/{i['RemarkName']}.jpg"
            else:
                path = f"微信好友头像/{self.nickNameSelf}/{i['NickName']}.jpg"

            try:
                # 写入每个头像数据，并设置一个进度显示
                with open(path, 'wb') as f:
                    f.write(img)
                    progress = baseNum/totalNum * 100
                    self.weChatUpdata.setText(f"数据更新中    {int(progress)}%")
                    baseNum += 1
            except Exception as e:
                self.weChatUpdata.setText(f"程序更新错误!")
        # if weChatUpdata == True:
        self.layout.addWidget(self.friendList)
        self.headImg.setPixmap(QPixmap(f"微信好友头像/{self.nickNameSelf}/{self.nickNameSelf}.jpg"))
        self.dockAddData()
        self.dock.show()
        self.weChatUpdata.setText(f"更新数据")

    def moveCenter(self, num=0):
        """实现窗体在屏幕中央. num只在启动程序时传值150,原因看调用注释"""
        screen = QDesktopWidget().screenGeometry()  # QDesktopWidget为一个类，调用screenGeometry函数获得电脑屏幕的尺寸
        uiSize = self.geometry()                    # Ui界面的尺寸
        self.move((screen.width() - uiSize.width()) / 2 + num,
                  (screen.height() - uiSize.height()) / 2 - 50)



app = QApplication(argv)                        # 固定写法: 还不知道确切含义
splash=QSplashScreen(QPixmap("images/0-0.jpg").scaled(300, 300, Qt.KeepAspectRatioByExpanding)) # 设置启动界面
splash.show()                                   # 显示启动画面
window = Ui_Widget()                            # 实例化此MainRun类
window.show()                          # 全屏显示(窗口透明方法,在此后设置window.setWindowOpacity(0.1),值为0-1之间)
splash.finish(window)                           # 主窗体对象初始化完成后，结束启动画面
exit(app.exec_())                               # 固定写法: 添加退出方法