#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, re
# sys,
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSettings, QSizeF
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPlainTextEdit, QShortcut, QPushButton, QCheckBox
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter


class WebkitView(QWebView):
   def __init__(self, parent, core):
      self.parent = parent
      self.core = core
      self.port = core.server.port
      self.view = QWebView.__init__(self, parent)
      self.setZoomFactor(1)
      self.load(QUrl('http://localhost:'+str(self.port)))
      self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
      # self.settings().setAttribute(QWebSettings.PluginsEnabled, True)

      self.initPDF()
      # self.mainframe = self.page.mainFrame()
      # print(self.mainframe)

   def initPDF(self):
      self.printer = QPrinter(QPrinter.HighResolution)
      self.printer.setFullPage(True)
      # self.printer.setPageMargins(0,0,0,0,QPrinter.Millimeter)
      self.printer.setFontEmbeddingEnabled(True)
      self.printer.setColorMode(QPrinter.Color)
      # TODO: set the page size and orientation from doc settings
      # (need to do doc settings before that)
      # self.printer.setPageSize(QPrinter.A4)
      self.printer.setPaperSize(QSizeF(210, 300), QPrinter.Millimeter)
      # self.printer.setOrientation(QPrinter.Portrait)
      self.printer.setOutputFormat(QPrinter.PdfFormat)
      self.printer.setCreator('Cascade')
      self.printer.setDocName(self.core.projectname)
      self.printer.setOutputFileName(self.core.projectname+".pdf")
      # self.setFixedWidth(1000)


   def ongenPDF(self):
      # QPrinter::Custom
      # dialog = QPrintPreviewDialog(self.printer)
      # dialog.setWindowState(Qt.WindowMaximized)
      # dialog.paintRequested.connect(self.print_)
      # dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
      # dialog.exec()
      # TODO: open a dialogue to ask where to save the pdf
      # TODO: reload webview and wait for it before printing
      # TODO: addd a progress bar
      # self.webview.
      self.print_(self.printer)

   def refresh(self):
      self.initPDF()
      self.reload()

class WebkitInspector(QWebInspector):
   def __init__(self, parent, webkitview):
      super(WebkitInspector, self).__init__(parent)
      self.webkitview = webkitview
      self.setPage(self.webkitview.page())
      self.showMaximized()
      # TODO: webkitinspector is disappearing when chaging tabs

class WebViewToolBar(QWidget):
   def __init__(self, parent):
      super(WebViewToolBar, self).__init__(parent)
      self.parent = parent
      self.hbox = QHBoxLayout()
      self.hbox.setContentsMargins(0,0,0,0)

      self.preview = QCheckBox('&Preview', self)
      # self.preview.setShortcut('Ctrl+Shift+p')
      self.preview.clicked.connect(self.onPreview)
      self.hbox.addWidget(self.preview)

      self.debug = QCheckBox('Deb&ug', self)
      # self.debug.setShortcut('Ctrl+Shift+u')
      self.debug.clicked.connect(self.onDebug)
      self.hbox.addWidget(self.debug)

      self.grid = QCheckBox('&Grid', self)
      # self.grid.setShortcut('Ctrl+Shift+g')
      self.grid.clicked.connect(self.onGrid)
      self.hbox.addWidget(self.grid)

      # spread
      self.spread = QCheckBox('&Spread', self)
      # self.spread.setShortcut('Ctrl+Shift+g')
      self.spread.clicked.connect(self.onSpread)
      self.hbox.addWidget(self.spread)

      self.hbox.addStretch()

      # zoom
      # page

      self.hbox.addStretch()



      self.reload = QPushButton("&Reload", self)
      # self.reload.setShortcut('Ctrl+Shift+r')
      # TODO: how to define same shortcut in different places
      # self.reload.setIcon(Icon(ico)))
      self.reload.clicked.connect(self.onReload)
      self.hbox.addWidget(self.reload)

      self.imprim = QPushButton("&Print", self)
      # self.imprim.setShortcut('Ctrl+Shift+r')
      # TODO: how to define same shortcut in different places
      # self.imprim.setIcon(Icon(ico)))
      self.imprim.clicked.connect(self.onPrint)
      self.hbox.addWidget(self.imprim)

      self.setLayout(self.hbox)

   def onPreview(self):
      print('onPreview')

   def onDebug(self):
      print('onDebug')

   def onGrid(self):
      print('onGrid')

   def onSpread(self):
      print('onSpread')


   def onReload(self):
      print("onReload")
      # self.parent.webkitview.

   def onPrint(self):
      print("onReload")
      self.parent.webkitview.onPrint()


