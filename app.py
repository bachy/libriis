#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys, os

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSlot, QSettings
from PyQt5.QtGui import QKeySequence, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QShortcut, QGridLayout, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSplitterHandle, QPlainTextEdit
# from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView, QWebInspector


from classes import server, compiler, view, content

class Core():
   def __init__(self, parent=None):
      self.server = server.Server()
      self.compiler = compiler.Compiler()
      self.settings = QSettings('FiguresLibres', 'Cascade')

class MainWindow(QMainWindow):
   def __init__(self, core):
      super(MainWindow, self).__init__()

      self.core = core

      self.restorePreferences()

      # self.setWindowFlags(QtCore.Qt.WindowTitleHint)
      # QtCore.Qt.CustomizeWindowHint
      # | QtCore.Qt.Tool
      #  | QtCore.Qt.FramelessWindowHint
      #  | QtCore.Qt.WindowTitleHint
      #  | QtCore.Qt.WindowStaysOnTopHint


      self.tabwidget = QTabWidget()
      # self.tabwidget.setContentsMargins(0,0,0,0)
      self.tabwidget.setStyleSheet("""
         QTabWidget::pane {
            border:0px solid inherted;
            margin:0px;
            padding:0px;
            }
         QTabBar::tab {
            padding: 4px;
            font-size:12px;
         }
         QTabBar::tab:selected {
            font-weight:bold;
         }
        """)

      self.viewtab = view.ViewTab(core)
      self.contenttab = content.ContentTab(core)
      self.versiontab = QLabel("Version (git).")


      self.tabwidget.addTab(self.viewtab, "View")
      self.tabwidget.addTab(self.contenttab, "Content")
      self.tabwidget.addTab(self.versiontab, "Version")

      self.setCentralWidget(self.tabwidget)

      self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
      self.shortcut.activated.connect(self.on_quit)


      self.show()

   def restorePreferences(self):
      try:
         self.resize(self.core.settings.value('mainwindow/size', QtCore.QSize(1024, 768)))
         self.move(self.core.settings.value('mainwindow/pos', QtCore.QPoint(0, 0)))
      except:
         pass

   def savePreferences(self):
      self.core.settings.beginGroup("mainwindow")
      self.core.settings.setValue('size', self.size())
      self.core.settings.setValue('pos', self.pos())
      self.core.settings.endGroup()

   @pyqtSlot()
   def on_quit(self):
     print("Quit!")
     self.savePreferences()
     QCoreApplication.instance().quit()


def main():
   app = QApplication(sys.argv)
   core = Core()
   mainappwindow = MainWindow(core)
   sys.exit(app.exec_())



if __name__ == "__main__":
   main()
