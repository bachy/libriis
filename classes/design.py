#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, re

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSettings
from PyQt5.QtGui import QKeySequence, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPlainTextEdit, QShortcut, QPushButton, QCheckBox
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector


class WebkitView(QWebView):
   def __init__(self, parent, port):
      self.port = port
      self.view = QWebView.__init__(self, parent)
      self.load(QUrl('http://localhost:'+str(self.port)))
      self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
      # self.settings().setAttribute(QWebSettings.PluginsEnabled, True)


class WebkitInspector(QWebInspector):
   def __init__(self, parent, webkitview):
      super(WebkitInspector, self).__init__(parent)
      self.webkitview = webkitview
      self.setPage(self.webkitview.page())
      self.showMaximized()
      # TODO: webkitinspector is disappearing when chaging tabs

class WebViewOptions(QWidget):
   def __init__(self, parent):
      super(WebViewOptions, self).__init__(parent)
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

      self.setLayout(self.hbox)

   def onReload(self):
      print("onReload")

   def onPreview(self):
      print('onPreview')

   def onDebug(self):
      print('onDebug')

   def onGrid(self):
      print('onGrid')

   def onSpread(self):
      print('onSpread')

class CodeEditor(QPlainTextEdit):
   def __init__(self, core, tabs, file=None):
      super(CodeEditor, self).__init__()
      self.core = core
      self.tabs = tabs
      # self.file = file
      self.file = os.path.join(self.core.cwd,file)

      self.insertPlainText(open(self.file, 'r').read())
      self.changed = False
      self.textChanged.connect(self.onTextChanged)

      self.shortcut = QShortcut(QKeySequence("Ctrl+s"), self)
      self.shortcut.activated.connect(self.save)

   def onTextChanged(self):
      # print('textChanged')
      # print(self.toPlainText())
      # open(self.file, 'w').write(self.toPlainText())
      if not self.changed:
         self.changed = True
         i = self.tabs.currentIndex()
         self.tabs.setTabText(i, "* "+self.tabs.tabText(i))

   def save(self):
      if self.changed:
         open(self.file, 'w').write(self.toPlainText())
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


      self.webkitview = WebkitView(self, core.server.port)

      self.webkitinspector = WebkitInspector(self, self.webkitview)

      shortcut = QShortcut(self)
      shortcut.setKey("F12")
      shortcut.activated.connect(self.toggleInspector)
      self.webkitinspector.setVisible(False)

      self.webviewoptions = WebViewOptions(self)
      self.webview.vbox.addWidget(self.webviewoptions)

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
