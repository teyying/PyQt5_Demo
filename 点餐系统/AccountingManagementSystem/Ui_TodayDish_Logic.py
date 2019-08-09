from json import dump, load
from time import strftime, localtime, time

from PyQt5.QtCore import pyqtSlot, Qt, QItemSelectionModel, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView

from Ui_TodayDish import Ui_TodayDish


#   return Super().eventFilter(obj,eve)

class Ui_TodayDish_Logic(QWidget, Ui_TodayDish):
    def __init__(self, parent):
        super(Ui_TodayDish_Logic, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground)  # 这一句可以解决QWidget不显示图片的问题。不用重写paintEvent了。
        self.setWindowIcon(QIcon('icon.png'))
        self.dateToday = parent.dateToday
        self.widAllDish.hide()  # 先隐藏历史全部菜谱widget，需要时点击显示
        self.loadAllDishData()  # 提前加载历史全部菜谱的数据，需要更新时调用此方法并给参数True.
        self.setFixedWidth(405)

        # 一些控件的信号与槽设置
        btns = [self.btnAddRow, self.btnDelRow, self.btnMoveUp, self.btnMoveDn]
        tableWids = [self.tableWidColdDish2, self.tableWidHotDishes2, self.tableWidDrinks2, self.tableWidOther2]
        [i.clicked.connect(self.slot_btns_clicked) for i in btns]
        [i.cellDoubleClicked.connect(self.slot_tableWid2s_cellDoubleClicked) for i in tableWids]

        for i in tableWids:
            i.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            eval(f"self.{i.objectName()[:-1]}.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)")

    def slot_btns_clicked(self):
        sender = self.sender()
        tabName = self.tabWidget.currentWidget().objectName()
        name = tabName[3:]
        if sender == self.btnAddRow:  # 按钮添加行：在最后添加一行（不是在选中行下方添加一行）
            eval(f"self.tableWid{name}.insertRow(self.tableWid{name}.rowCount())")
        elif sender == self.btnDelRow:  # 按钮删除行：删除选中一行或多行
            rowList = eval(f"[i.row() for i in self.tableWid{name}.selectedIndexes()]")  # 得到选中行的索引，放到列表中
            for i in rowList[::-1]:  # 逆序删除，不然只删除选中行的一半
                eval(f"self.tableWid{name}.removeRow(i)")
        else:
            tableObj = eval(f"self.tableWid{name}")  # 获取表格对象
            m_CurrentRow = eval(f"self.tableWid{name}.currentRow()")  # 获取当前行的Index
            # 按钮上移(其实是向上交换数据)：未选择数据之前，返回值是-1,选中第一行返回值是0
            if sender == self.btnMoveUp and m_CurrentRow > 0:  # 因为是向上交换，行索引不能是0(第1行上没东西了)
                self.swapTwoRow(tableObj, m_CurrentRow, m_CurrentRow - 1)  # 调用自定义的方法，减1是向上移动
            # 按钮下移：因为是向下交换数据，选中最后一行之后是没东西的，所以要小于总行数(表格是从0开始计数的)
            elif sender == self.btnMoveDn and -1 < m_CurrentRow < tableObj.rowCount() - 1:
                self.swapTwoRow(tableObj, m_CurrentRow, m_CurrentRow + 1)  # 调用自定义的方法，加1是向下移动

    def swapTwoRow(self, tableObj, selectRow, targetRow):
        """QTableWidget交换两行的数据，实现按键数据上下移动"""
        selectRowList = []  # 创建两个列表用于储存表格字符串数据
        targetRowList = []
        # 得到需要交换的两行的数据
        for i in range(2):  # 因为只有两列，所以要循环两次
            selectRowItem = tableObj.item(selectRow, i)  # 如果有数据，就是QTableWidgetItem类型，否则为None
            targetRowItem = tableObj.item(targetRow, i)  # 同上
            if selectRowItem == None:  # 如果为None,就随便给它一个''空数据，不然None是没有text()方法的
                selectRowItemText = ''
            else:
                selectRowItemText = selectRowItem.text()
            if targetRowItem == None:  # 同上
                targetRowItemText = ''
            else:
                targetRowItemText = targetRowItem.text()

            selectRowList.append(selectRowItemText)  # 选择的行，获取文本，并添加进字符串列表
            targetRowList.append(targetRowItemText)  # 目标的行，获取文本，并添加进字符串列表
        # 交换文本
        for i in range(2):
            tableObj.setItem(selectRow, i, QTableWidgetItem(targetRowList[i]))  # 交换文本
            tableObj.setItem(targetRow, i, QTableWidgetItem(selectRowList[i]))  # 交换文本
            tableObj.selectRow(targetRow)

    def slot_tableWid2s_cellDoubleClicked(self):
        try:
            sender = self.sender()
            row = sender.currentRow()
            text0 = sender.item(row, 0)
            text1 = sender.item(row, 1)

            self.tabWidget.setCurrentIndex(self.tabWidget_2.currentIndex())  # 在哪一类（比如热菜）里面添加，就把今天菜谱也设置到那一页，对用户实时查看友好
            tableWidName = sender.objectName()[:-1]  # tableWidColdDish2把最后一个字符去掉就是今日菜谱里QTableWidget的对象名了
            tableWid = eval(f'self.{tableWidName}')  # 得到今天菜谱对应的的QTableWidget对象，以便后面操作
            tableWid.insertRow(tableWid.rowCount())  # 先插入行，下面在两列内添加数据
            # self.btnAddRow.clicked.emit()
            tableWid.setItem(tableWid.rowCount() - 1, 0, QTableWidgetItem(text0))
            tableWid.setItem(tableWid.rowCount() - 1, 1, QTableWidgetItem(text1))
            # print(tableWid.objectName(), tableWid.rowCount())
        except Exception as e:
            pass

    @pyqtSlot(bool)
    def on_btnAllDish_clicked(self, flag):
        """按钮（显示全部菜谱）的槽函数"""
        if not flag:  # 第一次bool值是False，所以要通过not转换成True，注意此方法最后一行注释
            self.setFixedWidth(735)
            self.btnAllDish.setText("关闭历史\n全部菜谱")
        else:
            self.setFixedWidth(405)
            self.btnAllDish.setText("显示历史\n全部菜谱")
        self.widAllDish.setVisible(not flag)
        self.btnAllDish.setCheckable(not flag)  # 这句解决了用装饰器信号，给btn传bool值的问题

    @pyqtSlot()
    def on_btnSave_clicked(self):
        """保存菜谱按钮"""
        import time
        try:
            dict0 = dict()
            dict1 = dict()
            dict2 = dict()
            dict3 = dict()
            for i in range(4):  # 总共有“凉菜，热菜，酒水，其它”四页。
                name = self.tabWidget.widget(i).objectName()[3:]  # 得到QTabWidget对象名第三位之后的字符，让下一句拼接
                tableObj = eval(f"self.tableWid{name}")  # 得到QTableWidget对象，以便后面操作
                countRow = tableObj.rowCount()
                for row in range(countRow + 1):
                    item0 = tableObj.item(row, 0)
                    item1 = tableObj.item(row, 1)
                    if item0 == None and item1 == None:  # 这句可以不用，字典是不会保存键值都为 '' 的数据，后面代码没必要执行才写
                        continue
                    if item0 == None:  # 如果为None,就随便给它一个''空数据，不然None是没有text()方法的
                        dishName = ''
                    else:
                        dishName = item0.text()
                    if item1 == None:
                        price = ''
                    else:
                        price = item1.text()
                    exec(f"dict{i}[dishName] = price")

            # 写入今日日期的菜谱json文件
            dictDish = {'凉菜': dict0, '热菜': dict1, '酒水': dict2, '其它': dict3}
            # dateToday = strftime('%Y-%m-%d', localtime(time.time()))  # 得到日期字符串
            dump(dictDish, open(f"dataDish/{self.dateToday}菜谱.json", 'w', encoding='utf-8'), indent=4,
                 ensure_ascii=False)

            # 更新一下历史全部菜谱json文件，字典会排除重复的键。这里更新的是json文件，下面实时更新的是历史全部菜谱的显示
            dataAllDish = load(open('dataDish/历史全部菜谱.json', 'r', encoding='utf-8'))
            dataAllDish['凉菜'].update(dict0)  # 为了保存所有写过的菜谱，外层键是不应该变的，所以用这种方式更新
            dataAllDish['热菜'].update(dict1)
            dataAllDish['酒水'].update(dict2)
            dataAllDish['其它'].update(dict3)
            dump(dataAllDish, open('dataDish/历史全部菜谱.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

            QMessageBox.information(self, '消息', '已保存', QMessageBox.Ok)
            self.loadAllDishData(True)  # 实时更新一下历史全部菜谱，可能有新菜品。没必要再做是否有新菜品再更新的逻辑，数据量不大
            self.close()
        except Exception as e:
            pass

    def loadAllDishData(self, updata=False):
        """历史全部菜谱widget内的QTableWidget数据加载或者实时更新"""
        from os.path import isfile
        if updata:
            # 先清除各个QTableWidget中的所有行，会重复添加。
            for i in [self.tableWidColdDish2, self.tableWidHotDishes2, self.tableWidDrinks2, self.tableWidOther2]:
                for j in range(i.rowCount()):
                    i.removeRow(0)

        # 把“历史全部菜谱.json”的数据放入各个QTableWidget中
        dataAllDish = load(open('dataDish/历史全部菜谱.json', 'r', encoding='utf-8'))
        for _k, _v in dataAllDish.items():
            for k, v in _v.items():
                if _k == '凉菜':
                    tableWid = self.tableWidColdDish2
                elif _k == '热菜':
                    tableWid = self.tableWidHotDishes2
                elif _k == '酒水':
                    tableWid = self.tableWidDrinks2
                elif _k == '其它':
                    tableWid = self.tableWidOther2
                tableWid.insertRow(tableWid.rowCount())
                tableWid.setItem(tableWid.rowCount() - 1, 0, QTableWidgetItem(k))
                tableWid.setItem(tableWid.rowCount() - 1, 1, QTableWidgetItem(v))

        # 如果今天已经添加过菜谱，就加载它。
        if isfile(f'dataDish/{self.dateToday}菜谱.json'):
            # 先清除各个QTableWidget中的所有行，会重复添加。
            for i in [self.tableWidColdDish, self.tableWidHotDishes, self.tableWidDrinks, self.tableWidOther]:
                for j in range(i.rowCount()):
                    i.removeRow(0)
            dataTodayDish = load(open(f'dataDish/{self.dateToday}菜谱.json', 'r', encoding='utf-8'))
            for _k, _v in dataTodayDish.items():
                for k, v in _v.items():
                    if _k == '凉菜':
                        tableWid = self.tableWidColdDish
                    elif _k == '热菜':
                        tableWid = self.tableWidHotDishes
                    elif _k == '酒水':
                        tableWid = self.tableWidDrinks
                    elif _k == '其它':
                        tableWid = self.tableWidOther
                    tableWid.insertRow(tableWid.rowCount())
                    tableWid.setItem(tableWid.rowCount() - 1, 0, QTableWidgetItem(k))
                    tableWid.setItem(tableWid.rowCount() - 1, 1, QTableWidgetItem(v))

# from sys import argv
# from PyQt5.Qt import *
#
# if __name__ == '__main__':
#     app = QApplication(argv)
#     window = Ui_TodayDish_Logic()  # 实例化主窗口
#     window.show()
#     exit(app.exec_())
