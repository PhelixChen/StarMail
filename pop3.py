
import re, socket

__all__ = ["POP3","error_proto"]

# Exception raised when an error or invalid response is received:

class error_proto(Exception): pass

# Standard Port
POP3_PORT = 110

# POP SSL PORT
POP3_SSL_PORT = 995

# Line terminators (we always output CRLF, but accept any of CRLF, LFCR, LF)
CR = '\r'
LF = '\n'
CRLF = CR+LF


_MAXLINE = 2048


class POP3:

    """This class supports both the minimal and optional command sets.
    Arguments can be strings or integers (where appropriate)
    (e.g.: retr(1) and retr('1') both work equally well.

    Minimal Command Set:
            USER name               user(name)
            PASS string             pass_(string)
            STAT                    stat()
            LIST [msg]              list(msg = None)
            RETR msg                retr(msg)
            DELE msg                dele(msg)
            NOOP                    noop()
            RSET                    rset()
            QUIT                    quit()

    Optional Commands (some servers support these):
            RPOP name               rpop(name)
            APOP name digest        apop(name, digest)
            TOP msg n               top(msg, n)
            UIDL [msg]              uidl(msg = None)

    """


    def __init__(self, host, port=POP3_PORT,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.sock = socket.create_connection((host, port), timeout)
        self.file = self.sock.makefile('rb')
        self._debugging = 0
        self.welcome = self._getresp()


    def _putline(self, line):
        if self._debugging > 1: print '*put*', repr(line)
        self.sock.sendall('%s%s' % (line, CRLF))


    # Internal: send one command to the server (through _putline())

    def _putcmd(self, line):
        if self._debugging: print '*cmd*', repr(line)
        self._putline(line)


    # Internal: return one line from the server, stripping CRLF.
    # This is where all the CPU time of this module is consumed.
    # Raise error_proto('-ERR EOF') if the connection is closed.

    def _getline(self):
        line = self.file.readline(_MAXLINE + 1)
        if len(line) > _MAXLINE:
            raise error_proto('line too long')
        if self._debugging > 1: print '*get*', repr(line)
        if not line: raise error_proto('-ERR EOF')
        octets = len(line)
        # server can send any combination of CR & LF
        # however, 'readline()' returns lines ending in LF
        # so only possibilities are ...LF, ...CRLF, CR...LF
        if line[-2:] == CRLF:
            return line[:-2], octets
        if line[0] == CR:
            return line[1:-1], octets
        return line[:-1], octets


    # Internal: get a response from the server.
    # Raise 'error_proto' if the response doesn't start with '+'.

    def _getresp(self):
        resp, o = self._getline()
        if self._debugging > 1: print '*resp*', repr(resp)
        c = resp[:1]
        if c != '+':
            raise error_proto(resp)
        return resp


    # Internal: get a response plus following text from the server.

    def _getlongresp(self):
        resp = self._getresp()
        list = []; octets = 0
        line, o = self._getline()
        while line != '.':
            if line[:2] == '..':
                o = o-1
                line = line[1:]
            octets = octets + o
            list.append(line)
            line, o = self._getline()
        return resp, list, octets


    # Internal: send a command and get the response

    def _shortcmd(self, line):
        self._putcmd(line)
        return self._getresp()


    # Internal: send a command and get the response plus following text

    def _longcmd(self, line):
        self._putcmd(line)
        return self._getlongresp()


    # These can be useful:

    def getwelcome(self):
        return self.welcome


    def set_debuglevel(self, level):
        self._debugging = level


    # Here are all the POP commands:

    def user(self, user):
        """Send user name, return response

        (should indicate password required).
        """
        return self._shortcmd('USER %s' % user)


    def pass_(self, pswd):
        """Send password, return response

        (response includes message count, mailbox size).

        NB: mailbox is locked by server from here to 'quit()'
        """
        return self._shortcmd('PASS %s' % pswd)


    def stat(self):
        """Get mailbox status.

        Result is tuple of 2 ints (message count, mailbox size)
        """
        retval = self._shortcmd('STAT')
        rets = retval.split()
        if self._debugging: print '*stat*', repr(rets)
        numMessages = int(rets[1])
        sizeMessages = int(rets[2])
        return (numMessages, sizeMessages)


    def list(self, which=None):
        if which is not None:
            return self._shortcmd('LIST %s' % which)
        return self._longcmd('LIST')


    def retr(self, which):
        """Retrieve whole message number 'which'.

        Result is in form ['response', ['line', ...], octets].
        """
        return self._longcmd('RETR %s' % which)


    def dele(self, which):
        """Delete message number 'which'.

        Result is 'response'.
        """
        return self._shortcmd('DELE %s' % which)


    def noop(self):
        """Does nothing.

        One supposes the response indicates the server is alive.
        """
        return self._shortcmd('NOOP')


    def rset(self):
        """Unmark all messages marked for deletion."""
        return self._shortcmd('RSET')


    def quit(self):
        """Signoff: commit changes on server, unlock mailbox, close connection."""
        try:
            resp = self._shortcmd('QUIT')
        except error_proto, val:
            resp = val
        self.file.close()
        self.sock.close()
        del self.file, self.sock
        return resp

    #__del__ = quit


    # optional commands:

    def rpop(self, user):
        """Not sure what this does."""
        return self._shortcmd('RPOP %s' % user)


    timestamp = re.compile(r'\+OK.*(<[^>]+>)')

    def apop(self, user, secret):

        m = self.timestamp.match(self.welcome)
        if not m:
            raise error_proto('-ERR APOP not supported by server')
        import hashlib
        digest = hashlib.md5(m.group(1)+secret).digest()
        digest = ''.join(map(lambda x:'%02x'%ord(x), digest))
        return self._shortcmd('APOP %s %s' % (user, digest))


    def top(self, which, howmuch):
        """Retrieve message header of message number 'which'
        and first 'howmuch' lines of message body.

        Result is in form ['response', ['line', ...], octets].
        """
        return self._longcmd('TOP %s %s' % (which, howmuch))


    def uidl(self, which=None):
        if which is not None:
            return self._shortcmd('UIDL %s' % which)
        return self._longcmd('UIDL')

try:
    import ssl
except ImportError:
    pass
else:

    class POP3_SSL(POP3):

        def __init__(self, host, port = POP3_SSL_PORT, keyfile = None, certfile = None):
            self.host = host
            self.port = port
            self.keyfile = keyfile
            self.certfile = certfile
            self.buffer = ""
            msg = "getaddrinfo returns an empty list"
            self.sock = None
            for res in socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    self.sock = socket.socket(af, socktype, proto)
                    self.sock.connect(sa)
                except socket.error, msg:
                    if self.sock:
                        self.sock.close()
                    self.sock = None
                    continue
                break
            if not self.sock:
                raise socket.error, msg
            self.file = self.sock.makefile('rb')
            self.sslobj = ssl.wrap_socket(self.sock, self.keyfile, self.certfile)
            self._debugging = 0
            self.welcome = self._getresp()

        def _fillBuffer(self):
            localbuf = self.sslobj.read()
            if len(localbuf) == 0:
                raise error_proto('-ERR EOF')
            self.buffer += localbuf

        def _getline(self):
            line = ""
            renewline = re.compile(r'.*?\n')
            match = renewline.match(self.buffer)
            while not match:
                self._fillBuffer()
                if len(self.buffer) > _MAXLINE:
                    raise error_proto('line too long')
                match = renewline.match(self.buffer)
            line = match.group(0)
            self.buffer = renewline.sub('' ,self.buffer, 1)
            if self._debugging > 1: print '*get*', repr(line)

            octets = len(line)
            if line[-2:] == CRLF:
                return line[:-2], octets
            if line[0] == CR:
                return line[1:-1], octets
            return line[:-1], octets

        def _putline(self, line):
            if self._debugging > 1: print '*put*', repr(line)
            line += CRLF
            bytes = len(line)
            while bytes > 0:
                sent = self.sslobj.write(line)
                if sent == bytes:
                    break    # avoid copy
                line = line[sent:]
                bytes = bytes - sent

        def quit(self):
            """Signoff: commit changes on server, unlock mailbox, close connection."""
            try:
                resp = self._shortcmd('QUIT')
            except error_proto, val:
                resp = val
            self.sock.close()
            del self.sslobj, self.sock
            return resp

    __all__.append("POP3_SSL")

