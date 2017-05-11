#coding=utf-8


import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QTextCodec

from PyQt4.QtGui import *
from receiver import login1
from MainEmailWindow import *
import poplib
from Info import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        usr = QLabel(self.tr("用户："))
        pwd = QLabel(self.tr("密码："))
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 3);
        gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 3);


        okBtn = QPushButton(self.tr("确定"))
        detailBtn = QPushButton(self.tr("详细"))
        okBtn.setStyleSheet("QPushButton{background-color:#6495ED;width:75px;height:20px; "
                                      "border-radius: 5px;margin-right:3px;margin-bottom: 3px}""QPushButton:hover{background-color:#F0FFFF;}")
        detailBtn.setStyleSheet("QPushButton{background-color:#6495ED;width:75px;height:20px; "
                                      "border-radius: 5px;margin-bottom: 3px}""QPushButton:hover{background-color:#F0FFFF;}")
        btnLayout = QHBoxLayout()

        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(detailBtn)

        smtp = QLabel(self.tr("SMTP："))
        pop = QLabel(self.tr("POP："))
        self.smtpLineEdit = QLineEdit('smtp.163.com')
        self.popLineEdit = QLineEdit('pop.163.com')

        self.detailWidegt = QWidget()
        detailgridLayout = QGridLayout(self.detailWidegt)
        detailgridLayout.addWidget(smtp, 0, 0, 1, 1)
        detailgridLayout.addWidget(pop, 1, 0, 1, 1)
        detailgridLayout.addWidget(self.smtpLineEdit, 0, 1, 1, 3)
        detailgridLayout.addWidget(self.popLineEdit, 1, 1, 1, 3)
        self.detailWidegt.hide()

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)
        dlgLayout.addWidget(self.detailWidegt)
        dlgLayout.setSizeConstraint(QLayout.SetFixedSize)
        dlgLayout.setSpacing(10)



        self.setLayout(dlgLayout)
        okBtn.clicked.connect(self.accept)
        detailBtn.clicked.connect(self.slotExtension)
        self.setWindowTitle(self.tr("登录"))
        # self.resize(300, 200)

        palette1 = QtGui.QPalette(self)
        palette1.setBrush(self.backgroundRole(),  QtGui.QBrush(QtGui.QPixmap('background.png')))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        #self.color = QtGui.QColor(0, 0, 255)
        # self.setStyleSheet('QWidget{background-color:%s}'%self.color.name()) #利用样式表改变背景色



        self.setWindowIcon(QtGui.QIcon('mail.png'))
        self.setFixedSize(300,200)


    def accept(self):
        name = self.usrLineEdit.text()
        psw = self.pwdLineEdit.text()
        smtpInfo = self.smtpLineEdit.text()
        popInfo = self.popLineEdit.text()
        setName(str(name))
        setPsw(str(psw))
        setSmtp(str(smtpInfo))
        setPop(str(popInfo))


        self.flag = "-1"
        try:
            string = getName().split('@')[1]
            if string == 'qq.com':
                server = poplib.POP3_SSL(str(popInfo))
            else:
                server = poplib.POP3(str(popInfo))
            server.user(name)
            server.pass_(psw)
            server.quit()
            #login1(name, psw, "pop.163.com")
            self.flag = "1"
            # try:
            #     os.mkdir(str(name))
            # except:
            #     pass
            # path = str(name) + '/' + str(name) + '.txt'
            # #print path
            # for root, dirs, files in os.walk(path, True):
            #     for name in files:
            #         pathname = os.path.splitext(os.path.join(root, name))
            #         if (pathname[1] == ".txt"):
            #             os.remove(os.path.join(root, name))
            # with codecs.open(path, 'w', 'gbk') as fp:
            #     fp.write("name:" + str(name) + "\r\n")
            #     fp.write("password:" + str(psw) + "\r\n")
            #     fp.write("smtp:" + str(smtpInfo) + "\r\n")
            #     fp.write("pop:" + str(popInfo) + "\r\n")
        except:
            self.flag = "-1"

        if self.flag == "1":
            super(LoginDlg, self).accept()

        # if self.usrLineEdit.text() == "admin" and self.pwdLineEdit.text() == "000000":
        #     super(LoginDlg, self).accept()
        #     # mainwindow = MainWindow()
        #     # mainwindow.show()
        elif self.usrLineEdit.text() != "" or self.pwdLineEdit.text() != "" or self.flag == "-1":
            QMessageBox.warning(self,
                    self.tr("警告"),
                    self.tr("用户名或密码错误！"),
                    QMessageBox.Yes)
            self.usrLineEdit.setFocus()

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes|QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
    def slotExtension(self):
        if self.detailWidegt.isHidden():
            self.detailWidegt.show()
        else:
            self.detailWidegt.hide()

    def trayClick(self, reason):
        # 双击托盘
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.showNormal()
        else:
            pass

    def trayMenu(self):
        # 右击托盘弹出的菜单
        img_main = QtGui.QIcon("images/main.png")
        img_exit = QtGui.QIcon("images/exit.png")
        self.trayIcon.setToolTip(u"学生体能健康测试软件")
        self.restoreAction = QtGui.QAction(img_main, u"打开主窗口", self)
        self.restoreAction.triggered.connect(self.showNormal)
        self.quitAction = QtGui.QAction(img_exit, u"退出", self)
        self.quitAction.triggered.connect(QtGui.qApp.quit)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = LoginDlg()
    dlg.show()
    dlg.exec_()
    app.exit()