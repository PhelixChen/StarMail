# -*- coding: utf-8 -*-
import os
import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import codecs

import shutil

from Info import *
poplib._MAXLINE=20480
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    try:
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        else:
             value = value.decode('gbk')
        return value
    except:
        pass


def print_info(msg, num, indent=0):
    if indent == 0:
        strInfo = ''
        for header in ['From', 'Subject','Date']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                elif header == 'Date':
                    value = value
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
            strInfo = strInfo + ('%s%s: %s\r\n' % ('  ' * indent, header, value))

        try:
            os.makedirs(getName()+'/mail/info')
        except:
            pass
        try:
            strnum = getName()+'/mail/info/' + str(num) + '.txt'
            with codecs.open(strnum, 'w', 'gbk') as fp:
                fp.write(strInfo)
        except:
            strnum = getName() + '/mail/info/' + str(num) + '.txt'
            with codecs.open(strnum, 'w', 'gbk') as fp:
                fp.write("None")

    try:
        #filename1 = msg.get_filename()
        filename1 = msg.get_param("name")
        if filename1:
            try:
                os.makedirs(getName() + '/attachment/' + str(num))
            except:
                pass
            filename1 = str(filename1)
            #print 'filename: ' + filename1
            data = msg.get_payload(decode=True)
            fileName =  getName() + "/attachment/"+str(num)+"/%s" % (filename1)
            #try:
            fEx = open(fileName, 'wb')
            fEx.write(data)
            fEx.close()
            #except:
                #pass
                # fileName = getName()+"/attachment/"+str(num)+"/%s" % (str(num))
                # fEx = open(fileName, 'wb')
            # fEx.write(data)
            # fEx.close()
    except:
        pass
    try:
        os.makedirs(getName() + '/mail')
    except:
        pass
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, num, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            content11 = content
            if charset:
                try:
                    content11 = content.decode(charset)
                except:
                    pass
            print('%sText: %s' % ('  ' * indent, content11))

            strnum = getName()+'/mail/' + str(num) + '.html'
            fp = open(strnum, 'w+')
            fp.write(content)
            fp.close()
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
            pass


# email = raw_input('Email: ')
# password = raw_input('Password: ')
# pop3_server = raw_input('POP3 server: ')

email = 'weilemeng.1@163.com'
password = 'love-09weilemeng'
pop3_server = 'pop.163.com'

def login(email, password, server):
    # server = poplib.POP3_SSL(pop3_server)
    print(server.getwelcome())
    # 认证:

    server.user(email)
    server.pass_(password)

    #print('Messages: %s. Size: %s' % server.stat())


def login1(email, password, pop3_server):
    server = poplib.POP3_SSL(pop3_server)
    print(server.getwelcome())
    # 认证:
    try:
        server.user(email)
        server.pass_(password)
        #print('Messages: %s. Size: %s' % server.stat())
        server.quit()
        return "1"
    except:
        return "-1"


def receMail(server):
    resp, mails, octets = server.list()
    mailscount = len(mails)
    setCount(mailscount)
    # 获取最新一封邮件, 注意索引号从1开始:

    for num in range(mailscount):
        resp, lines, octets = server.retr(num)
        # 解析邮件:
        msg = Parser().parsestr("\r\n".join(lines))
        # 打印邮件内容:
        #print ('第' + str(num) + '封邮件：')
        print_info(msg, num)



def serverQuit(server):
    server.quit()

def getMail(email, password, pop3_server):
    server = poplib.POP3_SSL(pop3_server)
    login(email, password, server)
    receMail(server)
    serverQuit(server)


def getmail(email, password, pop3_server):
    #print '1111'
    # for root, dirs, files in os.walk(getName()+'/mail/info', True):
    #     for name in files:
    #         pathname = os.path.splitext(os.path.join(root, name))
    #         if (pathname[1] == ".txt"):
    #             os.remove(os.path.join(root, name))
    # try:
    #     shutil.rmtree(getName()+'/mail/info')
    # except:
    #     pass
    try:
        os.makedirs(getName() + '/mail/info')
    except:
        pass
    try:
        os.makedirs(getName() + '/mail/messageID')
    except:
        pass
    server = poplib.POP3_SSL(pop3_server)
    #server.set_debuglevel(1)
    print(server.getwelcome())
    # 认证:
    server.user(email)
    server.pass_(password)
    print('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()
    mailscount = len(mails)
    #lenth = sum([len(files) for root,dirs,files in os.walk(getName()+'/mail/info/')])
    # 获取最新一封邮件, 注意索引号从1开始:
    #try:
    uid = server.uidl()[1]
    #print uid
    for num in range(mailscount,0,-1):
        resp, lines, octets = server.retr(num)
    # 解析邮件:
        msg = Parser().parsestr("\r\n".join(lines))
    # 打印邮件内容:
    #     global receFlag
    #     receFlag = 1
    #     messageID = msg.get("Message-ID", '')
    #     try:
    #         os.makedirs(getName() + '/mail/messageID')
    #     except:
    #         pass
    #     try:
    #         strnum = getName() + '/mail/messageID/' 'messageID.txt'
    #         with codecs.open(strnum, 'r', 'gbk') as fp:
    #             msgID = fp.read()
    #             if messageID in msgID:
    #                 receFlag = 0
    #             else:
    #                 pass
    #     except:
    #         pass
        #if receFlag:
            # fp2 = open(getName()+'/mail/messageID/messageID.txt','a')
            # string =  '%s;\r\n' % str(messageID)
            # fp2.write(string)
            # lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/mail/info/')])
            #print lenth
        #print num
        messageID = uid[num-1].split(' ')[1]
        #print messageID
        messageIDFileName = r''+getName()+'/mail/messageID/'+messageID+'.txt'
        if os.path.exists(messageIDFileName):
            break
        else:
            strpath = getName()+'/mail/messageID/'+messageID+'.txt'
            fp2 = open(strpath, 'w')
            fp2.write(messageID)
            print ('第' + str(num) + '封邮件：')
        #print "aaaa4"
            print_info(msg,num)
    # except:
    #     pass

    # 慎重:将直接从服务器删除邮件:
    # server.dele(len(mails))
    # 关闭连接:
    server.quit()

if __name__ == '__main__':
    email = 'weilemeng.1@163.com'
    password = 'love-09weilemeng'
    pop3_server = 'pop.163.com'
    getmail(email, password, pop3_server)
