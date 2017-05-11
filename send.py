# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from Info import setSendFlag
import smtplib

from timerWindow import timerWin4


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

# from_addr = raw_input('From: ')
# password = raw_input('Password: ')
# to_addr = raw_input('To: ')
# smtp_server = raw_input('SMTP server: ')



def sendMail(from_addr, password='', str='', sub='',to_addr='',appendix='',smtp_server='smtp.163.com'):
    setSendFlag(0)
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s' % from_addr)
    msg['To'] = _format_addr(u'%s' % to_addr)
    msg['Subject'] = Header(u'%s' % sub, 'utf-8').encode()
    # add MIMEText:
    print str
    msg.attach(MIMEText(u'%s' % str, 'html', 'utf-8'))

    # # add file:
    if appendix != '':
        print '1111'
        for tmp in appendix.split(";"):
            if tmp != '':
                with open(tmp, 'rb') as f:
                    mime = MIMEBase('image', 'jpg', filename=tmp)
                    mime.add_header('Content-Disposition', 'attachment', filename=tmp)
                    mime.add_header('Content-ID', '<0>')
                    mime.add_header('X-Attachment-Id', '0')
                    mime.set_payload(f.read())
                    encoders.encode_base64(mime)
                    msg.attach(mime)
        print '2222'
    try:
        server = smtplib.SMTP_SSL(smtp_server)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        setSendFlag(1)
        #timerWin1()
    except:
        setSendFlag(0)
        # #timerWin4()
        # pass

