# -*- coding: utf-8 -*-
import os

from PyQt4 import QtCore, QtGui
from timerWindow import *


class timerThread(QtCore.QThread):
    """docstring for BigWorkThread"""
    def __init__(self, parent=None):
        super(timerThread, self).__init__(parent)



    #重写 run() 函数，在里面干大事。
    def run(self):
        timerWin()