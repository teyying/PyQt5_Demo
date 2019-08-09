from sys import argv

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QAction, QMenu, QLabel, QHBoxLayout, QGraphicsScene, \
    QGraphicsView

from PyQt5.QtWidgets import (QGraphicsView,QGraphicsScene,QApplication)
class MainWindow(QGraphicsView):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        #创建场景
        self.scene = QGraphicsScene()
        #在场景中添加文字
        self.scene.addText("Hello, world!")
        #将场景加载到窗口
        self.setScene(self.scene)
if __name__ == '__main__':
    import sys
    #每个PyQt程序必须创建一个application对象，sys.argv 参数是命令行中的一组参数
    #注意：application在 PyQt5.QtWidgets 模块中
    #注意：application在 PyQt4.QtGui 模块中
    app = QApplication(sys.argv)
    #创建桌面窗口
    mainWindow = MainWindow()
    #显示桌面窗口
    mainWindow.show()
    sys.exit(app.exec_())

