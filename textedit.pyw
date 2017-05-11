# -*- coding: utf-8 -*-
import os
import sys

from PyQt4.QtGui import QPushButton
import time

from timerWindow import *
from PyQt4.QtGui import QFileDialog

reload(sys)
sys.setdefaultencoding( "utf-8" )

from Info import *
from PyQt4 import QtCore, QtGui

try:
    import textedit_rc3
except ImportError:
    import textedit_rc2


if sys.platform.startswith('darwin'):
    rsrcPath = ":/images/mac"
else:
    rsrcPath = ":/images/win"


class TextEdit(QtGui.QMainWindow):
    def __init__(self, fileName=None, parent=None):
        super(TextEdit, self).__init__(parent)

        self.setWindowIcon(QtGui.QIcon('mail.png'))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)

        palette1 = QtGui.QPalette(self)
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('bk1.png')))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)

        #self.setupFileActions()
        self.setupEditActions()
        self.setupTextActions()

        helpMenu = QtGui.QMenu("Help", self)
        #self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("About", self.about)
        helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)

        self.sendBtn = QtGui.QPushButton(u'发送')
        self.appendix = QtGui.QPushButton(u'添加附件')
        self.draftBtn = QtGui.QPushButton(u'保存草稿')
        self.sendBtn.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.appendix.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 3px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.draftBtn.setStyleSheet("QPushButton{background-color:#6495ED;width:60px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#F0FFFF;}")
        self.sendBtn.clicked.connect(self.sendmail)
        self.appendix.clicked.connect(self.attachment)
        self.draftBtn.clicked.connect(self.draftSave)
        self.hbox3 = QtGui.QHBoxLayout()
        self.hbox3.addStretch(1)
        self.hbox3.addWidget(self.sendBtn)
        self.hbox3.addWidget(self.draftBtn)
        self.hbox4 = QtGui.QHBoxLayout()
        self.hbox4.addWidget(self.appendix)
        self.hbox4.addStretch(1)
        #self.hbox3.addWidget(self.appendix)
        self.textEdit = QtGui.QTextEdit(self)
        self.vbox = QtGui.QVBoxLayout()
        self.toaddr = QtGui.QLabel(u"收件人：")
        self.toedit = QtGui.QLineEdit()
        if getReply():
            self.toedit.setText(getToaddr())
        self.subject = QtGui.QLabel(u"主  题：")
        self.subedit = QtGui.QLineEdit()
        if getTrans():
            self.subedit.setText(getReplySub())
            #self.textEdit.setText(getContent())
            self.textEdit.setHtml(getHtml())
            print getHtml()
        print
        if getDraft():
            setDraft(0)
            self.toedit.setText(getToaddr())
            self.subedit.setText(getReplySub())
            self.textEdit.setHtml(getHtml())

        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox1.addWidget(self.toaddr)
        self.hbox1.addWidget(self.toedit)
        self.hbox2.addWidget(self.subject)
        self.hbox2.addWidget(self.subedit)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox4)
        self.vbox.addWidget(self.textEdit)
        self.vbox.addLayout(self.hbox3)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vbox)
        self.setCentralWidget(self.widget)

        self.textEdit.currentCharFormatChanged.connect(
                self.currentCharFormatChanged)
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)

        #self.setCentralWidget(self.textEdit)

        self.textEdit.setFocus()
        self.setCurrentFileName()
        self.fontChanged(self.textEdit.font())
        self.colorChanged(self.textEdit.textColor())
        self.alignmentChanged(self.textEdit.alignment())
        # self.textEdit.document().modificationChanged.connect(
        #         self.actionSave.setEnabled)
        self.textEdit.document().modificationChanged.connect(
                self.setWindowModified)
        self.textEdit.document().undoAvailable.connect(
                self.actionUndo.setEnabled)
        self.textEdit.document().redoAvailable.connect(
                self.actionRedo.setEnabled)
        self.setWindowModified(self.textEdit.document().isModified())
        #self.actionSave.setEnabled(self.textEdit.document().isModified())
        self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        QtGui.QApplication.clipboard().dataChanged.connect(
                self.clipboardDataChanged)



        # if fileName is None:
        #     fileName = ':/example.html'
        #
        # if not self.load(fileName):
        #     self.fileNew()


    def sendmail(self):
        toaddr = str(self.toedit.text())
        setToaddr(toaddr)
        list1 = toaddr.split(';')
        list1 = list((list1))
        setList(list1)
        sub = self.subedit.text()
        setSub(sub)
        #context = self.textEdit.toPlainText()
        content = self.textEdit.toHtml()
        setContent(content)
        timerWin()
        from sendThreads import sendThread
        # 新建对象
        self.sThread = sendThread()
        # 开始执行run()函数里的内容
        self.sThread.start()



    def attachment(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file', 'D:/')
        str1 = ''
        for name in fname:
            name = unicode(name,'utf-8')
            str1 = str1 + name + ';'
            self.addAppendix(name)
        setAppendix(str1)
        #self.hbox4.addStretch(1)

    def addAppendix(self,btnname):
        widget = QPushButton(unicode(str(btnname.split('\\')[-1]),'utf-8'), self)
        #widget.setVisible()
        menu = QtGui.QMenu()
        menu.addAction(u'删除 ', lambda: self.delAppendix(widget,btnname))
        widget.setMenu(menu)
        widget.setStyleSheet("QPushButton{background-color:	#F8F8FF;width:100px;height:20px; "
                                      "border-radius: 5px;margin-right:5px;margin-bottom: 5px}""QPushButton:hover{background-color:#B0C4DE;}")
        self.hbox4.addWidget(widget)
        #widget.clicked.connect(lambda: self.delAppendix(btnname))

    def delAppendix(self,widget,btnname):
        #print 'aaa'
        #print getAppendix()
        strAppendix = getAppendix()
        strAppendix.replace(btnname+';', '')
        #print  self.sender().text()
        self.hbox4.addStretch(1)
        self.hbox4.removeWidget(widget.setVisible(False))
        self.hbox4.addStretch(1)
        #print 'bbbb'
        #print getAppendix()

    def draftSave(self):
        try:
            os.makedirs(getName() + '/draftmail/info')
        except:
            pass
        try:
            lenth = sum([len(files) for root, dirs, files in os.walk(getName() + '/draftmail/info/')])
            with codecs.open(getName() + '/draftmail/' + str(lenth + 1) + '.html', 'w', 'gbk') as fp:
                fp.write(self.textEdit.toHtml())
            with codecs.open(getName() + '/draftmail/info/' + str(lenth + 1) + '.txt', 'a', 'gbk') as fp:
                #fp.write('From:' + getName() + '\r\n')
                fp.write('To:' + str(self.toedit.text()) + '\r\n')
                fp.write('Subject:' + self.subedit.text() + '\r\n')
                ISOTIMEFORMAT = '%Y-%m-%d %X'
                fp.write('Date:' + time.strftime(ISOTIMEFORMAT, time.localtime()) + '\r\n')
            timerWin5()
        except:
            timerWin6()


    def closeEvent(self, e):
        # if self.maybeSave():
        #     e.accept()
        # else:
        #     e.ignore()
        pass

    def sendActions(self):
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("File Actions")
        self.addToolBar(tb)

    def setupFileActions(self):
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("File Actions")
        self.addToolBar(tb)

        menu = QtGui.QMenu("&File", self)
        #self.menuBar().addMenu(menu)

        self.actionNew = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-new',
                        QtGui.QIcon(rsrcPath + '/filenew.png')),
                "&New", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.New, triggered=self.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-open',
                        QtGui.QIcon(rsrcPath + '/fileopen.png')),
                "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                triggered=self.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-save',
                        QtGui.QIcon(rsrcPath + '/filesave.png')),
                "&Save", self, shortcut=QtGui.QKeySequence.Save,
                triggered=self.fileSave, enabled=False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QtGui.QAction("Save &As...", self,
                priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_S,
                triggered=self.fileSaveAs)
        menu.addAction(self.actionSaveAs)
        menu.addSeparator()
 
        self.actionPrint = QtGui.QAction(
                QtGui.QIcon.fromTheme('document-print',
                        QtGui.QIcon(rsrcPath + '/fileprint.png')),
                "&Print...", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Print, triggered=self.filePrint)
        tb.addAction(self.actionPrint)
        menu.addAction(self.actionPrint)

        self.actionPrintPreview = QtGui.QAction(
                QtGui.QIcon.fromTheme('fileprint',
                        QtGui.QIcon(rsrcPath + '/fileprint.png')),
                "Print Preview...", self,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_P,
                triggered=self.filePrintPreview)
        menu.addAction(self.actionPrintPreview)

        self.actionPrintPdf = QtGui.QAction(
                QtGui.QIcon.fromTheme('exportpdf',
                        QtGui.QIcon(rsrcPath + '/exportpdf.png')),
                "&Export PDF...", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_D,
                triggered=self.filePrintPdf)
        tb.addAction(self.actionPrintPdf)
        menu.addAction(self.actionPrintPdf)
        menu.addSeparator()

        self.actionQuit = QtGui.QAction("&Quit", self,
                shortcut=QtGui.QKeySequence.Quit, triggered=self.close)
        menu.addAction(self.actionQuit)

    def setupEditActions(self):
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Edit Actions")
        self.addToolBar(tb)

        menu = QtGui.QMenu("&Edit", self)
        #self.menuBar().addMenu(menu)

        self.actionUndo = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-undo',
                        QtGui.QIcon(rsrcPath + '/editundo.png')),
                "&Undo", self, shortcut=QtGui.QKeySequence.Undo)
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)

        self.actionRedo = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-redo',
                        QtGui.QIcon(rsrcPath + '/editredo.png')),
                "&Redo", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Redo)
        tb.addAction(self.actionRedo)
        menu.addAction(self.actionRedo)
        menu.addSeparator()

        self.actionCut = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-cut',
                        QtGui.QIcon(rsrcPath + '/editcut.png')),
                "Cu&t", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Cut)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)

        self.actionCopy = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-copy',
                        QtGui.QIcon(rsrcPath + '/editcopy.png')),
                "&Copy", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Copy)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)

        self.actionPaste = QtGui.QAction(
                QtGui.QIcon.fromTheme('edit-paste',
                        QtGui.QIcon(rsrcPath + '/editpaste.png')),
                "&Paste", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtGui.QKeySequence.Paste,
                enabled=(len(QtGui.QApplication.clipboard().text()) != 0))
        tb.addAction(self.actionPaste)
        menu.addAction(self.actionPaste)

    def setupTextActions(self):
        tb = QtGui.QToolBar(self)
        tb.setWindowTitle("Format Actions")
        self.addToolBar(tb)

        menu = QtGui.QMenu("F&ormat", self)
        #self.menuBar().addMenu(menu)

        self.actionTextBold = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-text-bold',
                        QtGui.QIcon(rsrcPath + '/textbold.png')),
                "&Bold", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_B,
                triggered=self.textBold, checkable=True)
        bold = QtGui.QFont()
        bold.setBold(True)
        self.actionTextBold.setFont(bold)
        tb.addAction(self.actionTextBold)
        menu.addAction(self.actionTextBold)

        self.actionTextItalic = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-text-italic',
                        QtGui.QIcon(rsrcPath + '/textitalic.png')),
                "&Italic", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_I,
                triggered=self.textItalic, checkable=True)
        italic = QtGui.QFont()
        italic.setItalic(True)
        self.actionTextItalic.setFont(italic)
        tb.addAction(self.actionTextItalic)
        menu.addAction(self.actionTextItalic)

        self.actionTextUnderline = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-text-underline',
                        QtGui.QIcon(rsrcPath + '/textunder.png')),
                "&Underline", self, priority=QtGui.QAction.LowPriority,
                shortcut=QtCore.Qt.CTRL + QtCore.Qt.Key_U,
                triggered=self.textUnderline, checkable=True)
        underline = QtGui.QFont()
        underline.setUnderline(True)
        self.actionTextUnderline.setFont(underline)
        tb.addAction(self.actionTextUnderline)
        menu.addAction(self.actionTextUnderline)

        menu.addSeparator()

        grp = QtGui.QActionGroup(self, triggered=self.textAlign)

        # Make sure the alignLeft is always left of the alignRight.
        if QtGui.QApplication.isLeftToRight():
            self.actionAlignLeft = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-left',
                            QtGui.QIcon(rsrcPath + '/textleft.png')),
                    "&Left", grp)
            self.actionAlignCenter = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-center',
                            QtGui.QIcon(rsrcPath + '/textcenter.png')),
                    "C&enter", grp)
            self.actionAlignRight = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-right',
                            QtGui.QIcon(rsrcPath + '/textright.png')),
                    "&Right", grp)
        else:
            self.actionAlignRight = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-right',
                            QtGui.QIcon(rsrcPath + '/textright.png')),
                    "&Right", grp)
            self.actionAlignCenter = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-center',
                            QtGui.QIcon(rsrcPath + '/textcenter.png')),
                    "C&enter", grp)
            self.actionAlignLeft = QtGui.QAction(
                    QtGui.QIcon.fromTheme('format-justify-left',
                            QtGui.QIcon(rsrcPath + '/textleft.png')),
                    "&Left", grp)
 
        self.actionAlignJustify = QtGui.QAction(
                QtGui.QIcon.fromTheme('format-justify-fill',
                        QtGui.QIcon(rsrcPath + '/textjustify.png')),
                "&Justify", grp)

        self.actionAlignLeft.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QtGui.QAction.LowPriority)

        self.actionAlignCenter.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QtGui.QAction.LowPriority)

        self.actionAlignRight.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QtGui.QAction.LowPriority)

        self.actionAlignJustify.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_J)
        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QtGui.QAction.LowPriority)

        tb.addActions(grp.actions())
        menu.addActions(grp.actions())
        menu.addSeparator()

        pix = QtGui.QPixmap(16, 16)
        pix.fill(QtCore.Qt.black)
        self.actionTextColor = QtGui.QAction(QtGui.QIcon(pix), "&Color...",
                self, triggered=self.textColor)
        tb.addAction(self.actionTextColor)
        menu.addAction(self.actionTextColor)

        tb = QtGui.QToolBar(self)
        tb.setAllowedAreas(
                QtCore.Qt.TopToolBarArea | QtCore.Qt.BottomToolBarArea)
        tb.setWindowTitle("Format Actions")
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self.addToolBar(tb)

        comboStyle = QtGui.QComboBox(tb)
        tb.addWidget(comboStyle)
        comboStyle.addItem("Standard")
        comboStyle.addItem("Bullet List (Disc)")
        comboStyle.addItem("Bullet List (Circle)")
        comboStyle.addItem("Bullet List (Square)")
        comboStyle.addItem("Ordered List (Decimal)")
        comboStyle.addItem("Ordered List (Alpha lower)")
        comboStyle.addItem("Ordered List (Alpha upper)")
        comboStyle.addItem("Ordered List (Roman lower)")
        comboStyle.addItem("Ordered List (Roman upper)")
        comboStyle.activated.connect(self.textStyle)

        self.comboFont = QtGui.QFontComboBox(tb)
        tb.addWidget(self.comboFont)
        self.comboFont.activated[str].connect(self.textFamily)

        self.comboSize = QtGui.QComboBox(tb)
        self.comboSize.setObjectName("comboSize")
        tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QtGui.QFontDatabase()
        for size in db.standardSizes():
            self.comboSize.addItem("%s" % (size))

        self.comboSize.activated[str].connect(self.textSize)
        self.comboSize.setCurrentIndex(
                self.comboSize.findText(
                        "%s" % (QtGui.QApplication.font().pointSize())))

    def load(self, f):
        if not QtCore.QFile.exists(f):
            return False

        fh = QtCore.QFile(f)
        if not fh.open(QtCore.QFile.ReadOnly):
            return False

        data = fh.readAll()
        codec = QtCore.QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)

        if QtCore.Qt.mightBeRichText(unistr):
            self.textEdit.setHtml(unistr)
        else:
            self.textEdit.setPlainText(unistr)

        self.setCurrentFileName(f)
        return True

    def maybeSave(self):
        if not self.textEdit.document().isModified():
            return True

        if self.fileName.startswith(':/'):
            return True

        ret = QtGui.QMessageBox.warning(self, "Application",
                "The document has been modified.\n"
                "Do you want to save your changes?",
                QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                        QtGui.QMessageBox.Cancel)

        if ret == QtGui.QMessageBox.Save:
            return self.fileSave()

        if ret == QtGui.QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        self.fileName = fileName
        self.textEdit.document().setModified(False)

        if not fileName:
            shownName = 'untitled.txt'
        else:
            shownName = QtCore.QFileInfo(fileName).fileName()

        #self.setWindowTitle(self.tr("%s[*] - %s" % (shownName, self.tr("Send Mail"))))
        self.setWindowTitle(u"发邮件")
        self.setWindowModified(False)

    def fileNew(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFileName()

    def fileOpen(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, "Open File...", None,
                "HTML-Files (*.htm *.html);;All Files (*)")

        if fn:
            self.load(fn)

    def fileSave(self):
        if not self.fileName:
            return self.fileSaveAs()

        writer = QtGui.QTextDocumentWriter(self.fileName)
        success = writer.write(self.textEdit.document())
        if success:
            self.textEdit.document().setModified(False)

        return success

    def fileSaveAs(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, "Save as...", None,
                "ODF files (*.odt);;HTML-Files (*.htm *.html);;All Files (*)")

        if not fn:
            return False

        lfn = fn.lower()
        if not lfn.endswith(('.odt', '.htm', '.html')):
            # The default.
            fn += '.odt'

        self.setCurrentFileName(fn)
        return self.fileSave()

    def filePrint(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)

        if self.textEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QtGui.QAbstractPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QtGui.QDialog.Accepted:
            self.textEdit.print_(printer)

        del dlg

    def filePrintPreview(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        preview = QtGui.QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)

    def filePrintPdf(self):
        fn = QtGui.QFileDialog.getSaveFileName(self, "Export PDF", None,
                "PDF files (*.pdf);;All Files (*)")

        if fn:
            if QtCore.QFileInfo(fn).suffix().isEmpty():
                fn += '.pdf'

            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def textBold(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontWeight(self.actionTextBold.isChecked() and QtGui.QFont.Bold or QtGui.QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textFamily(self, family):
        fmt = QtGui.QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QtGui.QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

    def textStyle(self, styleIndex):
        cursor = self.textEdit.textCursor()
        if styleIndex:
            styleDict = {
                1: QtGui.QTextListFormat.ListDisc,
                2: QtGui.QTextListFormat.ListCircle,
                3: QtGui.QTextListFormat.ListSquare,
                4: QtGui.QTextListFormat.ListDecimal,
                5: QtGui.QTextListFormat.ListLowerAlpha,
                6: QtGui.QTextListFormat.ListUpperAlpha,
                7: QtGui.QTextListFormat.ListLowerRoman,
                8: QtGui.QTextListFormat.ListUpperRoman,
            }

            style = styleDict.get(styleIndex, QtGui.QTextListFormat.ListDisc)
            cursor.beginEditBlock()
            blockFmt = cursor.blockFormat()
            listFmt = QtGui.QTextListFormat()

            if cursor.currentList():
                listFmt = cursor.currentList().format()
            else:
                listFmt.setIndent(blockFmt.indent() + 1)
                blockFmt.setIndent(0)
                cursor.setBlockFormat(blockFmt)

            listFmt.setStyle(style)
            cursor.createList(listFmt)
            cursor.endEditBlock()
        else:
            bfmt = QtGui.QTextBlockFormat()
            bfmt.setObjectIndex(-1)
            cursor.mergeBlockFormat(bfmt)

    def textColor(self):
        col = QtGui.QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        if action == self.actionAlignLeft:
            self.textEdit.setAlignment(
                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.textEdit.setAlignment(QtCore.Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.textEdit.setAlignment(
                    QtCore.Qt.AlignRight | QtCore.Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.textEdit.setAlignment(QtCore.Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(
                len(QtGui.QApplication.clipboard().text()) != 0)

    def about(self):
        QtGui.QMessageBox.about(self, "About", 
                "This example demonstrates Qt's rich text editing facilities "
                "in action, providing an example document for you to "
                "experiment with.")

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        self.comboFont.setCurrentIndex(
                self.comboFont.findText(QtGui.QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(
                self.comboSize.findText("%s" % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QtGui.QPixmap(16, 16)
        pix.fill(color)
        self.actionTextColor.setIcon(QtGui.QIcon(pix))

    def alignmentChanged(self, alignment):
        if alignment & QtCore.Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif alignment & QtCore.Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif alignment & QtCore.Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif alignment & QtCore.Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    textEdit = TextEdit()
    textEdit.resize(1068, 608)
    textEdit.show()
    app.exec_()

    # mainWindows = []
    # for fn in sys.argv[1:] or [None]:
    #     textEdit = TextEdit(fn)
    #     textEdit.resize(1068, 608)
    #     textEdit.show()
    #     mainWindows.append(textEdit)

    #sys.exit(app.exec_())
