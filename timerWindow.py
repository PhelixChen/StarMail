#coding=utf-8
import sys
from PyQt4 import Qt

from PyQt4 import QtGui

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from Info import getSendFlag


class timerWindow(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"正在发送...", self)
        #if getSendFlag():
           # self.setText()
        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

class timerWindow1(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"发送成功", self)

        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

class timerWindow2(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"正在收取...", self)

        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

class timerWindow3(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"收取完毕", self)

        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

class timerWindow4(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"发送失败", self)

        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

class timerWindow5(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"保存草稿成功", self)

        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

class timerWindow6(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        self.qbtn_one = QtGui.QPushButton(u"保存草稿失败", self)

        self.qbtn_one.setGeometry(0, 0, 150, 40)
        self.qbtn_one.setStyleSheet("QPushButton{background-color:#16A085;border:none;color:#ffffff;font-size:20px;}"
                               "QPushButton:hover{background-color:#333333;}")
        self.setFixedSize(150,60)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.show()

        self.qbtn_one.clicked.connect(self.close)
        QTimer.singleShot(2000, self.close)  # 设置10s后自动退出

def timerWin():
    #app = QApplication(sys.argv)
    dlg = timerWindow()
    dlg.show()
    dlg.exec_()

def timerWin1():
    # app = QApplication(sys.argv)
    dlg = timerWindow1()
    dlg.show()
    dlg.exec_()

def timerWin2():
    dlg = timerWindow2()
    dlg.show()
    dlg.exec_()

def timerWin3():
    dlg = timerWindow3()
    dlg.show()
    dlg.exec_()

def timerWin4():
    dlg = timerWindow4()
    dlg.show()
    dlg.exec_()

def timerWin5():
    dlg = timerWindow5()
    dlg.show()
    dlg.exec_()

def timerWin6():
    dlg = timerWindow6()
    dlg.show()
    dlg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # dlg = timerWindow()
    # dlg.show()
    # QTimer.singleShot(1000, app.quit)  # 设置10s后自动退出
    # app.exec_()
    timerWin()
    app.exec_()

