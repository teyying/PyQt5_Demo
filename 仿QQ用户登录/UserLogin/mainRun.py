from sys import argv
from PyQt5.QtCore import Qt, QSize, QPoint, QBasicTimer, QUrl
from PyQt5.QtGui import QMovie, QIcon, QPixmap, QFont, QIntValidator, QCursor, QBrush, QPalette, QImage, QBitmap, \
    QPainter, QColor, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QLineEdit, QComboBox, QListView, QLabel, QPushButton, QMenu, \
    QGridLayout, QFrame
from Ui_Login import Ui_Login
from menuKeyBoard import Ui_menuKeyBoard

# 改变self.flagCapsLock为False，然后使用if self.flagCapsLock或者if not self.flagCapsLock
# self.labFrameQRcodeErrorImg的出现还没设置

USER_ID = '165227316'
USER_LOGINED_ON = True

class Login(QWidget, Ui_Login):
    def __init__(self):
        super(Login, self).__init__()

        self.setupUi(self)
        self.flagMove = False
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉标题栏的代码,这种顶部就不会出现空白,但是不能移动，需自己处理
        self.movie = QMovie('image/login/0.gif')
        self.label_2.setMovie(self.movie)
        self.movie.start()

        # 用户头像的一系列效果设置
        self.myQPushButton = MyQPushButton(self.slot_myQPushButton, self.frameGlobal) # 重写的QPushButton类
        self.myQPushButton.setGeometry(234, 142, 16, 16)
        self.myQPushButton.setObjectName('myQPushButton')
        self.myQPushButton.setIcon(QIcon('image/login/8.png'))  # 默认的icon，可以从数据库中根据条件选择

        self.labUserImg_orgin_enterEvent = self.labUserImg.enterEvent # 鼠标移入用户头像
        self.labUserImg_orgin_leaveEvent = self.labUserImg.leaveEvent # 鼠标离开用户头像
        self.btnAddUser_orgin_enterEvent = self.btnAddUser.enterEvent # 鼠标移入滑出的添加账号按钮
        self.btnAddUser_orgin_leaveEvent = self.btnAddUser.leaveEvent # 鼠标离开滑出的添加账号按钮
        self.labUserImg.enterEvent = self.labUserImg_EnterEvent # 绑定函数
        self.btnAddUser.enterEvent = self.btnAddUser_EnterEvent
        self.btnAddUser.leaveEvent = self.btnAddUser_LeaveEvent
        self.labUserImg.leaveEvent = self.labUserImg_LeaveEvent

        self.timer = QBasicTimer() # 鼠标离开用户头像或者添加账号按钮时的计时器
        self.flagTimer = 0 # 鼠标离开用户头像或者添加账号按钮时的计时器的初始值
        self.timerBtnAddUserMove = QBasicTimer()# 添加账号按钮移动开始至结束的计时事件
        self.btnAddUserX = 203 # 添加账号按钮水平位置x的滑出效果初始标记（这个值原本就是它的x位置）

        # 账号输入下拉列表的设置
        self.comboUserId.setView(QListView()) # 先随便设置一个QListView()，使下拉列表可以设置qss样式
        self.actionLeftUserID = QAction(self.comboUserId)
        self.actionLeftUserID.setIcon(QIcon("image/login/3.png"))
        self.comboUserId.lineEdit().addAction(self.actionLeftUserID, QLineEdit.LeadingPosition) # 左侧图标
        self.comboUserId.lineEdit().setPlaceholderText('账号') # 设置默认提示语
        self.comboUserId.addItem(QIcon("image/login/02.jpg"), "1235321111")
        self.comboUserId.addItem(QIcon("image/login/03.jpg"), "3745634222")
        # self.comboUserID.setItemData(2, QPixmap('image/login/4.png'), Qt.DecorationRole)  # 数据作为图标出现
        # self.comboUserID.setItemIcon(1, QIcon("image/login/4.png"))
        # self.comboUserID.setItemDelegate()
        # self.comboUserID.setItemData(0, 0, Qt.UserRole - 1)  # 锁定第0项。参数3如果是-256，第0项显示空字符
        self.comboUserId.setCurrentIndex(-1) # 下拉列表初始设置为空，这样不用添加一个空的下拉项了
        self.comboUserId.activated[str].connect(self.slot_comboUserID)
        self.comboUserID_orgin_focusInEvent = self.comboUserId.focusInEvent # 账号输入下拉列表获得焦点事件
        self.comboUserId.focusInEvent = self.comboUserID_FocusInEvent # 账号输入下拉列表获得焦点事件的函数绑定
        self.comboUserID_orgin_focusOutEvent = self.comboUserId.focusOutEvent # 账号输入下拉列表失去焦点事件
        self.comboUserId.focusOutEvent = self.comboUserID_FocusOutEvent # 账号输入下拉列表失去焦点事件的函数绑定
        self.comboUserID_orgin_mousePressEvent = self.comboUserId.mousePressEvent # 账号输入下拉列表鼠标按下事件
        self.comboUserId.mousePressEvent = self.comboUserID_MousePressEvent # 账号输入下拉列表鼠标按下事件的函数绑定
        self.flagComboUserID = False  # 点击下拉箭头需要的标记

        # 密码框的设置
        self.actionLeftPassword = QAction(self.lEditPassword)
        self.actionLeftPassword.setIcon(QIcon("image/login/1.png"))
        self.actionRightPassword = QAction(self.lEditPassword)
        self.actionRightPassword.setIcon(QIcon("image/login/17.png"))
        self.actionRightPassword.triggered.connect(self.slot_actionRightPassword)
        self.menuKeyBoard = MyMenu(self)

        self.lEditPassword.addAction(self.actionLeftPassword, QLineEdit.LeadingPosition)  # 左侧图标
        self.lEditPassword.addAction(self.actionRightPassword, QLineEdit.TrailingPosition)  # 右侧图标
        self.lEditPassword.setPlaceholderText('密码')
        self.lEditPassword_orgin_focusInEvent = self.lEditPassword.focusInEvent
        self.lEditPassword.focusInEvent = self.lEditPassword_FocusInEvent
        self.lEditPassword_orgin_focusOutEvent = self.lEditPassword.focusOutEvent
        self.lEditPassword.focusOutEvent = self.lEditPassword_FocusOutEvent

        # 二维码登录界面frame的设置
        self.frameQRcodeUpdata_orgin_enterEvent = self.frameQRcodeUpdata.enterEvent # 鼠标滑入更新二维码容器
        self.frameQRcodeUpdata.enterEvent = self.frameQRcodeUpdata_EnterEvent
        self.frameQRcodeUpdata_orgin_leaveEvent = self.frameQRcodeUpdata.leaveEvent # 鼠标离开更新二维码容器
        self.frameQRcodeUpdata.leaveEvent = self.frameQRcodeUpdata_LeaveEvent
        self.timerFrameQRcodeUpdata = QBasicTimer()
        self.flagTimerFrameQRcodeUpdata = False
        self.flagTimerFrameQRcodeUpdataX = 115
        self.btnFrameQRcodeBack.clicked.connect(self.slot_btnQRcode_btnFrameQRcodeBack)

        # 一些控件的信号与槽的绑定，以及隐藏初始界面不应该显示的控件
        self.btnAddUser.hide() # 先把添加账号按钮隐藏，鼠标移入self.labUserImg时再滑出
        self.btnLoginSingle.hide() # 单账号登录按钮在self.btnAddUser被点击时才显示
        self.frameAdduser.hide() # 此容器内的控件在self.btnAddUser被点击时才显示
        self.frameQRcode.hide()
        self.btnSignIn.clicked.connect(lambda :QDesktopServices.openUrl(QUrl(("https://ssl.zc.qq.com/v3/index-chs.html"))))
        self.btnFindBack.clicked.connect(lambda :QDesktopServices.openUrl(QUrl(("https://aq.qq.com/v2/uv_aq/html/reset_pwd/pc_reset_pwd_input_account.html"))))

        self.btnSetting.clicked.connect(lambda :self.timerError.start(10, self)) # 以后再写设置界面
        self.btnQRcode.clicked.connect(self.slot_btnQRcode_btnFrameQRcodeBack)
        # self.btnQRcode.clicked.connect(lambda :self.timerError.start(10, self))
        self.btnAddUser.clicked.connect(self.slot_btnAddUser_btnLoginSingle)
        # self.btnAddUser.clicked.connect(lambda: self.timerError.start(10, self))
        self.btnLoginSingle.clicked.connect(self.slot_btnAddUser_btnLoginSingle)
        self.btnCancel.clicked.connect(self.slot_btnAddUser_btnLoginSingle)
        self.btnError.clicked.connect(lambda :self.timerError.start(10, self))

        self.btnSetting.clicked.connect(self.slot_btnSetting)

        # 模拟登录需要的一些数据及设置
        self.login_test()

        # # 界面滑出效果，如果y设置为1，界面出现的位置不对，尝试让界面y=330，然后隐藏，再进行滑出试试
        # # 同timerEvent事件中，elif e.timerId() == self.timerLoginShow.timerId():一起取消注释调试
        # self.setFixedHeight(1)
        # self.timerLoginShow = QBasicTimer()
        # self.timerLoginShow.start(1, self)
        # self.login_test()
    def slot_btnSetting(self):
        print(111)

    def login_test(self):
        """此函数内是模拟已经登录过此账号，发生的界面变化"""
        # USER_ID = '165227316'
        # USER_LOGINED_ON = True
        self.comboUserId.setEditText(USER_ID)
        self.lEditPassword.setText('xxxxxxxxxxx')
        self.checkBoxAotuLogin.click()
        self.checkBoxKeepPassword.click()
        # 测试提示信息的显示。self.frameError的位置是（0，330），是看不见的，因为窗口的固定高度就是330，所以这里把窗口的
        # 固定高度加上20（self.frameError的固定高度就是20），自然就显示出来了。self.frameGlobal的固定高度是330，没有变化
        self.timerError = QBasicTimer()
        if USER_LOGINED_ON:
            self.setFixedHeight(self.height() + 20)

    def slot_actionRightPassword(self):
        """在槽内setMenu，然后显示，才可以改变menu菜单的位置。
        如果在外面setMenu就不用self.menuKeyBoard.exec()方法了，直接点击就显示了。
        """
        self.actionRightPassword.setMenu(self.menuKeyBoard)
        pos = QPoint()
        pos.setX(93)
        pos.setY(233)
        self.menuKeyBoard.exec(self.mapToGlobal(pos))

    def slot_comboUserID(self, text):
        """选择下拉项后，重新设置显示为空项，再改变lineEdit的text"""
        self.comboUserId.setCurrentIndex(-1)
        self.comboUserId.lineEdit().setText(text)

    def slot_myQPushButton(self):
        """状态功能在此设置，因这程序只是一个登录界面，所以没写状态功能"""
        sender = self.sender()
        self.myQPushButton.setIcon(sender.icon())

    def slot_btnAddUser_btnLoginSingle(self):
        if self.sender() == self.btnAddUser:
            flag = True
            self.timerError.start(10, self) # 如果有已经登录提示，开始计时器
        else:
            flag = False
            self.setFocus()

        self.frameAdduser.setVisible(flag)
        self.btnLoginSingle.setVisible(flag)

        self.frameLogin.setHidden(flag)
        self.btnSignIn.setHidden(flag)
        self.btnQRcode.setHidden(flag)

    def slot_btnQRcode_btnFrameQRcodeBack(self):
        if self.sender() == self.btnQRcode:
            flag = True
            self.timerError.start(10, self) # 如果有已经登录提示，开始计时器
        else:
            flag = False

        self.frameGlobal.setHidden(flag)
        self.frameQRcode.setVisible(flag)
        self.btnFrameQRcodeUrl.hide()
        self.labFrameQRcodeErrorImg.hide()

    def labUserImg_EnterEvent(self, e):
        self.btnAddUser.show()
        self.flagTimer = 0
        self.timer.stop()
        self.timerBtnAddUserMove.start(3, Qt.PreciseTimer, self)
        return self.labUserImg_orgin_enterEvent(e)

    def labUserImg_LeaveEvent(self, e):
        self.timer.start(10, Qt.PreciseTimer, self)
        return self.labUserImg_orgin_leaveEvent(e)

    def btnAddUser_EnterEvent(self, e):
        self.flagTimer = 0
        self.timer.stop()
        return self.btnAddUser_orgin_enterEvent(e)

    def btnAddUser_LeaveEvent(self, e):
        self.timer.start(10, Qt.PreciseTimer, self)
        return self.btnAddUser_orgin_leaveEvent(e)

    def comboUserID_MousePressEvent(self, e):
        """处理点击下拉箭头后，使封装的lineEdit左侧图标变成蓝色"""
        self.flagComboUserID = True
        self.actionLeftUserID.setIcon(QIcon("image/login/4.png"))
        return self.comboUserID_orgin_mousePressEvent(e)

    def comboUserID_FocusInEvent(self, e):
        """
        获得焦点：改变图标，默认字符设置为空，再改变字符尺寸变大和颜色，就不影响视觉效果了（无内容时光标变小，
        有输入时光标变大）
        """
        self.actionLeftUserID.setIcon(QIcon("image/login/4.png"))
        self.comboUserId.lineEdit().setPlaceholderText('')
        self.comboUserId.setStyleSheet('font-size:17px;color:blank;')
        return self.comboUserID_orgin_focusInEvent(e)

    def comboUserID_FocusOutEvent(self, e):
        """失去焦点：恢复图标，恢复默认字符，再恢复字符尺寸变小和颜色"""
        self.actionLeftUserID.setIcon(QIcon("image/login/3.png"))
        self.comboUserId.lineEdit().setPlaceholderText('账号')
        if self.flagComboUserID: # 如果点击了下拉箭头
            self.actionLeftUserID.setIcon(QIcon("image/login/4.png"))
            self.flagComboUserID = False # 恢复标记，不然会一直判断是True，封装的lineEdit失去焦点时，左侧图标还是蓝色

        text = self.comboUserId.lineEdit().text()
        if text == '': # 这个if,else语段，是处理让默认字符“密码”和有输入以及获得焦点时的字符大小不一样
            self.comboUserId.setStyleSheet('font-size:12px;color:#838383;')
        else:
            self.comboUserId.setStyleSheet('font-size:17px;color:blank;')
        return self.comboUserID_orgin_focusOutEvent(e)

    def lEditPassword_FocusInEvent(self, e):
        """获得焦点：改变图标，默认字符设置为空，再改变字符尺寸变大和颜色，就不影响视觉效果了"""
        self.actionLeftPassword.setIcon(QIcon("image/login/2.png"))
        self.lEditPassword.setPlaceholderText('')
        self.lEditPassword.setStyleSheet('font-size:16px;color:blank;')
        return self.lEditPassword_orgin_focusInEvent(e)

    def lEditPassword_FocusOutEvent(self, e):
        """失去焦点：恢复图标，恢复默认字符，再恢复字符尺寸变小和颜色"""
        self.actionLeftPassword.setIcon(QIcon("image/login/1.png"))
        self.lEditPassword.setPlaceholderText('密码')
        text = self.lEditPassword.text()
        if text == '':
            self.lEditPassword.setStyleSheet('font-size:12px;color:#838383;')
        else:
            self.lEditPassword.setStyleSheet('font-size:16px;color:blank;')
        return self.lEditPassword_orgin_focusOutEvent(e)

    def frameQRcodeUpdata_EnterEvent(self, e):
        """鼠标滑入更新二维码容器："""
        self.timerFrameQRcodeUpdata.start(1, self)
        self.btnFrameQRcodeUrl.show()
        return self.frameQRcodeUpdata_orgin_enterEvent(e)

    def frameQRcodeUpdata_LeaveEvent(self, e):
        """鼠标离开更新二维码容器："""
        self.timerFrameQRcodeUpdata.start(1, self)
        self.btnFrameQRcodeUrl.hide()
        return self.frameQRcodeUpdata_orgin_leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.setFocus() # 主要处理焦点在账号和密码框内时，左键窗口的焦点位置，让输入框失去焦点
            self.flagMove = True
            self.posMove = e.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            e.accept()
        elif e.button() == Qt.RightButton: # 如果焦点在密码框里，右键窗口的焦点位置，账号框会得到焦点并全选
            if self.lEditPassword.hasFocus():
                self.comboUserId.setFocus()
                self.comboUserId.lineEdit().selectAll()

    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self.flagMove:
            self.move(e.globalPos() - self.posMove)  # 更改窗口位置
            e.accept()

    def mouseReleaseEvent(self, e):
        self.flagMove = False

    def timerEvent(self, e):
        if e.timerId() == self.timerBtnAddUserMove.timerId():
            self.btnAddUser.move(self.btnAddUserX, 102)
            self.btnAddUserX += 1
            if self.btnAddUserX >= 273:
                self.timerBtnAddUserMove.stop()
                self.btnAddUserX = 203

        elif e.timerId() == self.timer.timerId():
            if self.flagTimer >= 40:
                self.btnAddUser.hide()
                self.timer.stop()
                self.flagTimer = 0
            self.flagTimer += 1

        elif e.timerId() == self.timerError.timerId():
            if self.height() == 330:
                self.timerError.stop()
            else:
                self.setFixedHeight(self.height() - 1)

        elif e.timerId() == self.timerFrameQRcodeUpdata.timerId():
            if self.flagTimerFrameQRcodeUpdata:
                self.flagTimerFrameQRcodeUpdataX += 1
                self.btnFrameQRcodeUpdata.move(self.flagTimerFrameQRcodeUpdataX, self.btnFrameQRcodeUpdata.y())
                if self.flagTimerFrameQRcodeUpdataX == 115:
                    self.timerFrameQRcodeUpdata.stop()
                    self.flagTimerFrameQRcodeUpdata = False
            elif not self.flagTimerFrameQRcodeUpdata:
                self.flagTimerFrameQRcodeUpdataX -= 1
                self.btnFrameQRcodeUpdata.move(self.flagTimerFrameQRcodeUpdataX, self.btnFrameQRcodeUpdata.y())
                if self.flagTimerFrameQRcodeUpdataX == 20:
                    self.timerFrameQRcodeUpdata.stop()
                    self.flagTimerFrameQRcodeUpdata = True


        # elif e.timerId() == self.timerLoginShow.timerId():
        #     if USER_LOGINED_ON:
        #         height = 20
        #     else:
        #         height = 0
        #     if self.height() == 330 + height:
        #         self.timerLoginShow.stop()
        #     else:
        #         self.setFixedHeight(self.height() + 8)