class CodeEditor(QPlainTextEdit):
   def __init__(self, core, tabs, file=None):
      super(CodeEditor, self).__init__()
      self.core = core
      self.tabs = tabs
      self.file = file
      self.setText()

      self.shortcut = QShortcut(QKeySequence("Ctrl+s"), self)
      self.shortcut.activated.connect(self.save)

   def setText(self):
      try:
         self.textChanged.disconnect(self.onTextChanged)
      except Exception as e:
         print(e)

      self.filepath = os.path.join(self.core.cwd,self.file)
      self.clear()
      self.insertPlainText(open(self.filepath, 'r').read())
      self.changed = False
      self.textChanged.connect(self.onTextChanged)


   def onTextChanged(self):
      # print('textChanged')
      # print(self.toPlainText())
      # open(self.filepath, 'w').write(self.toPlainText())
      if not self.changed:
         self.changed = True
         i = self.tabs.currentIndex()
         self.tabs.setTabText(i, "* "+self.tabs.tabText(i))
         # TODO: indicate that webview needs to be reloaded

   def save(self):
      if self.changed:
         open(self.filepath, 'w').write(self.toPlainText())
         i = self.tabs.currentIndex()
         self.tabs.setTabText(i, re.sub(r'^\*\s', '', self.tabs.tabText(i)))
         self.changed = False
         # TODO: how to combine file save and project save


class Editor(QWidget):
   def __init__(self, parent, core):
      super(Editor, self).__init__()
      self.core = core

      self.layout = QVBoxLayout(self)
      self.layout.setContentsMargins(0,0,0,0)

      # Initialize tab screen
      self.tabs = QTabWidget()

      self.scsstab = CodeEditor(core, self.tabs, 'assets/css/styles.scss')
      self.jstab = CodeEditor(core, self.tabs, 'assets/js/script.js')

      # Add tabs
      self.tabs.addTab(self.scsstab,"scss")
      self.tabs.addTab(self.jstab,"js")

      # Add tabs to widget
      self.layout.addWidget(self.tabs)
      self.setLayout(self.layout)

      # font = QFont()
      # font.setFamily('Courier')
      # font.setFixedPitch(True)
      # font.setPointSize(10)
      # self.setFont(font)
      # self.highlighter = Highlighter(self.document())
      # https://pypi.python.org/pypi/QScintilla/2.9.2

   def refresh(self):
      self.scsstab.setText()
      self.jstab.setText()

class DesignStack(QWidget):
   def __init__(self, core):
      super(DesignStack, self).__init__()

      # self.grid = QGridLayout()
      self.hbox = QHBoxLayout()
      self.hbox.setContentsMargins(0,0,0,0)
      self.setLayout(self.hbox)


      self.webview = QWidget()
      self.webview.vbox = QVBoxLayout()
      self.webview.setLayout(self.webview.vbox)
      self.webview.vbox.setContentsMargins(0,0,0,0)

      self.webkitview = WebkitView(self, core)

      self.webkitinspector = WebkitInspector(self, self.webkitview)

      shortcut = QShortcut(self)
      shortcut.setKey("F12")
      shortcut.activated.connect(self.toggleInspector)
      self.webkitinspector.setVisible(False)

      self.webviewtoolbar = WebViewToolBar(self)
      self.webview.vbox.addWidget(self.webviewtoolbar)

      self.vsplitter = QSplitter(QtCore.Qt.Vertical)
      self.vsplitter.addWidget(self.webkitview)
      self.vsplitter.addWidget(self.webkitinspector)
      self.vsplitter.splitterMoved.connect(self.movedSplitter)

      self.webview.vbox.addWidget(self.vsplitter)

      self.hsplitter = QSplitter(QtCore.Qt.Horizontal)
      self.hsplitter.addWidget(self.webview)

      self.editor = Editor(self, core)
      self.hsplitter.addWidget(self.editor)

      self.hsplitter.splitterMoved.connect(self.movedSplitter)

      self.hbox.addWidget(self.hsplitter)

      self.restorePrefs()

   def toggleInspector(self):
      self.webkitinspector.setVisible(not self.webkitinspector.isVisible())


   def restorePrefs(self):
      settings = QSettings('FiguresLibres', 'Cascade')
      print(settings.value('design/vsplitter/sizes', self.vsplitter.sizes()))
      vals = settings.value('design/vsplitter/sizes', None)
      if vals:
         sizes = []
         for size in vals: sizes.append(int(size))
         self.vsplitter.setSizes(sizes)

      vals = settings.value('design/hsplitter/sizes', None)
      if vals:
         sizes = []
         for size in vals: sizes.append(int(size))
         self.hsplitter.setSizes(sizes)


   def movedSplitter(self):
      settings = QSettings('FiguresLibres', 'Cascade')
      # print(self.vsplitter.sizes())
      settings.setValue('design/vsplitter/sizes', self.vsplitter.sizes())
      settings.setValue('design/hsplitter/sizes', self.hsplitter.sizes())

   def refresh(self):
      self.editor.refresh()
      self.webkitview.refresh()
