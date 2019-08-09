from json import load, dump

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QStyledItemDelegate, QStyleOptionViewItem, QStyle, \
    QTextEdit, QComboBox, QPushButton, QGridLayout, QDialog, QLabel, QVBoxLayout, QHBoxLayout
from Ui_NewGuests import Ui_NewGuests
from Ui_Dialog import Ui_Dialog


class Ui_NewGuests_Logic(QWidget, Ui_NewGuests):
    def __init__(self, parent, deskName=None, deskDish=None):
        super(Ui_NewGuests_Logic, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground)  # 这一句可以解决QWidget不显示图片的问题。不用重写paintEvent了。
        self.setWindowIcon(QIcon('icon.png'))
        self.p = parent
        self.message = parent.message
        self.dateToday = parent.dateToday
        self.dictTodayBill = parent.dictTodayBill
        self.gridUnpaid = parent.gridUnpaid
        self.gridPaid = parent.gridPaid

        self.listDeskNames = parent.listDeskNames

        self.loadTodayDish()

        self.btnPay.hide()

        self.tableWids = [self.tableWidColdDish3, self.tableWidHotDishes3, self.tableWidDrinks3, self.tableWidOther3]
        # 设置表格列宽自适应填满界面。设计师中已经设置了StretchLastSection,单个表格适应字符长度。
        [i.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) for i in self.tableWids]
        self.tableWidOrderDish.setColumnWidth(0, 50)
        self.tableWidOrderDish.setColumnWidth(1, 200)
        self.tableWidOrderDish.setColumnWidth(2, 50)
        self.tableWidOrderDish.setColumnWidth(3, 50)

        # 部分信号与槽函数的设置
        self.tableWid = None
        self.rowIndex = None
        [i.cellClicked.connect(self.tableWids_cellClicked) for i in self.tableWids]
        [i.cellDoubleClicked.connect(self.btnAdd.clicked.emit) for i in self.tableWids]
        [i.clicked.connect(self.slot_addOrDel) for i in [self.btnAdd, self.btnDel]]

        self.btnWait.clicked.connect(lambda: self.slot_waitOrPay('未结账'))
        self.btnPay.clicked.connect(lambda: self.slot_waitOrPay('已结账'))

        self.btnTodayDishShow.clicked.connect(parent.btnTodayDish.clicked.emit)
        self.tabWidget.tabBarClicked.connect(self.slot_tabWidget_tabBarClicked)

        self.btnWait.setProperty('from', 'new')  # 创建新客时，设置等待客人用餐按钮属性from为new.点击时就可以创建桌号按钮

        self.flagBtn = None
        self.flagClose = False

        if deskName:
            self.labDeskName.setText(deskName)
            self.loadTodayBill(deskDish)
        else:
            self.setDeskName("未知")


    def loadTodayBill(self, deskDish):
        a = {'已结账': {}, '未结账': {'未知': {'备注': '', '花生': ['凉菜', '12', '1']}, '未知(2)': {'备注': ''}, '未知(3)': {'备注': ''},
                            '未知(4)': {'备注': '', '云丝': ['凉菜', '12', '1']},
                            '未知(5)': {'备注': '', '云丝': ['凉菜', '12', '1'], '面筋': ['凉菜', '12', '1']},
                            '未知(6)': {'备注': '', '面筋': ['凉菜', '12', '1'], '花生': ['凉菜', '12', '1']},
                            '未知(7)': {'备注': '', '白酒': ['酒水', '111', '1'], '红酒': ['酒水', '222', '1']},
                            '未知(8)': {'备注': ''}, '未知(9)': {'备注': ''}, '未知(10)': {'备注': ''}, '未知(11)': {'备注': ''},
                            '未知(12)': {'备注': ''}, '未知(13)': {'备注': ''}, '未知(14)': {'备注': ''},
                            '未知(15)': {'备注': '', '面筋': ['凉菜', '12', '1']}, '未知(16)': {'备注': ''},
                            '未知(17)': {'备注': '', '面筋': ['凉菜', '12', '1']},
                            '未知(18)': {'备注': '', '鸡蛋': ['凉菜', '12', '1']}, '未知(19)': {'备注': ''}, '未知(20)': {'备注': ''},
                            '未知(21)': {'备注': '', '面筋': ['凉菜', '12', '1']},
                            '未知(22)': {'备注': '', '鸡蛋': ['凉菜', '12', '1']},
                            '未知(23)': {'备注': '', '面筋': ['凉菜', '12', '1']}}}
        for k, v in deskDish.items():
            if k != '备注':
                self.tableWidOrderDish.insertRow(self.tableWidOrderDish.rowCount())  # 先插入行，下面再添加数据
                self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 0, QTableWidgetItem(v[0]))
                self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 1, QTableWidgetItem(k))
                self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 2, QTableWidgetItem(v[1]))
                self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 3, QTableWidgetItem(v[2]))

    def loadTodayDish(self):
        try:
            dataTodayDish = load(open(f'dataDish/{self.dateToday}菜谱.json', 'r', encoding='utf-8'))
            for _k, _v in dataTodayDish.items():
                for k, v in _v.items():
                    if _k == '凉菜':
                        tableWid = self.tableWidColdDish3
                    elif _k == '热菜':
                        tableWid = self.tableWidHotDishes3
                    elif _k == '酒水':
                        tableWid = self.tableWidDrinks3
                    elif _k == '其它':
                        tableWid = self.tableWidOther3
                    tableWid.insertRow(tableWid.rowCount())
                    tableWid.setItem(tableWid.rowCount() - 1, 0, QTableWidgetItem(k))
                    tableWid.setItem(tableWid.rowCount() - 1, 1, QTableWidgetItem(v))

        except Exception as e:
            if type(e) is FileNotFoundError:
                self.message.setMsg('今日还未\n设置菜谱', self)
            else:
                pass

    def slot_tabWidget_tabBarClicked(self):
        """换页时清除已选，不然换页没选择时，会添加之前页面所选项"""
        [i.clearSelection() for i in self.tableWids if i != self.sender()]
        self.tableWid = None
        self.rowIndex = None

    def tableWids_cellClicked(self):
        self.tableWid = self.sender()
        self.rowIndex = self.sender().currentRow()

    def slot_addOrDel(self):
        if self.tableWid == None or self.rowIndex == None:
            return
        textKind = self.tabWidget.tabText(self.tabWidget.currentIndex())  # 得到种类字符串，比如'热菜'或者'凉菜'。
        sender = self.sender()
        if sender == self.btnAdd:
            text1 = self.tableWid.item(self.rowIndex, 0)
            text2 = self.tableWid.item(self.rowIndex, 1)

            self.tableWidOrderDish.insertRow(self.tableWidOrderDish.rowCount())  # 先插入行，下面在两列内添加数据
            self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 0, QTableWidgetItem(textKind))
            self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 1, QTableWidgetItem(text1))
            self.tableWidOrderDish.setItem(self.tableWidOrderDish.rowCount() - 1, 2, QTableWidgetItem(text2))
        elif sender == self.btnDel:
            rowList = [i.row() for i in self.tableWidOrderDish.selectedIndexes()]  # 得到选中行的索引，放到列表中
            for i in rowList[::-1]:  # 逆序删除，不然只删除选中行的一半
                self.tableWidOrderDish.removeRow(i)

        self.tableWid = None
        self.rowIndex = None

    def setDeskName(self, deskName):
        # deskName = self.labDeskName.text()
        # whetherPay = self.labWhetherPay.text()
        tempName = deskName
        flagCount = 2

        # lt = self.listDeskNames
        lt = []
        [lt.extend(d.keys()) for d in self.dictTodayBill.values()]
        while True:
            if tempName in lt:
                tempName = f"{deskName}({flagCount})"
                flagCount += 1
            else:
                self.labDeskName.setText(tempName)
                break
        self.listDeskNames.append(tempName)

    def slot_waitOrPay(self, whetherPay):
        try:
            sender = self.sender()
            deskName = self.labDeskName.text()

            # 如果等待客人用餐按钮的属性from等于new，说明是新创建的，就创建一个按钮。如果等于old说明已经存在，只执行上面
            # 代码，不能再创建桌号按钮了。
            if sender == self.btnWait and self.btnWait.property('from') == 'new':
                self.p.btnUnpaid.clicked.emit()
                MyBtn(self, self.p, self.p.widUnpaid)  # 自己封装的QPushButton按钮，里面改变了传进去的self的等待客人用餐按钮属性为old
            elif sender == self.btnPay:
                rep = MyDialog(self).replay()  # 自定义了一个有返回值的模态界面
                if not rep:  # 如果确认客人结账了，就关闭或者隐藏此界面的一些功能（如果有弊端，就撤消这些设置）
                    return
                self.p.btnPaid.clicked.emit()
                self.flagBtn.addToGrid(self.p.widPaid)  # 因为结账按钮是提前隐藏的，显示的时候就说明已经创建相应的按钮了
                self.dictTodayBill['未结账'].pop(deskName)  # 结账后要把未结账中此桌的键值删除，后面有加到已结账的键值中

            self.dictTodayBill[whetherPay][deskName] = {'备注': ""}
            countRow = self.tableWidOrderDish.rowCount()
            for row in range(countRow):
                item0 = self.tableWidOrderDish.item(row, 0)
                item1 = self.tableWidOrderDish.item(row, 1)
                item2 = self.tableWidOrderDish.item(row, 2)
                item3 = self.tableWidOrderDish.item(row, 3)
                kind = item0.text()
                name = item1.text()
                price = item2.text()
                if item3 == None:
                    num = '1'
                else:
                    num = item3.text()
                self.dictTodayBill[whetherPay][deskName].update({name: [kind, price, num]})

            dump(self.dictTodayBill, open(f"dataOrder/{self.dateToday}账单.json", 'w', encoding='utf-8'), indent=4,
                 ensure_ascii=False)
            self.flagClose = True
            print(whetherPay)
            self.close()

        except Exception as e:
            print('有错误', e)

    def closeEvent(self, e):
        try:
            print(self.sender())
            if self.sender() is None:
                print('信号是None')
            elif self.sender() == self.btnQuit:
                print('信号是btnQuit')
            else:
                print('信号是等待或者结账')
            # if not self.flagClose and len(self.listDeskNames):
            #     # self.p.listDeskNames = []
            #     print(self.labDeskName.text())
            #     print(self.listDeskNames)
                # self.p.listDeskNames.remove(self.labDeskName.text())
        except Exception as e:
            print(e)

