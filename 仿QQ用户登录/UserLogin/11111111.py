from sys import argv

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGraphicsView, QGraphicsScene


class A(QWidget):
    def __init__(self):
        super(A, self).__init__()
        btn = QPushButton('AAAA', self)
        btn.resize(200, 200)

class B(QWidget):
    def __init__(self):
        super(B, self).__init__()
        btn = QPushButton('BBBb', self)
        btn.resize(200, 200)

class C(QGraphicsScene):
    def __init__(self):
        super(C, self).__init__()
        # 创建场景
        # self.scene = QGraphicsScene()
        # 在场景中添加文字
        # self.scene.addText("Hello, world!")
        a = A()
        b = B()
        self.addWidget(a)
        self.addWidget(b)
        # 将场景加载到窗口
        # self.setScene(self.scene)


if __name__ == '__main__':
    app = QApplication(argv)
    mainWindow = C()
    mainWindow.show()
    exit(app.exec_())