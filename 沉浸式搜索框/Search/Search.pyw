from sys import argv
import webbrowser

import keyboard as keyboard
import win32con
import win32api
import win32gui

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QApplication, QDesktopWidget

# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))  # 当前项目路径加入
# 运行时关闭CMD窗口
ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0, ct)
win32gui.ShowWindow(hd, 0)


class Search(QLineEdit):
    def __init__(self):
        super(Search, self).__init__()

        # 隐藏标题栏、窗口永远置顶、不在任务栏上显示
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('search')
        self.setFixedSize(500, 60)

        # 发现pyqt界面如果没有设置任何text，第一次输入时会出现的卡顿问题。所以用下面的方式解决了。
        self.setPlaceholderText("---学无止境---")

        # 这三段代码的原因在函数 on_hotkey 里有详细注释
        self.move(0, -60)
        self.firstRunFlag = True
        self.setReadOnly(True)

        self.setStyleSheet("""
            font:30px;
            font-family: 华文宋体;
            font-weight:300;
            color: white;
            background: rgba(0, 0, 0, 150);
            border-radius:30px;
            border: none;
            padding-left: 30;
            padding-right: 30;
            border: 3px solid rgba(255, 255, 255, 150);;
            """)

        self.setContextMenuPolicy(False)  # 取消右键上下文
        self.setClearButtonEnabled(True)  # 添加清空字符的按钮
        self.returnPressed.connect(self.on_returnPressed)  # 回车事件

        # 注册系统热键，并且拦截其它程序的冲突热键
        keyboard.add_hotkey('Win+F1', self.on_hotkey, suppress=True)

        # self.clipboard = QApplication.clipboard()
        # print(self.clipboard)

    def on_returnPressed(self):
        url = "https://"
        text = self.text().strip()  # 去掉字符串首尾空格
        ts = ('.com', '.net', '.org', '.gov')
        t1 = text[0]
        t3 = text[-3:]  # 为了判断（域名）后3位是否是 '.cn'。  执行内容不多，不需要使用正则了。
        t4 = text[-4:]  # 为了判断（域名）后4位是否在元组ts中
        t5 = text[:5]
        if t1 == ":" or t1 == "：":
            url = f"https://{text[1:]}"  # 直接得到网址字符串
        elif t4 in ts or t3 == '.cn':
            url = f"https://{text}"  # 直接得到网址字符串
        elif t5 == 'https' or t5 == 'HTTPS':
            url = text  # 直接得到网址字符串
        elif text in "qQ我":
            exit()  # 如果输入内容在"qQ我"内就关闭此程序（沉浸式搜索框）
        else:  # 如果不是以上条件，打开百度网站搜索输入内容
            url = f'{url}www.baidu.com/s?wd={self.text()}'  # 百度关键字搜索地址（=号后面输入想搜索的内容）
        # 调用指定浏览器打开网页
        chromePath = r'C:\Users\Administrator.DESKTOP-VMCD0IN\AppData\Local\Google\Chrome\Application\chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
        webbrowser.get('chrome').open(url=url, new=1, autoraise=True)

    def on_hotkey(self):
        """
        注册的系统热键功能函数
        函数内处理了两种Bug：

        一、 如果在另一个编辑器中，如QQ，记事本等，光标处于编辑状态时，调用热键显示
        此界面时，虽然光标也在此界面闪动，但当前的编辑器光标也是在闪动的，此程序
        并不是系统活动的窗口，而是当前的编辑器，输出只会在当前编辑器中。为了解决
        这个问题，下载了pywin32模块，调用了里面的模拟鼠标移动并点击事件，就是为了
        点击此程序，让它成为系统活动窗口。觉得这个模块下载的包太多，不知道pymouse
        模块下载的包多不多。

        二、 为了解决第一次运行时不能提前hide窗体，不然调用热键F1时会报错
        （OSError: exception: access violation reading 0x0000000000000008+-baijiahao），
        所以用了障眼法解决这个问题。
        先移动到界面之外，让肉眼看不见，设置第一次运行的标记self.firstRunFlag=True，
        只读为True，然后第一次用热键F1显示时，其实是移动窗口到指定位置（窗口并没有hide），
        此时设置标记为False，设置只读为False。（因为标记已设置为False，所以只执行一次
        上面的代码）。如果找到其它方法就不需要这么烂的办法了。
        """
        if self.firstRunFlag:
            # 移动到屏幕中心靠上10%的位置
            rect = QDesktopWidget().availableGeometry()
            x, y = rect.width() / 2 - self.width() / 2, rect.height() * 0.1
            self.firstRunFlag = False
            self.setReadOnly(False)
            self.move(x, y)
        else:
            self.setVisible(not self.isVisible())

        if self.isVisible():  # 只有在调用热键F1时才会在窗口是显示状态时，进入此if语句
            pos = self.pos()  # 得到窗体的位置，这其实就是屏幕位置
            win32api.SetCursorPos((pos.x() + 30, pos.y() + 30))  # 移动鼠标到指定位置
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按下鼠标
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 松开鼠标
            self.selectAll()  # 显示界面全选字符串，保留了前一次的输入，暂不想提前清空。

    def focusOutEvent(self, e):
        self.hide()  # 失去焦点时隐藏

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()  # 按Esc键后隐藏
        elif e.modifiers() & Qt.ControlModifier and e.key() == Qt.Key_D:
            self.clear()  # 组合键 Ctrl+D 时清空输入框的字符串

        return super().keyPressEvent(e)  # 继续执行其它键盘事件（不影响其它操作）


if __name__ == '__main__':
    app = QApplication(argv)
    window = Search()
    window.show()
    exit(app.exec_())
