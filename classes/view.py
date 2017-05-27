#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPlainTextEdit
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector


class WebkitView(QWebView):
   def __init__(self, port):
      self.port = port
      self.view = QWebView.__init__(self)
      self.load(QUrl('http://localhost:'+str(self.port)))
      self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
      # self.settings().setAttribute(QWebSettings.PluginsEnabled, True)


class WebkitInspector(QWebInspector):
   def __init__(self, webkitview):
      super(WebkitInspector, self).__init__()
      self.webkitview = webkitview
      self.setPage(self.webkitview.page())
      # TODO: webkitinspector is disappearing when chaging tabs

class CodeEditor(QWidget):
   def __init__(self, core):
      super(CodeEditor, self).__init__()
      self.core = core

      self.layout = QVBoxLayout(self)
      self.layout.setContentsMargins(0,0,0,0)

      # Initialize tab screen
      self.tabs = QTabWidget()

      self.scsstab = QPlainTextEdit()
      self.scssfile = open(os.path.join(self.core.cwd,'assets/scss/styles.scss'))
      scssstr = self.scssfile.read()
      self.scsstab.insertPlainText(scssstr)

      self.jstab = QPlainTextEdit()
      self.jsfile = open(os.path.join(self.core.cwd,'assets/js/script.js'))
      jsstr = self.jsfile.read()
      self.jstab.insertPlainText(jsstr)


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


class ViewStack(QWidget):
   def __init__(self, core):
      super(ViewStack, self).__init__()

      # self.grid = QGridLayout()
      hbox = QHBoxLayout()
      hbox.setContentsMargins(0,0,0,0)
      self.setLayout(hbox)


      # webviewbox = QVBoxLayout()
      vsplitter = QSplitter(QtCore.Qt.Vertical)

      self.webkitview = WebkitView(core.server.port)
      vsplitter.addWidget(self.webkitview)

      self.webkitinspector = WebkitInspector(self.webkitview)
      vsplitter.addWidget(self.webkitinspector)

      hsplitter = QSplitter(QtCore.Qt.Horizontal)
      hsplitter.addWidget(vsplitter)

      self.codeeditor = CodeEditor(core)
      hsplitter.addWidget(self.codeeditor)

      hbox.addWidget(hsplitter)


   # def onChanged(self, text):
   #    print("ViewTba Layout Changed")
   #    self.lbl.setText(text)
   #    self.lbl.adjustSize()
