import math
import os
import sys

import time
import keyboard
from json import load, dump
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx
from winsound import PlaySound

from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QRect, QPoint, QDir, QThread, pyqtSignal, QBasicTimer, QRectF
from PyQt5.QtGui import QCursor, QIcon, QBitmap, QPainter, QPen, QBrush, QPixmap, QGuiApplication, QPalette, \
    QMouseEvent, QPainterPath, QColor
from PyQt5.QtWidgets import QApplication, QDialog, QAction, QLineEdit, QWidget, QDesktopWidget, QFileDialog, \
    QPushButton, QMenu, qApp, QSystemTrayIcon, QLabel
from Ui_MainWindow import Ui_MainWindow
from Ui_Config import Ui_Config
from Ui_ScShot import Ui_ScShot

'''
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
db=QSqlDatabase.addDatabase('QODBC')
db.setDatabaseName("Driver={Sql Server};Server=localhost;Database=master;Uid=sa;Pwd=12345678")
#db.setDatabaseName('DSN=QODBC')

'''
# 打包 nuikta xc_freeze pyinstaller
# 主窗口的右键移动需要重写
# 放大鼠标处的图像还未写
# 设置窗口需要修改一个设置设置选项
# 给 self.wid注释
# QRegion

class MainWindow(QDialog, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.flagMove = False
        self.uiConfig = Ui_Config_Logic(self)  # 没有继承，会显示两个窗口，但是是模态的
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(89, 59)

        # self.animation = QPropertyAnimation(self, b'size')
        # self.animation.setDuration(1200)
        # self.animation.setStartValue(QSize(0, 0))
        # self.animation.setKeyValueAt(0.2, QSize(30, 20))
        # self.animation.setKeyValueAt(0.6, QSize(60, 40))
        # self.animation.setKeyValueAt(1, QSize(60, 40))
        # self.animation.setEndValue(QSize(289, 159))
        # self.animation.start()

        # 按钮的信号与槽
        self.btnConfig.clicked.connect(self.uiConfig.exec)
        self.btnMini.clicked.connect(self.slot_MainWindow_btns)
        self.btnScShot.clicked.connect(self.slot_MainWindow_btns)
        self.btnPrtSc.clicked.connect(self.slot_MainWindow_btns)
        self.loadConfig()
        # print(self.btnMini.isChecked())

        # 设置系统托盘
        self.tray = QSystemTrayIcon()  # 创建系统托盘对象
        self.tray.setIcon(QIcon('image/btnOk.png'))  # 设置系统托盘图标
        # self.tray.doubleClicked.connect(self.show)  # 设置托盘点击事件处理函数
        self.menuTray = QMenu(QApplication.desktop())  # 创建菜单
        self.actRestore = QAction(u'还原 ', self, triggered=self.showNormal)  # 添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(u'退出 ', self, triggered=self.close)  # 添加一级菜单动作选项(退出程序)
        self.menuTray.addAction(self.actRestore)  # 为菜单添加动作
        self.menuTray.addAction(self.QuitAction)
        self.tray.setContextMenu(self.menuTray)  # 设置系统托盘菜单

        # 添加系统热键，suppress默认是False,改为True后，就把系统中其它程序的热键阻塞了。
        keyboard.add_hotkey('ctrl+alt+a', self.btnScShot.click, suppress=False)


    def closeEvent(self, QCloseEvent):
        """保险起见，为了完整的退出"""
        self.tray.deleteLater()
        qApp.quit()

    def loadConfig(self):
        try:
            self.configDict = load(open('config.json', 'r', encoding='utf-8'))
            for k, v in self.configDict.items():
                eval(f"{k}({v})")
        except Exception as e:
            print(e)

    def slot_MainWindow_btns(self):
        sender = self.sender()
        if sender == self.btnMini:
            if self.uiConfig.ccBoxMiniToTray.checkState():  # 是否最小化到托盘
                self.hide()
        elif sender == self.btnScShot:
            self.uiScShot = Ui_ScShot_Logic(self.uiConfig)
            self.uiScShot.show()
        elif sender == self.btnPrtSc:
            if self.uiConfig.ccBoxAppHide.checkState():
                self.hide()

            prtSc = QApplication.primaryScreen().grabWindow(0)  # 截取整个屏幕，QPixmap类型
            filePath = self.uiConfig.lineEdFilePath.text()
            if not os.path.exists(filePath):  # 如果此路径没有此文件夹，就创建一个
                os.mkdir(filePath)
            rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            imgPath = f"{filePath}/{rq}.png"
            prtSc.save(imgPath, format='png', quality=100)
            PlaySound('prtSc.wav', flags=1)

            if self.uiConfig.ccBoxAppShow.checkState():
                self.showNormal()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.flagMove = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.RightButton and self.flagMove:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.flagMove = False
        self.setCursor(QCursor(Qt.CustomCursor))  # 更改鼠标图标为系统默认   CrossCursor十字


class Ui_Config_Logic(QDialog, Ui_Config):
    def __init__(self, parent):
        super(Ui_Config_Logic, self).__init__()
        self.setupUi(self)
        self.p = parent
        self.flagMove = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setMouseTracking(True)
        self.setupUiLogic()

    def setupUiLogic(self):

        # 选项卡QListWidget，它在设计师中已经连接QStackedWidget了
        self.listWidget_orgin_mousePressEvent = self.listWidget.mousePressEvent
        self.listWidget.mousePressEvent = self.listWidget_MousePressEvent

        # 存储路径，选项卡第一项（也就是QStackedWidget第一页）
        self.actSetFilePath = QAction(self.lineEdFilePath)
        self.actSetFilePath.setIcon(QIcon("image/openFile.png"))
        self.lineEdFilePath.addAction(self.actSetFilePath, QLineEdit.LeadingPosition)
        self.actSetFilePath.triggered.connect(self.slot_actSetFilePath)
        self.ccBoxSaveDesktop.toggled[bool].connect(self.slot_ccBoxSaveDeskTop)

        # 一些按钮的信号及槽
        self.btnSaveConfig.clicked.connect(self.saveConfig)
        self.btnSaveConfig.clicked.connect(self.close)
        self.btnCancel.clicked.connect(self.close)
        self.btnCancel.clicked.connect(self.p.loadConfig)

    def saveConfig(self):
        """保存设置"""
        try:
            tempDict = dict()
            flag = bool(self.ccBoxSaveDesktop.checkState())
            flag1 = bool(self.ccBoxAppHide.checkState())
            flag2 = bool(self.ccBoxAppShow.checkState())
            flag3 = bool(self.ccBoxAutoExec.checkState())
            flag4 = bool(self.ccBoxWindowOnTop.checkState())
            flag5 = bool(self.ccBoxMiniToTray.checkState())
            tempDict['self.uiConfig.ccBoxSaveDesktop.setChecked'] = str(flag)
            tempDict['self.uiConfig.ccBoxAppHide.setChecked'] = str(flag1)
            tempDict['self.uiConfig.ccBoxAppShow.setChecked'] = str(flag2)
            tempDict['self.uiConfig.ccBoxAutoExec.setChecked'] = str(flag3)
            tempDict['self.uiConfig.ccBoxWindowOnTop.setChecked'] = str(flag4)
            tempDict['self.uiConfig.ccBoxMiniToTray.setChecked'] = str(flag5)
            tempDict['self.uiConfig.lineEdShortcutSlice.setText'] = f"\'{self.lineEdShortcutSlice.text()}\'"
            tempDict['self.uiConfig.lineEdShortcutFull.setText'] = f"\'{self.lineEdShortcutFull.text()}\'"
            tempDict['self.uiConfig.lineEdShortcutSave.setText'] = f"\'{self.lineEdShortcutSave.text()}\'"

            tempDict['self.uiConfig.lineEdFilePath.setText'] = f"\'{self.lineEdFilePath.text()}\'"
            tempDict['self.uiConfig.lineEdFilePath.setReadOnly'] = str(flag)
            tempDict['self.uiConfig.actSetFilePath.setEnabled'] = f"not {flag}"
            dump(tempDict, open('config.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

    def slot_ccBoxSaveDeskTop(self, state):
        """QCheckBox:ccBoxSaveDeskTop（保存到桌面文件夹）的槽函数"""
        key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        deskPath = QueryValueEx(key, "Desktop")[0].replace('\\', '/') + '/SC屏幕截图'
        self.actSetFilePath.setEnabled(not state)
        self.lineEdFilePath.setReadOnly(state)
        self.lineEdFilePath.setText(deskPath)

    def slot_actSetFilePath(self):
        diaLogFile = QFileDialog(self)
        initialPath = QDir.currentPath()  # 当前文件夹路径，应该写ini配置文件让它读取记录,自己用json文件代替了
        newPath = diaLogFile.getExistingDirectory(self, "选取文件夹", initialPath)
        self.lineEdFilePath.setText(newPath)
        self.setFocus()

    def listWidget_MousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            return self.listWidget_orgin_mousePressEvent(e)  # 这样做就使它右键失效了，但是右键窗口移动还没实现

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.flagMove = True
            self.m_Position = e.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            e.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标
        elif e.button() == Qt.LeftButton:
            self.setFocus()

    def mouseMoveEvent(self, e):
        if Qt.RightButton and self.flagMove:
            self.move(e.globalPos() - self.m_Position)  # 更改窗口位置
            e.accept()

    def mouseReleaseEvent(self, e):
        self.flagMove = False
        self.setCursor(QCursor(Qt.CustomCursor))  # 更改鼠标图标为系统默认


class Ui_ScShot_Logic(QWidget, Ui_ScShot):
    """
    截屏逻辑：
    1、一打开截屏，就先创建屏幕截图pixScreenshot，并设置为主窗口的背景，并设置窗口无标题栏。再创建一个QWidget（wTop），
    用来作为全屏的阴影遮盖，设置背景样式rgba的透明，它的大小以及主窗口的大小都是全屏大小（和全屏截图一样大）。功能
    按钮容器wFunc，以及其它功能不作介绍，代码里有注释。
    2、设置鼠标按下、移动，释放，来画出一个矩形框。在移动的时候设置标记(flagDrawing)为True,并self.update刷新界面，在刷新
    界面时就能设置画笔和画刷来画出所要截图的范围
    3、这第三步，其实有一部分在第一处就要设置。这对我来说是个难点，研究了两天，才瞎猫碰到死耗子搞成了。原本在网上复制的
    截屏代码，竟然矩形选框内被穿透了，直接可以操作内部（此程序下面此范围内），很是让人无语。才研究两天，总算总算解决了。
    此程序就是用pyqt5的setMask遮罩效果来完成对我来说主要的功能的。
    在初始化处先创建一个QBitmap（blackMask)，并填充成黑色，然后设置QWidget(wTop)的遮罩为blackMask。这里简单说一下，如果
    在遮罩的地方用白色画刷涂的地方会失去遮罩（也就是wTop的背景），显示出下层窗口（窗口已经设置为全屏截图）的图片。
    用黑色画刷涂的话，就是显示出wTop的背景。这里就样photoShop中的那个蒙版效果，原理是一样的。重要处在paintEvent事件中，
    已经有注释。
    """

    def __init__(self, parent):
        super(Ui_ScShot_Logic, self).__init__()
        self.setupUi(self) # 加载设计师画的界面
        self.p = parent

        # 主窗口设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 隐藏标题栏
        self.pixPrtSc = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())  # 截取整个屏幕（QPixmap类型）
        self.resize(self.pixPrtSc.size())  # 设置主窗口大小
        p = QPalette()
        p.setBrush(self.backgroundRole(), QBrush(self.pixPrtSc))
        self.setPalette(p)  # 设置主窗口背景
        self.flagDrawing = False  # 主窗口的鼠标拖动标记，已经为子

        self.wid = QLabel(self)
        self.wid.lower()
        # self.wid.raise_() # 最上层
        self.wid.resize(self.size())
        self.wid.move(0, 0)
        self.wid.setStyleSheet('border:3px solid #00FFFF;')
        # self.wid.hide()


        # 阴影容器设置
        self.wTop.resize(self.size())  # 设置wTop也为屏幕大小
        self.blackMask = QBitmap(self.size())  # 创建位图，全屏大小
        self.blackMask.fill(Qt.black)  # 填充位图为全黑。显示效果为原本wTop的背影，如果全白，相当于把wTop擦掉了。
        self.wTop.setMask(self.blackMask)  # 设置self.wTop的遮罩为self.blackMask
        self.wTop.enterEvent = self.wTop_EnterEvent  # 设置wTop的鼠标进入事件。事件内有详细注释。
        self.flagWTopEnter = False  # wTop的鼠标进入事件的标记

        # 其它需要初始化的
        self.btnOk.clicked.connect(self.slot_ScShot_btns)
        self.btnSaveAs.clicked.connect(self.slot_ScShot_btns)
        self.wFunc.hide()  # 先隐藏功能按钮容器
        self.wInfo.hide() # 本来可以不用隐藏，再让后面显示，但是那样它会闪一下。因为原来的位置是在Qt设计师中乱放的。
        self.strDpi = "0 x 0"
        self.flag = False

        # lab = QLabel('aaa', self.wTop)
        # lab.resize(300, 300)
        # lab.setStyleSheet('background:red;')

    def wTop_EnterEvent(self, e):
        """
        鼠标进入wTop子QWidget内，为了处理一打开截屏界面wInfo初始跟随鼠标状态，只需要一次，因为有self的鼠标
        mouseMoveEvent处理后续动作。之所以要做一个标记flagWTopEnter为False才有动作，是因为在截图时，画的矩形
        选区内是self的焦点，之外才是wTop的焦点。鼠标在矩形内外来回移动会多次处理此事件动作，关键是此动作和
        self的鼠标移动件事有冲突，都在处理wInfo的鼠标跟随。目前只想到这种方法解决。
        """
        if not self.flagWTopEnter:  # 只有self.flagWTopEnter=False时，not self.flagWTopEnter 才为真
            self.flagWTopEnter = True
            self.imgPrtSc = self.pixPrtSc.toImage()
            self.method_wInfo(e.globalPos().x(), e.globalPos().y())
            self.wInfo.show()
            # rect = QRect(e.globalPos().x() - 13, e.globalPos().y() - 10, 114, 85)  # 截取的范围
            # copyZoomIn = self.pixPrtSc.copy(rect)
            # self.labInfoZoomIn.setPixmap(copyZoomIn)

    def method_wInfo(self, pointX, pointY):
        """QWidget(wInfo)的移动，以及wInfo内的QLebal(labInfoZoomIn)的图片设置"""
        self.wInfo.move(pointX + 5, pointY + 20)
        color = self.imgPrtSc.pixelColor(pointX, pointY)
        self.strRgb = str(color.getRgb()[:-1])
        self.textEdInfoRgb.setText(f"DPI:({self.strDpi})<br/>RGB:{self.strRgb}")  # 13 10
        # 参数32，24，是矩形的宽高，是要QLabel(labInfoZoomIn)设置的图片，因为在设计师中已经设置setScaledContents为True,
        # 所以它放比它小的图片会放大。而pointX-14和pointY-10，是矩形的左上角位置，需要减多少，是看原图大小的宽高除以2,
        # 再减去十字线（宽4px）的一半（32/2-2=14,24/2-2=10。labInfoZoomIn的尺寸是116x84
        # 这样，labInfoZoomIn在显示图片的时候，十字交差处才会是鼠标指针点的位置。
        rect = QRect(pointX-14, pointY-10, 32, 24)  # 截取的范围
        copyZoomIn = self.pixPrtSc.copy(rect)
        self.labInfoZoomIn.setPixmap(copyZoomIn)

    def slot_ScShot_btns(self):
        sender = self.sender()
        filePath = self.p.lineEdFilePath.text()
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.copyPixPrtSc = self.pixPrtSc.copy(self.rect)  # 截取矩形区内的图片
        PlaySound('prtSc.wav', flags=1)
        if sender == self.btnOk:
            if not os.path.exists(filePath):  # 如果此路径没有此文件夹，就创建一个
                os.mkdir(filePath)
            imgPath = f"{filePath}/{rq}.png"
            self.copyPixPrtSc.save(imgPath, format='png', quality=100)
        elif sender == self.btnSaveAs:
            currentPath = filePath + f"/{rq}.png"
            fileName, _ = QFileDialog.getSaveFileName(self, "另存为", currentPath, f"PNG File(*.png);;All Files(*)")
            if fileName:
                self.copyPixPrtSc.save(fileName, format='png', quality=100)
                self.close()

    def paintEvent(self, event):
        if self.flag:
            pointX = self.endPoint.x()
            pointY = self.endPoint.y()
            self.method_wInfo(pointX, pointY)  # 调用移动方法

        if self.flagDrawing:
            self.mask = self.blackMask.copy()  # 必须要拷贝，其实我也不是很理解这句为何。
            pp = QPainter(self.mask)  # 参数一定要是拷贝的QPixmap(self.mask)
            pen = QPen()  # 创建画笔    Qt.green, 13, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)  # 创建画刷
            pp.setBrush(brush)
            rect = QRect(self.startPoint, self.endPoint)
            pp.drawRect(rect)  # 画矩形
            self.wTop.setMask(QBitmap(self.mask))  # 是wTop设置遮罩，不是主窗口。不然会穿透的。

            self.strDpi = f"{abs(rect.width())} x {abs(rect.height())}"
            # self.wid.setStyleSheet('border:2px dashed #00FFFF;') # 改变边宽和样式（虚线）
            # self.wid.setGeometry(rect.adjusted(-2, -2, 2, 2)) # 上下左右都往外偏移2px，因为上面设置border为2px
            # self.wid.setGeometry( rect.x()-2, rect.y()-2,abs(rect.width())+2,abs(rect.height())+2) # 上下左右都往外偏移2px，因为上面设置border为2px
            try:
                sX, sY, eX, eY = self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y()
                p2 = QPainter(self)
                pen2 = QPen(QColor('#00FFFF'), 1)
                p2.setPen(pen2)
                p2.drawRect(rect)
                # 下面这四句忘了本来要做什么的了
                # p2.fillRect(rect, QColor('background:rgba(0,0,0,100);'))
                # rect.adjust(50, 50, -50, -50)
                # p2.drawRect(rect)
                # p2.fillRect(rect, Qt.red)


                listPointRect = [(sX, sY), (sX + (eX - sX) / 2, sY), (eX, sY), (eX, sY + (eY - sY) / 2),
                                 (eX, eY), (sX + (eX - sX) / 2, eY), (sX, eY), (sX, sY + (eY - sY) / 2)]
                for x, y in listPointRect:
                    p2.drawRect(x - 3, y - 3, 6, 6)
                    p2.fillRect(x - 3, y - 3, 6, 6, QBrush(QColor('#00FFFF')))


                # p2.begin(self)
                # path = QPainterPath()
                # path.addRect(QRectF(self.startPoint, self.endPoint))

                # self.wid.setGeometry(QRect(*path.controlPointRect().getRect()).adjusted(-20, -20, 20, 20))
                # p2.drawRect(QRectF(*(sX, sY), *(sX + (eX - sX) / 2, sY)))



                # listPointRect = [(sX, sY), (sX+(eX-sX)/2, sY), (eX, sY), (eX, sY+(eY-sY)/2),
                #                  (eX, eY), (sX+(eX-sX)/2, eY), (sX, eY), (sX, sY+(eY-sY)/2)]
                # path2 = QPainterPath()
                # for x, y in listPointRect:
                #     path2.addRect(x-3, y-3, 6, 6)
                # p2.fillPath(path2, QBrush(QColor('#00FFFF')))
                # path.connectPath(path2) # 连接两个闭合路径
                # path.translate(50, 50) # 偏移到某点
                # p2.drawPath(path)
                # self.wid.setStyleSheet('border:none;')
                # p2.end()

            except Exception as e:
                print(e)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # self.wid.hide()
            self.wTop.setStyleSheet('background:rgba(0,0,0,100);') # 设置背景透明度，阴影效果。鼠标按下时再出现
            self.wInfo.show()
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.wFunc.hide()  # 鼠标按下时隐藏功能按钮容器
            self.flagDrawing = True
        elif event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, event):
        """
        必须为子控件设置鼠标跟踪setMouseTracking(True)，不然鼠标在控件上时，就不再追踪了。
        已经在Qt设计师中设置好了
        """
        self.flag = True
        self.endPoint = event.pos()
        self.update()

        # self.pointX = event.globalPos().x()  # event.pos()也行
        # self.pointY = event.globalPos().y()
        # self.flag = True
        # # self.method_wInfo_move(pointX, pointY)  # 调用移动方法
        # if self.flagDrawing:
        #     self.endPoint = event.pos()
        # self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            self.rect = QRect(self.startPoint, self.endPoint)  # 截取的范围
            shotX, shotY, shotWidth, shotHeight = self.rect.getRect()
            wFuncWidth, wFuncHeight = self.wFunc.width(), self.wFunc.height()
            # 以下if语句是判断鼠标释放后，最后一点到窗口边缘时，功能按钮容器超界问题
            if shotWidth < 0:
                moveX = shotX + shotWidth - (wFuncWidth + shotWidth)  # 这里width是负数，这里用+号相当于减去
            else:
                moveX = shotX + shotWidth - wFuncWidth
            if shotHeight < 0:
                moveY = shotY
            else:
                moveY = shotY + shotHeight
            if moveX < 0:
                moveX = 0
            if self.pixPrtSc.height() - moveY < wFuncHeight:
                moveY = moveY - shotHeight - wFuncHeight
            self.wFunc.move(moveX, moveY)
            self.wFunc.show() # 鼠标释放时显示功能按钮容器
            self.wInfo.hide() # 鼠标释放时隐藏信息显示容器
            self.flagDrawing = False
            self.flag = False #

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(open("style.qss", encoding='utf8').read())  # qss文件引入
    win = MainWindow()
    win.show()  # C5D1DC F0F3F6 CA7037
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
