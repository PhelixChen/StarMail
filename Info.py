# -*- coding: utf-8 -*-
import codecs
name = ''
password = ''
smtpInfo = ''
popInfo = ''
lenthOfMail = ''

toaddr = ''
content = ''
sub = ''
replysub = ''
list1 = ''
appendix = ''

sendFlag = 0
messageID = ''
replyFlag = 0
transFlag = 0
html = ''
draftFlag = 0

numInfo = ''
sendBtn = 1

def setSendBtn(flag):
    global sendBtn
    sendBtn = flag

def getSendBtn():
    return sendBtn

def setNum(num):
    global numInfo
    numInfo = num

def getNum():
    return numInfo

def setDraft(flag):
    global draftFlag
    draftFlag = flag

def getDraft():
    return draftFlag

def setHtml(htmlInfo):
    global html
    html = htmlInfo

def getHtml():
    return html

def setTrans(flag):
    global transFlag
    transFlag = flag

def getTrans():
    return transFlag

def setReply(flag):
    global replyFlag
    replyFlag = flag

def getReply():
    return replyFlag

def setMessageID(id):
    global messageID
    messageID = id

def getMessageID():
    return messageID

def setSendFlag(flag):
    global sendFlag
    sendFlag = flag

def getSendFlag():
    return sendFlag

def setAppendix(tmp):
    global appendix
    appendix = tmp

def getAppendix():
    return appendix

def setName(name1):
    global name
    name = name1

def setPsw(psw):
    global password
    password = psw

def setSmtp(smtp):
    global smtpInfo
    smtpInfo = smtp

def setPop(pop):
    global popInfo
    popInfo = pop

def getName():
    global name
    return name

def getPsw():
    global password
    return password

def getSmtp():
    global smtpInfo
    return smtpInfo

def getPop():
    global popInfo
    return popInfo

def setCount(lenth):
    global lenthOfMail
    lenthOfMail = lenth

def getCount():
    global lenthOfMail
    return lenthOfMail

def setToaddr(addr):
    global toaddr
    toaddr = addr

def setContent(content1):
    global content
    content =content1

def setList(list2):
    global list1
    list1 = list2

def setSub(subject):
    global sub
    sub = subject



def getToaddr():
    return toaddr

def getContent():
    return content

def getList():
    return list1

def getSub():
    return sub

def setReplySub(subject):
    global replysub
    replysub = subject

def getReplySub():
    return replysub