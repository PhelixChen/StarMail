# -*- coding: utf-8 -*-
import threading

import re

import chardet
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import sys
from receiver import *
from PyQt4.QtGui import *
from textedit import *
from Info import *
from timerWindow import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("%s -StarMail" % getName())
        self.setWindowIcon(QtGui.QIcon('mail.png'))
        #self.createMenus()
        palette1 = QtGui.QPalette(self)
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('bk1.png')))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)


        self.receButton = QPushButton(self.tr("收件箱"))
        self.sendButton = QPushButton(self.tr("发件箱"))
        self.junkButton = QPushButton(self.tr("垃圾箱"))
        self.draftButton = QPushButton(self.tr("草稿箱"))
        self.receButton.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                 "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.sendButton.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.junkButton.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.draftButton.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.receButton)
        self.vbox.addWidget(self.sendButton)
        self.vbox.addWidget(self.junkButton)
        self.vbox.addWidget(self.draftButton)



        self.listWidegt = QListWidget()
        self.listWidegt.setSortingEnabled(1)
        self.listWidegt.setSpacing(5)
        self.listWidegt.setStyleSheet("QListWidget{background-image: url(:/images/bk3.png);}")

        #self.listWidegt.setStyleSheet("QListWidget{background-color:	#ADD8E6;}")

        self.webView = QWebView()
        self.webView.setTextSizeMultiplier(1.2)
        self.webView.setWindowOpacity(0.5)
        self.webView.setPalette(palette1)
        #self.webView.setStyleSheet("QWebView{background-color:	#ADD8E6;}")
        self.webView.setStyleSheet("QListWidget{background-image: url(:/images/bk3.png);}")


        self.rbtn = QPushButton(self.tr("收信"))
        self.sbtn = QPushButton(self.tr("写信"))
        self.rebtn = QPushButton(self.tr("回信"))
        self.tbtn = QPushButton(self.tr("转发"))
        self.rbtn.setStyleSheet("QPushButton{background-color:#6495ED;width:70px;height:20px; border-radius: 5px;margin-right:10px;}""QPushButton:hover{background-color:#F0FFFF;}")
        self.tbtn.setStyleSheet("QPushButton{background-color:#6495ED;width:70px;height:20px; border-radius: 5px;margin-right:10px;}""QPushButton:hover{background-color:#F0FFFF;}")
        self.sbtn.setStyleSheet("QPushButton{background-color:#6495ED;width:70px;height:20px; border-radius: 5px;margin-right:10px;}""QPushButton:hover{background-color:#F0FFFF;}")
        self.rebtn.setStyleSheet("QPushButton{background-color:#6495ED;width:70px;height:20px; border-radius: 5px;margin-right:10px;}""QPushButton:hover{background-color:#F0FFFF;}")
        self.rbtn.clicked.connect(self.getMailThread)
        self.sbtn.clicked.connect(self.send)
        self.rebtn.clicked.connect(self.replyMail)
        self.tbtn.clicked.connect(self.transMail)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.rbtn)
        self.hbox.addWidget(self.sbtn)
        self.hbox.addWidget(self.rebtn)
        self.hbox.addWidget(self.tbtn)
        self.hbox.setSpacing(5)
        self.hbox.setMargin(5)
        self.hbox.addStretch(1)

        mainLayout1 = QVBoxLayout()
        mainLayout1.setMargin(5)
        mainLayout1.setSpacing(5)

        mainLayout = QHBoxLayout()
        mainLayout.setMargin(5)
        mainLayout.setSpacing(5)
       # mainLayout.addWidget(self.listView)
        self.vbox.addStretch()

        sublabel = QLabel(self.tr("主题："))
        self.text1 = QLineEdit()
        self.text1.setFixedSize(300,20)
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(sublabel)
        hlayout1.addWidget(self.text1)
        hlayout1.addStretch(1)
        self.label2 = QLabel(self.tr("发件人："))
        self.text2 = QLineEdit()
        self.text2.setFixedSize(300,20)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.label2)
        hlayout2.addWidget(self.text2)
        hlayout2.addStretch(1)

        hlayout3 = QHBoxLayout()
        hlayout3.addLayout(hlayout1)
        hlayout3.addLayout(hlayout2)

        self.webLayout = QVBoxLayout()
        self.webLayout.addLayout(hlayout3)
        #webLayout.addLayout(hlayout2)

        #附件按钮
        btn = QPushButton("SSS")
        self.hbox1 = QHBoxLayout()
        self.hbox1.addStretch(1)
        #self.webLayout.addLayout(self.hbox1)

        self.webLayout.addWidget(self.webView)
        self.webLayout.addLayout(self.hbox1)

        mainLayout.addLayout(self.vbox)
        mainLayout.addWidget(self.listWidegt)
        mainLayout.addLayout(self.webLayout)
        #mainLayout.addWidget(self.webView, 0, Qt.AlignHCenter)
        #mainLayout.setStretchFactor(self.listWidegt, 1)
        #mainLayout.setStretchFactor(self.webView, 5)

        mainLayout1.addLayout(self.hbox)
        mainLayout1.addLayout(mainLayout)

        self.listWidegt.sortItems(1)
        widegt = QWidget()
        widegt.setLayout(mainLayout1)
        self.receButton.clicked.connect(self.receButton1)
        self.sendButton.clicked.connect(self.sendButton1)
        self.junkButton.clicked.connect(self.junkButton1)
        self.draftButton.clicked.connect(self.draftButton1)
        widegt.connect(self.listWidegt, SIGNAL('itemClicked(QListWidgetItem *)'), self.listViewOnClick)
        self.setCentralWidget(widegt)

        # palette1 = QtGui.QPalette(self)
        # palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('background1.png')))
        # self.setPalette(palette1)
        # self.setAutoFillBackground(True)

        #self.resize(1085, 608)
        self.setFixedSize(1085,608)

    flag = 1
    setSendBtn(1)
    def createMenus(self):
        receMenu = self.menuBar().addMenu(self.tr("收取"))
        sendMenu = self.menuBar().addMenu(self.tr("写邮件"))
        replyMenu = self.menuBar().addMenu(self.tr("回复"))
        tranMenu = self.menuBar().addMenu(self.tr("转发"))

        #receMenu.addAction(self.getMail1)

    def getMailThread(self):
        #print 'aaaaa'
        timerWin2()
        t = threading.Thread(target=self.getMail1())
        t.start()

    def getMail1(self):
        from receThreads import receThread
        # 新建对象
        self.receThread1 = receThread()
        # 开始执行run()函数里的内容
        self.receThread1.start()



    def createTools(self):
        receMail = self.addToolBar("rece")
        sendMail = self.addToolBar("send")

    def listViewSet(self):
        for t in range(100):
            listAll = self.listWidegt.count()
            for ii in range(-1, listAll):
                item = self.listWidegt.takeItem(ii)
                item = None

        lenth = sum([len(files) for root,dirs,files in os.walk(getName()+'/mail/info/')])
        #print lenth
        for num in range(lenth):
            strnum = getName()+'/mail/info/' + str(num+1) + '.txt'
            s = "%05d" % (num+1)
            try:
                with codecs.open(strnum, 'r', 'gbk') as fp:
                    info = fp.read()
                    info = s + ': \r\n' + info
                    self.listWidegt.insertItem(4, self.tr(info))
            except:
                info = s + ': \r\n' +"None"
                self.listWidegt.insertItem(4, self.tr(info))

        # for i in range(100):
        #     self.listWidegt.insertItem(4, self.tr(str(i)+".html"))

    def listViewSet1(self):
        for t in range(100):
            listAll = self.listWidegt.count()
            for ii in range(-1, listAll):
                item = self.listWidegt.takeItem(ii)
                item = None

        lenth = sum([len(files) for root,dirs,files in os.walk(getName()+'/sendmail/info/')])
        #print lenth
        for num in range(lenth):
            strnum = getName()+'/sendmail/info/' + str(num+1) + '.txt'
            s = "%05d" % (num+1)
            try:
                with codecs.open(strnum, 'r', 'gbk') as fp:
                    info = fp.read()
                    info = s + ': \r\n' + info
                    self.listWidegt.insertItem(4, self.tr(info))
            except:
                info = s + ': \r\n' +"None"
                self.listWidegt.insertItem(4, self.tr(info))

    def listViewSet3(self):
        for t in range(100):
            listAll = self.listWidegt.count()
            for ii in range(-1, listAll):
                item = self.listWidegt.takeItem(ii)
                item = None

        lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/draftmail/info/')])
        # print lenth
        for num in range(lenth):
            strnum = getName() + '/draftmail/info/' + str(num + 1) + '.txt'
            s = "%05d" % (num + 1)
            try:
                with codecs.open(strnum, 'r', 'gbk') as fp:
                    info = fp.read()
                    info = s + ': \r\n' + info
                    self.listWidegt.insertItem(4, self.tr(info))
            except:
                info = s + ': \r\n' + "None"
                self.listWidegt.insertItem(4, self.tr(info))

    def listViewSet2(self):
        for t in range(100):
            listAll = self.listWidegt.count()
            for ii in range(-1, listAll):
                item = self.listWidegt.takeItem(ii)
                item = None



    def listViewOnClick(self):

        row = self.listWidegt.currentRow()
        if getDraft():
            lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/draftmail/info/')])
            string = getName() + '/draftmail/' + str(lenth - row) + '.html'
            setNum(str(lenth - row))
        elif flag:
            lenth = sum([len(files) for root, dirs, files in os.walk(getName()+'/mail/info/')])
            string = getName()+'/mail/' + str(lenth-row) + '.html'
            setNum('')
        else:
            lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/sendmail/info/')])
            string = getName() + '/sendmail/' + str(lenth - row) + '.html'
            setNum('')

        file = open(string, 'r')
        html = file.read()
        try:
            html = html.decode('utf-8')
        except:
            html = html.decode('gbk')
        setHtml(html)
        self.webView.setHtml(html)
        self.webView.show()

        if getDraft():
            strnum = getName() + '/draftmail/info/' + str(lenth - row) + '.txt'
        elif flag:
            strnum = getName()+'/mail/info/' + str(lenth-row) + '.txt'
        else:
            strnum = getName() + '/sendmail/info/' + str(lenth - row) + '.txt'
        try:
            with codecs.open(strnum, 'r', 'gbk') as fp:
                info = fp.readline()
                info = info.split(':')[1]
                print info
                self.text2.setText(self.tr(info))
                info = fp.readline()
                info = info.split(':')[1]
                setReplySub(info)
                info  = info[0:25]+ '...'
                print info
                self.text1.setText(self.tr(info))

                #self.listWidegt.insertItem(4, self.tr(info))
        except:
            pass
            info = "None"
            self.text1.setText(self.tr(info))
            self.text2.setText(self.tr(info))

        count = self.hbox1.count()
        for ii in range(count):
            item = self.hbox1.itemAt(ii)
            print ii
            self.hbox1.removeItem(item)
        self.webLayout.removeItem(self.hbox1)
        self.hbox1 = QHBoxLayout()
        self.hbox1.addStretch(1)
        self.webLayout.addLayout(self.hbox1)
        self.attachment()

    def receButton1(self):
        global flag
        flag = 1
        setSendBtn(1)
        self.label2.setText(self.tr("发件人："))
        self.listViewSet()
        setDraft(0)

    def sendButton1(self):
        global flag
        flag = 0
        setSendBtn(0)
        self.label2.setText(self.tr("收件人："))
        self.listViewSet1()
        setDraft(0)

    def junkButton1(self):
        setSendBtn(0)
        setDraft(0)
        self.listViewSet2()

    def draftButton1(self):
        setSendBtn(0)
        setDraft(1)
        self.label2.setText(self.tr("收件人："))
        self.listViewSet3()

    def send(self):
        setReply(0)
        setTrans(0)
        print getDraft()
        if getDraft():
            toaddrInfo = str(self.text2.text())
            setToaddr(toaddrInfo)
        textEdit = TextEdit()
        #textEdit.resize(1068, 608)
        textEdit.setFixedSize(1085,608)
        textEdit.show()
        textEdit.exec_

    def replyMail(self):
        setReply(1)
        setTrans(0)
        toaddrInfo = str(self.text2.text())
        try:
            result = re.findall(".*\<(.*)\>.*", toaddrInfo)[0]
            setToaddr(result)
        except:
            setToaddr(toaddrInfo)
        textEdit = TextEdit()
        # textEdit.resize(1068, 608)
        textEdit.setFixedSize(1085, 608)
        textEdit.show()
        textEdit.exec_

    def transMail(self):
        setReply(0)
        setTrans(1)
        subInfo = self.tr(u''+self.text1.text())
        #setSub(subInfo)
        #setContent(getHtml())
        #conInfo = getHtml()
        textEdit = TextEdit()
        # textEdit.resize(1068, 608)
        textEdit.setFixedSize(1085, 608)
        textEdit.show()
        textEdit.exec_

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes|QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def attachment(self):
        #fname = QFileDialog.getOpenFileNames(self, 'Open file', 'D:/')
        if getDraft():
            pass
        else:
            row = self.listWidegt.currentRow()
            lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/mail/info/')])
            #string = getName() + '/mail/' + str(lenth - row) + '.html'
            print str(lenth - row)
            try:
                for root, dirs, files in os.walk(getName() + '/attachment/' + str(lenth - row), True):
                    for name in files:
                        print name
                        path = os.path.join(root, name)
                        print path
                        self.addAppendix(path)
            except:
                pass

    def addAppendix(self,btnname):
        self.appendixbtn = QPushButton(str(btnname.split('\\')[-1]), self)
        self.appendixbtn.setStyleSheet("QPushButton{background-color:	#F8F8FF;width:100px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#B0C4DE;}")
        self.hbox1.addWidget(self.appendixbtn)
        menu = QtGui.QMenu()
        menu.addAction(u'隐藏', lambda: self.delAppendix(self.appendixbtn))
        menu.addAction(u'另存为 ', lambda: self.saveFile(btnname))
        self.appendixbtn.setMenu(menu)
        self.appendixbtn.clicked.connect(lambda: self.delAppendix(btnname))

    def delAppendix(self,btnname):
        self.hbox1.addStretch(1)
        self.hbox1.removeWidget(btnname.setVisible(False))
        self.hbox1.addStretch(1)

    def saveFile(self,btnname):
        import os.path
        import shutil
        file_path = QFileDialog.getSaveFileName(self, 'save file', str(btnname.split('\\')[-1]))
        shutil.copy(btnname,file_path)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()