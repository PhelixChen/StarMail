#coding=utf-8
from demo import *
from MainEmailWindow import *
import sys

def login():
    dialog = LoginDlg()
    if dialog.exec_():
        return True
    return False
if __name__ == '__main__':
    app = QApplication(sys.argv)
    if login():
        win = MainWindow()
        win.show()
        sys.exit(app.exec_())