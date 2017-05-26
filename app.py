#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys, os, shutil

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSlot, QSettings
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QApplication, QShortcut, QGridLayout, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSplitterHandle, QPlainTextEdit, QInputDialog, QLineEdit, QFileDialog
# from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView, QWebInspector

import json
import git

from classes import server, compiler, view, content

class Core():
   def __init__(self, parent=None):
      self.server = server.Server()
      self.compiler = compiler.Compiler()
      self.settings = QSettings('FiguresLibres', 'Cascade')

class MainWindow(QMainWindow):
   def __init__(self, core):
      super(MainWindow, self).__init__()

      # load core class
      self.core = core
      # restore previous preferences
      self.restorePreferences()

      self.setWindowTitle("Cascade")
      self.setWindowIcon(QIcon('assets/images/icon.png'))

      self.initMenuBar()

      self.initTabs()
      # self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
      # self.shortcut.activated.connect(self.quit)


      self.show()

   def initMenuBar(self):
      # menu bar
      bar = self.menuBar()
      file = bar.addMenu("&File")

      new = QAction("&New Project",self)
      new.setShortcut("Ctrl+n")
      file.addAction(new)

      open = QAction("&Open",self)
      open.setShortcut("Ctrl+o")
      file.addAction(open)

      quit = QAction("&Quit",self)
      quit.setShortcut("Ctrl+q")
      file.addAction(quit)

      file.triggered[QAction].connect(self.processtrigger)

      edit = bar.addMenu("Edit")
      edit.addAction("copy")
      edit.addAction("paste")


   def processtrigger(self, q):
      print(q.text()+" is triggered")
      if q.text() == "&New Project":
         self.newprojectdialogue()
      elif q.text() == "&Open":
         self.opendialogue()
      elif q.text() == "&Quit":
         self.quit()

   def opendialogue(self):
      print("open")

   def newprojectdialogue(self):
      projectname = QFileDialog.getSaveFileName(self, 'Dialog Title', '')
      # TODO: no file type
      if not os.path.isdir(projectname[0]):
         self.core.cwd = projectname[0]
         self.initnewproject()
      else:
         print("folder already exists")
         # TODO: check if is cascade folder

   def initnewproject(self):
      shutil.copytree('templates/newproject', self.core.cwd)
      self.core.prefs = json.loads(open(os.path.join(self.core.cwd,'.config/prefs.json')).read())
      self.core.summary = json.loads(open(os.path.join(self.core.cwd,'.config/summary.json')).read())
      # TODO: init git repos
      self.core.repository = git.Repo.init(self.core.cwd)
      self.core.repository.index.add(['assets','contents','.config'])
      self.core.repository.index.commit("initial commit")
      # TODO: set mdtohtml compiler from project md to app index.html
      # TODO: embed project styles.scss to app scss frame work

   def quit(self):
     print("Quit")
     self.savePreferences()
     QCoreApplication.instance().quit()

   def initTabs(self):
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
      self.core.settings.setValue('cwd', self.core.cwd)
      self.core.settings.endGroup()


def main():
   app = QApplication(sys.argv)
   core = Core()
   mainappwindow = MainWindow(core)
   sys.exit(app.exec_())



if __name__ == "__main__":
   main()
