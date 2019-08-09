from json import load, dump
from os.path import isfile
from sys import argv
from time import localtime, time

from PyQt5.QtCore import pyqtSlot, Qt, QRectF, QPoint, QThread
from PyQt5.QtGui import QIcon, QBitmap, QPainter, QBrush, QCloseEvent
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QSystemTrayIcon, qApp, QMenu, QAction, QStyle
from Ui_Main import Ui_Main
from Ui_TodayDish_Logic import Ui_TodayDish_Logic
from Ui_NewGuests_Logic import Ui_NewGuests_Logic, MyBtn

class Ui_Main_Logic(QWidget, Ui_Main):
    def __init__(self, parent=None):
        super(Ui_Main_Logic, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground)  # 这一句可以解决QWidget不显示图片的问题。不用重写paintEvent了。
        self.setWindowIcon(QIcon('icon.png'))
        self.message = Message()
        self.loadDateAndBill()
        self.uiTodayDish = Ui_TodayDish_Logic(self)

        # 一些控件的信号与槽设置
        self.btnTodayDish.clicked.connect(self.uiTodayDish.raise_)  # 每次点击使界面显示在前面，但有一问题:
        self.btnTodayDish.clicked.connect(self.uiTodayDish.show)    # 只有第一次它获得焦点，setFoucs也不管用
        [j.clicked.connect(self.slot_whetherPay(i)) for i, j in enumerate([self.btnUnpaid, self.btnPaid])]# 目前总共就2页
        self.btnUnpaid.clicked.emit()  # 为了样式设置，先放着吧，不好看再删除

        self.listDeskNames = []


    def loadDateAndBill(self):
        """加载今日日期和账单。菜单（在Ui_TodayDish_Logic加载的）"""
        # 得到今日日期，因为是饭店是夜市，所以自定义凌晨8点之前都为昨日的日期。
        date = localtime(time())
        year, mon, day, hour = date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour
        if hour < 8:
            day -= 1
        self.dateToday = f"{year}-{mon}-{day}"

        if not isfile(f'dataOrder/{self.dateToday}账单.json'):  # 如果今日还未创建账单，就提前创建一个空账单
            d = {'已结账': dict(), "未结账": dict()}
            dump(d, open(f"dataOrder/{self.dateToday}账单.json", 'w', encoding='utf-8'), indent=4,
                 ensure_ascii=False)
        self.dictTodayBill = load(open(f'dataOrder/{self.dateToday}账单.json', 'r', encoding='utf-8'))

        self.timer = self.startTimer(1000, Qt.VeryCoarseTimer)

    def timerEvent(self, e):
        for k, v in self.dictTodayBill.items():
            for k2, v2 in v.items():
                if k == '未结账':
                    whetherPay = self.widUnpaid
                else:
                    whetherPay = self.widPaid
                MyBtn(Ui_NewGuests_Logic(self, deskName=k2, deskDish=v2), self, whetherPay)
        # 今日还没开张时显示
        if not self.dictTodayBill['已结账'] and not self.dictTodayBill['未结账']:
            self.message.setMsg('新的一天\n财源滚滚', self)
        self.killTimer(self.timer)

    def slot_whetherPay(self, index):
        """未结账和已结账按钮的功能设置和改变样式"""
        def fn():
            sender = self.sender()
            self.stkWid.setCurrentIndex(index)
            sender.setStyleSheet('border:1px solid white;background: rgba(255, 255, 255, 100);')
            if sender == self.btnUnpaid:
                self.btnPaid.setStyleSheet('border:none;background: rgba(0, 0, 0, 50);')
            elif sender == self.btnPaid:
                self.btnUnpaid.setStyleSheet('border:none;background: rgba(0, 0, 0, 50)')

        return fn

    @pyqtSlot()
    def on_btnOrder_clicked(self):
        # self.uiNewGuests = Ui_NewGuests_Logic(self)
        # self.uiNewGuests.show()
        Ui_NewGuests_Logic(self).show()


class Message(QLabel):
    def __init__(self,):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('background:rgba(255,255,255,100);font-size:40px;border-radius:20px;')


    def setMsg(self,  msg, parent, sec=2):
        self.sec = sec
        self.setParent(parent)
        self.move(parent.mapToGlobal(QPoint(parent.width()/2-self.width()/2, parent.height()/2-self.height()/2)))
        self.setText(msg)
        self.show()
        self.timerId = self.startTimer(sec*1000, Qt.VeryCoarseTimer)

    def mousePressEvent(self, e):
        self.close()

    def timerEvent(self, e):
        self.killTimer(self.timerId)
        self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    window = Ui_Main_Logic()
    window.show()
    exit(app.exec_())