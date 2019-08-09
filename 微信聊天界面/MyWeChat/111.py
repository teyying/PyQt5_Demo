import sys
from time import sleep, time

# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QFile, QSize, QBasicTimer, QModelIndex
from PyQt5.QtGui import QTextFrameFormat, QFont, QTextBlockFormat, QIcon, QColor, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import *
from os import listdir


class MainWindow(QMainWindow):
    def __init__(self,):
        super(QMainWindow,self).__init__()
        file = QFile('test.qss')
        file.open(QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = str(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        self.resize(340, 600)

        dock = QDockWidget(self)
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)


        self.edit = QLineEdit()
        self.edit.textChanged[str].connect(self.temp)
        self.list = QListWidget()
        self.btn = QPushButton()
        self.btn.setFixedHeight(50)
        self.btn.clicked.connect(self.fn)
        layout.addWidget(self.edit)

        layout.addWidget(self.list)
        layout.addWidget(self.btn)

        widget.setLayout(layout)
        dock.setWidget(widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        names = listdir('微信好友头像/〃那刻温存丶/')  # 路径
        dock.setWindowTitle(f'共 {len(names)} 位好友')  # self.listWidget.count()也能统计列表项数
        self.list.setIconSize(QSize(40, 40))

        self.nameList = []
        for name in names:
            # item = QListWidgetItem(QIcon(f"微信好友头像/〃那刻温存丶/{name}"), f'{name[:-4]}') # 温存.jpg
            item = QListWidgetItem(self.list) # 温存.jpg
            item.setIcon(QIcon(f"微信好友头像/〃那刻温存丶/{name}"))
            item.setText(name[:-4])
            self.nameList.append(name[:-4])
            # item.setTextAlignment(0)
            # self.aa = QWidget()
            # self.aa.setObjectName('widget2')
            # hbox = QVBoxLayout()
            # hbox.setContentsMargins(0,0,0,0)
            # b = QLabel(name[:-4], self.aa)
            # b.setObjectName('labUp')
            # c = QLabel(name[:-4], self.aa)
            # c.setObjectName('labDown')
            # hbox.addWidget(b)
            # hbox.addWidget(c)
            # self.aa.setLayout(hbox)
            self.list.addItem(item)
            self.list.setItemWidget(item, self.fn2(name[:-4]))




        # self.c = self.list.findItems('中国电信小牛', Qt.MatchContains)[0]
        # self.list.takeItem(0)
        # self.list.setCurrentIndex(QModelIndex())
        # self.list.currentItemChanged.connect(self.fn)
    def fn2(self, name):
        aa = QWidget()
        aa.setObjectName('widget2')
        aa.setFixedHeight(40)
        hbox = QVBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        b = QLabel(name, aa)
        b.setObjectName('labUp')
        c = QLabel(name, aa)
        c.setObjectName('labDown')
        hbox.addWidget(b)
        hbox.addWidget(c)
        aa.setLayout(hbox)
        return aa
    def temp(self, text):
        # text = self.edit.text()
        try:
            all_items = self.list.findItems(text, Qt.MatchContains)
            a = self.list.findItems('', Qt.MatchContains)
            # all_items = self.list.findItems(text, Qt.MatchExactly)
            # all_items = self.list.findItems('', Qt.MatchRegExp)
            for i in a:
                if i in all_items:
                    i.setHidden(False)
                else:i.setHidden(True)
        except Exception as e:
            print(e)
    def fn(self):
        try:
            from random import choice
            name = choice(self.nameList)
            self.b = self.list.findItems(name, Qt.MatchContains)[0]
            self.list.takeItem(self.list.row(self.b))
            self.list.insertItem(0, self.b)
            self.list.setItemWidget(self.b, self.fn2(name))
        # print(self.list.selectedItems())
        except Exception as e:
            print(e)


    def is_Chinese(self, word):
        ddd = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”…﹏"

        for ch in word:
            if '\u4e00' <= ch <= '\u9fff' or ch in ddd:
                return True
        return False




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

"""
widget2 = QWidget()
widget2.setObjectName('widget2')
vbox = QVBoxLayout()
vbox.setSpacing(15)
vbox.setContentsMargins(0,5,0,0)
labUp = QLabel(name[:-4])
labUp.setObjectName('labUp')
labUp.setFixedHeight(20)
labDown = QLabel(name[:-4])
labDown.setObjectName('labDown')
labDown.setFixedHeight(15)
vbox.addWidget(labUp)
vbox.addWidget(labDown)
hbox = QHBoxLayout()
icon = QLabel()
icon.setFixedSize(50, 50)
icon.setScaledContents(True)
icon.setPixmap(QPixmap(f"微信好友头像/〃那刻温存丶/{name}"))
hbox.addWidget(icon, 0)
hbox.addLayout(vbox, 1)
widget2.setLayout(hbox)

item = QListWidgetItem(self.list) # 温存.jpg
item.setText(name[:-4])
item.setSizeHint(widget2.sizeHint())
self.list.addItem(item)
self.list.setItemWidget(item, widget2)
item.setBackground(QColor(QColor(255,0,0, 90)))
item.setBackground(Qt.transparent)
"""

"""
import sys
from time import sleep, time

# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QFile, QSize, QBasicTimer, QModelIndex
from PyQt5.QtGui import QTextFrameFormat, QFont, QTextBlockFormat, QIcon, QColor, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import *
from os import listdir


class MainWindow(QMainWindow):
    def __init__(self,):
        super(QMainWindow,self).__init__()
        file = QFile('itchatQSS.qss')
        file.open(QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = str(styleSheet, encoding='utf8')
        self.setStyleSheet(styleSheet)
        self.resize(340, 600)

        dock = QDockWidget(self)
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)


        self.edit = QLineEdit()
        self.edit.textChanged[str].connect(self.temp)
        self.list = QListWidget()
        self.btn = QPushButton()
        self.btn.setFixedHeight(50)
        self.btn.clicked.connect(self.fn)
        layout.addWidget(self.edit)

        layout.addWidget(self.list)
        layout.addWidget(self.btn)

        widget.setLayout(layout)
        dock.setWidget(widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        names = listdir('微信好友头像/〃那刻温存丶/')  # 路径
        dock.setWindowTitle(f'共 {len(names)} 位好友')  # self.listWidget.count()也能统计列表项数
        self.list.setIconSize(QSize(40, 40))

        for name in names:
            item = QListWidgetItem(QIcon(f"微信好友头像/〃那刻温存丶/{name}"), f'{name[:-4]}') # 温存.jpg
            self.list.addItem(item)


        # self.b = self.list.findItems('二哥', Qt.MatchContains)[0]
        # self.c = self.list.findItems('中国电信小牛', Qt.MatchContains)[0]
        # self.list.takeItem(0)
        # self.list.setCurrentIndex(QModelIndex())
        # self.list.currentItemChanged.connect(self.fn)

    def temp(self, text):
        # text = self.edit.text()
        try:
            all_items = self.list.findItems(text, Qt.MatchContains)
            a = self.list.findItems('', Qt.MatchContains)
            # all_items = self.list.findItems(text, Qt.MatchExactly)
            # all_items = self.list.findItems('', Qt.MatchRegExp)
            for i in a:
                if i in all_items:
                    i.setHidden(False)
                else:i.setHidden(True)
        except Exception as e:
            print(e)
    def fn(self):
        try:
            self.list.takeItem(self.list.row(self.b))
            self.list.insertItem(0, self.b)
        # print(self.list.selectedItems())
        except Exception as e:
            print(e)


    def is_Chinese(self, word):
        ddd = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”…﹏"

        for ch in word:
            if '\u4e00' <= ch <= '\u9fff' or ch in ddd:
                return True
        return False




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

"""