class MyQPushButton(QPushButton):
    """自己重写的QPushButton，添加了下拉选项(在线，隐身等)"""
    def __init__(self, func, parent=None):
        super(MyQPushButton, self).__init__(parent)
        self.setupUi(func)

    def setupUi(self, func):
        menu = QMenu()
        iconList = ['image/login/8.png', 'image/login/9.png', 'image/login/10.png',
                    'image/login/11.png', 'image/login/12.png', 'image/login/13.png', ]
        iconTextList = ['我在线上', 'Q我吧', '离开', '忙碌', '请勿打扰', '隐身']
        for i in range(6):
            action = QAction(iconTextList[i], menu)
            action.setIcon(QIcon(iconList[i]))
            action.triggered.connect(func)
            menu.addAction(action)
            if i == 2:
                menu.addSeparator()
            elif i == 4:
                menu.addSeparator()
        self.setMenu(menu)

class MyMenu(QMenu, Ui_menuKeyBoard):
    """自定义的QMenu类，通过QAction设置MyMenu打开自己做的软键盘"""

    def __init__(self, parent):
        super(MyMenu, self).__init__()
        self.p = parent
        self.setupUi(self)
        self.flag = 1 # 鼠标是否移入QMenu的标记，为了处理menu中点击空白地方会关闭的bug
        self.setFixedSize(415, 110)
        self.setStyleSheet('background-color: #1B93D9')

        self.flagShift = 0
        self.flagCapsLock = 0
        self.listNumSymbolBtn = []
        self.listLetterBtn = []
        self.strStyleSheet = 'QPushButton {background-color:#cde6c7;} QPushButton:hover {background:#48D1BC} ' \
                        'QPushButton:pressed {background:qlineargradient(spread:pad, x1:0.494, y1:1, x2:0.482955,' \
                        'y2:0.046, stop:0 rgba(0, 191, 162, 255), stop:1 rgba(255, 255, 255, 255));}'
        for btn in self.children()[2:]: # 前两个是布局
            text = btn.text()
            btn.clicked.connect(self.slot_btnsFromMenu)
            btn.setStyleSheet(self.strStyleSheet) # btn按下显示渐变色
            if len(text) == 2:
                self.addLab(text, btn) # 为了处理btn中不能两个字符一个低一个高,往btn里添加了两个lab，btn没有富文本功能
                btn.setText('') # self.addLab中的两个lab已经显示text了，所以要把btn的text清除(还可以让这btn文字全透明)
                self.listNumSymbolBtn.append(btn)

            elif text == '×':
                btn.setStyleSheet('QPushButton {background : transparent;} QPushButton:hover {background:#FF5439;}')
                btn.setToolTip('关闭键盘')

            elif text not in  ['Caps Lock', 'Shift', '←']:
                self.listLetterBtn.append(btn)

    def slot_btnsFromMenu(self):
        sender = self.sender()

        if sender == self.btnCapsLock:
            if self.flagCapsLock == 0:
                for btn in self.listLetterBtn:
                    btn.setText(btn.text().upper())
                self.btnCapsLock.setStyleSheet('background-color : #48D1BC;')
                self.flagCapsLock = 1
            elif self.flagCapsLock == 1:
                for btn in self.listLetterBtn:
                    btn.setText(btn.text().lower())
                self.btnCapsLock.setStyleSheet(self.strStyleSheet)
                self.flagCapsLock = 0

        elif sender == self.btnShift:
            if self.flagShift == 0:
                for btn in self.listLetterBtn:
                    btn.setText(btn.text().upper())
                for btn1 in self.listNumSymbolBtn:
                    textBtn1 = btn1.children()[0].text()[-8] # text()竟然是'<font size=4 color=black>*</font>'，所以取-8
                    textBtn2 = btn1.children()[1].text()[-8]
                    if textBtn2 == ';':
                        textBtn2 = '&lt;'
                    btn1.children()[0].setText(f'<font size=4>{textBtn1}</font>')
                    btn1.children()[1].setText(f'<font size=4 color=black>{textBtn2}</font>')
                self.btnShift.setStyleSheet('background-color : #48D1BC;')
                self.flagShift = 1
            elif self.flagShift == 1:
                for btn in self.listLetterBtn:
                    btn.setText(btn.text().lower())
                for btn1 in self.listNumSymbolBtn:
                    textBtn1 = btn1.children()[0].text()[-8]  # text()竟然是'<font size=4 color=black>*</font>'，所以取-8
                    textBtn2 = btn1.children()[1].text()[-8]
                    if textBtn2 == ';':
                        textBtn2 = '&lt;'
                    btn1.children()[0].setText(f'<font size=4 color=black>{textBtn1}</font>')
                    btn1.children()[1].setText(f'<font size=4>{textBtn2}</font>')
                self.btnShift.setStyleSheet(self.strStyleSheet)
                self.flagShift = 0

        elif sender in self.listNumSymbolBtn:
            text = sender.children()[0].text()[-8]
            text1 = sender.children()[1].text()[-8]
            if text1 == ';':
                text1 = '<' # 这里要插入到密码框，不是要显示，所以不能再用'&lt;'
            if self.flagShift == 0:
                self.p.lEditPassword.insert(text)
            elif self.flagShift == 1:
                self.p.lEditPassword.insert(text1)

        elif sender in self.listLetterBtn:
            self.p.lEditPassword.insert(sender.text())

        elif sender == self.btnBackspace:
            self.p.lEditPassword.backspace() # 删除最后一个字符

        elif sender == self.btnQuit:
            self.close()

    def leaveEvent(self, e):
        """鼠标离开menu"""
        self.flag = 1

    def mousePressEvent(self, e):
        """鼠标按下。为了处理menu中点击空白地方会关闭的bug"""
        if self.flag == 1: # 当标记为1时，说明鼠标离开了menu
            self.close()

    def enterEvent(self, e):
        """鼠标移入menu"""
        self.flag = 0

    def closeEvent(self, e):
        """处理menu关闭后，不让密码框获得焦点"""
        self.p.setFocus()

    def addLab(self, text, parent):
        """专为btn添加两个lab，处理btn中不能两个字符一个低一个高,btn没有富文本功能"""
        lab = QLabel(parent)
        lab.setGeometry(1, 0, 12, 24)
        lab.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        lab1 = QLabel(f'<font size=4>{text[1]}</font>', parent) # 虽然可以用上标<sub>3</sub>,但是字太小了，不能改变大小
        lab1.setGeometry(13, 0, 12, 24)
        lab1.setAlignment(Qt.AlignTop)
        lab.setEnabled(False) # 不设置禁用，按钮点击之后没有回弹效果，并且触发不了点击信号。
        lab.setText(f'<font size=4 color=black>{text[0]}</font>') # 禁用之后字体颜色会变灰，需设置一下颜色
        lab1.setEnabled(False)
        lab.setStyleSheet('background:transparent')
        lab1.setStyleSheet('background:transparent')

        if text == ',<': # 符号"<",会被html识别为标签，所以要用实体符号"&lt;"代替
            lab1.setText('<font size=4>&lt;</font>')

def main():
    app = QApplication(argv)
    app.setStyleSheet(open("QSS.qss", encoding='utf8').read()) # qss文件引入
    window = Login()
    window.show()
    exit(app.exec_())

if __name__ == '__main__':
    main()