class MyBtn(QPushButton):
    """自己重新封装的按钮。主要处理每个按钮点击弹出相应的客人菜单。"""
    def __init__(self, uiDishDeskName, parent, whetherPay):
        super(MyBtn, self).__init__(parent)
        self.p = parent
        self.uiDishDeskName = uiDishDeskName
        self.setFixedSize(60, 60)
        self.setText(uiDishDeskName.labDeskName.text())
        self.clicked.connect(uiDishDeskName.show)
        uiDishDeskName.btnPay.show()
        # 因为结账按钮的槽函数在Ui_NewGuests_Logic内，为了点击结账确定之后，把此按钮切换到widPaid的布局中去，设置了标记
        uiDishDeskName.flagBtn = self
        # 如果此按钮被创建，则需要保存相应的界面，里面的等待客人用餐按钮设置属性from为old.点击时就不会再创建按钮了
        uiDishDeskName.btnWait.setProperty('from', 'old')
        self.addToGrid(whetherPay)

    def addToGrid(self, whetherPay):
        """在gridlayout中的排序方法"""
        try:
            self.setStyleSheet("background:green;")
            count = len(whetherPay.children()[1:])
            row = count//10  # 行索引，其实就是整除的值
            column = count%10  # 列索引，其实就是余数（remainder）
            whetherPay.children()[0].addWidget(self, row, column)  # 第0项就是此widget的gridlayout

            if whetherPay == self.p.widPaid:
                # print(whetherPay.objectName())
                self.uiDishDeskName.btnWait.hide()
                self.uiDishDeskName.btnPay.hide()
                self.uiDishDeskName.btnChangeDesk.setDisabled(True)
                self.uiDishDeskName.widget_2.setDisabled(True)  # 添加删除按钮的容器
                self.uiDishDeskName.tabWidget.setDisabled(True)  # 标签控件
                self.uiDishDeskName.labWhetherPay.setText('已结账')
                self.uiDishDeskName.labWhetherPay.setStyleSheet('color:red;')
                self.uiDishDeskName.close()  # 关闭一些功能之后，把界面关了
                self.setStyleSheet("background:red;")

        except Exception as e:
            print('错误', e)

class MyDialog(QDialog, Ui_Dialog):
    """此弹窗，直接实例并调用replay函数，可以得到返回值"""
    def __init__(self, parent):
        super(MyDialog, self).__init__(parent)
        self.setupUi(self)
        self.flag = False
        self.pushButton_3.clicked.connect(self.close)  # 取消按钮
        self.exec()

    @pyqtSlot(bool)
    def on_pushButton_clicked(self, checkable):
        """点击编辑图标按钮后的功能设置和改变样式"""
        self.lineEdit.setReadOnly(checkable)
        if checkable:
            self.pushButton.setStyleSheet("background: rgb(255, 255, 255, 0);")
        else:  # if not checkable: 等同于 not self.lineEdit.isReadOnly()
            self.lineEdit.setFocus()
            self.pushButton.setStyleSheet("background: rgb(82, 178, 23);")
        self.pushButton.setCheckable(not checkable)


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """确定按钮。改变标记。"""
        self.flag = True
        self.close()

    def replay(self):
        """返回标记"""
        return self.flag
