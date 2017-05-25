#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QHBoxLayout, QSplitter, QPlainTextEdit


class Summary(QLabel):
   def __init__(self):
      super(Summary, self).__init__()



class ContentTab(QWidget):
   def __init__(self, core):
      super(ContentTab, self).__init__()

      # self.grid = QGridLayout()
      hbox = QHBoxLayout()
      hbox.setContentsMargins(0,0,0,0)
      self.setLayout(hbox)

      hsplitter = QSplitter(QtCore.Qt.Horizontal)

      self.summary = QLabel("Summary (markdown files list).")
      hsplitter.addWidget(self.summary)

      self.mdsource = QLabel("Content (markdown src).")
      hsplitter.addWidget(self.mdsource)

      self.mdpreview = QLabel("Content (markdown preview).")
      hsplitter.addWidget(self.mdpreview)

      hbox.addWidget(hsplitter)
