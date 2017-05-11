# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import time
from Info import *
from receiver import getmail
from timerWindow import timerWin3
#继承 QThread 类
class receThread(QtCore.QThread):
    """docstring for BigWorkThread"""
    def __init__(self, parent=None):
        super(receThread, self).__init__(parent)

    #重写 run() 函数，在里面干大事。
    def run(self):
        email = getName()
        password = getPsw()
        pop3_server = getPop()
        getmail(email, password, pop3_server)
        time.sleep(10)
        timerWin3()