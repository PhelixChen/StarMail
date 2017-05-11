# -*- coding: utf-8 -*-
import os

from PyQt4 import QtCore, QtGui
import time
from Info import *


#继承 QThread 类
from send import sendMail
from timerWindow import *

class sendThread(QtCore.QThread):
    """docstring for BigWorkThread"""
    def __init__(self, parent=None):
        super(sendThread, self).__init__(parent)

        self.toaddr = getToaddr()
        self.formaddr = getName()
        self.psw = getPsw()
        self.context = getContent()
        self.sub = getSub()
        self.list1 = getList()
        self.smtp = getSmtp()
        self.appendix = getAppendix()
        #print 'aaa: '+self.appendix


    def run(self):
        #global toadd
        #print self.list1[0]
        try:
            for toaddr in self.list1:
                print toaddr
                sendMail(self.formaddr, self.psw, self.context, self.sub, [toaddr], self.appendix,self.smtp)
                if getSendFlag() and (not(getReply() or getTrans())):

                    lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/sendmail/info/')])
                    try:
                        os.makedirs(getName() + '/sendmail/info')
                    except:
                        pass
                    with codecs.open(getName() + '/sendmail/' + str(lenth + 1) + '.html', 'w', 'gbk') as fp:
                        fp.write(self.context)
                    with codecs.open(getName() + '/sendmail/info/' + str(lenth + 1) + '.txt', 'a', 'gbk') as fp:
                        #fp.write('From:' + getName() + '\r\n')
                        fp.write('To:' + self.toaddr + '\r\n')
                        fp.write('Subject:' + self.sub + '\r\n')
                        ISOTIMEFORMAT = '%Y-%m-%d %X'
                        fp.write('Date:' + time.strftime(ISOTIMEFORMAT, time.localtime()) + '\r\n')
                    timerWin1()
                    if getNum():
                            os.remove(getName() + '/draftmail/' + getNum() + '.html')
                            os.remove(getName() + '/draftmail/info/' + getNum() + '.txt')
                if getSendFlag() and getReply() or getTrans():
                    timerWin1()
                    if getNum():
                            os.remove(getName() + '/draftmail/' + getNum() + '.html')
                            os.remove(getName() + '/draftmail/info/' + getNum() + '.txt')
        except:
            timerWin4()