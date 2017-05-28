#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, re

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QKeySequence, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPlainTextEdit, QShortcut
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
      # TODO: webkitinspector is disappearing when chaging tabs

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

      self.scsstab = CodeEditor(core, self.tabs, 'assets/scss/styles.scss')
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
      hbox = QHBoxLayout()
      hbox.setContentsMargins(0,0,0,0)
      self.setLayout(hbox)


      # webviewbox = QVBoxLayout()
      vsplitter = QSplitter(QtCore.Qt.Vertical)

      self.webkitview = WebkitView(self, core.server.port)
      vsplitter.addWidget(self.webkitview)

      self.webkitinspector = WebkitInspector(self, self.webkitview)
      vsplitter.addWidget(self.webkitinspector)

      shortcut = QShortcut(self)
      shortcut.setKey("F12")
      shortcut.activated.connect(self.toggleInspector)
      self.webkitinspector.setVisible(False)


      hsplitter = QSplitter(QtCore.Qt.Horizontal)
      hsplitter.addWidget(vsplitter)

      self.editor = Editor(self, core)
      hsplitter.addWidget(self.editor)

      hbox.addWidget(hsplitter)

   def toggleInspector(self):
      self.webkitinspector.setVisible(not self.webkitinspector.isVisible())
      
