#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys, os, shutil, tempfile

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QUrl, pyqtSlot, QSettings
from PyQt5.QtGui import QIcon, QKeySequence, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QApplication, QShortcut, QGridLayout, QLabel, QTabWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSplitterHandle, QPlainTextEdit, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton
# from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView, QWebInspector

import json
import git

from classes import server, compiler, view, content

class Core():
   def __init__(self, parent=None):
      # restore previous preferences

      self.restorePreferences()

      self.temp = tempfile.mkdtemp()
      # print(self.temp)

      self.tempcwd = False
      if(self.cwd == None or not os.path.isdir(self.cwd)):
         self.cwd = os.path.join(self.temp, 'cwd')
         self.tempcwd = True
         self.initnewproject()


      self.server = server.Server(self.temp)
      self.compiler = compiler.Compiler(self.temp)


   def restorePreferences(self):
      # print("restorePreferences")
      settings = QSettings('FiguresLibres', 'Cascade')
      # settings.clear()
      # print(settings.allKeys())

      self.cwd = settings.value('core/cwd', None)
      self.mw_size = settings.value('mainwindow/size', QtCore.QSize(1024, 768))
      self.mw_pos = settings.value('mainwindow/pos', QtCore.QPoint(0, 0))


   def savePreferences(self):
      # print("savePreferences")
      settings = QSettings('FiguresLibres', 'Cascade')
      # print(settings.allKeys())

      if not self.tempcwd:
         settings.setValue('core/cwd', self.cwd)

      settings.setValue('mainwindow/size', self.mainwindow.size())
      settings.setValue('mainwindow/pos', self.mainwindow.pos())
      # TODO: save splitters pos
      
   def initnewproject(self, cwd = None):
      if cwd == None :
         cwd = self.cwd
      else :
         self.cwd = cwd

      shutil.copytree('templates/newproject', cwd)
      self.prefs = json.loads(open(os.path.join(cwd,'.config/prefs.json')).read())
      self.summary = json.loads(open(os.path.join(cwd,'.config/summary.json')).read())
      self.repository = git.Repo.init(cwd)
      self.repository.index.add(['assets','contents','.config'])
      self.repository.index.commit("initial commit")
      # TODO: set mdtohtml compiler from project md to app index.html
      # TODO: embed project styles.scss to app scss frame work

   def saveproject(self, cwd = None):
      if not cwd == None and self.tempcwd:
         shutil.copytree(self.cwd, cwd)
         self.cwd = cwd
         self.tempcwd = False

   def quit(self):
      self.savePreferences()
      shutil.rmtree(self.temp, ignore_errors=True)
      QCoreApplication.instance().quit()

class MainWindow(QMainWindow):
   def __init__(self, core):
      super(MainWindow, self).__init__()

      # load core class
      self.core = core

      self.setWindowTitle("Cascade")
      self.setWindowIcon(QIcon('assets/images/icon.png'))

      self.resize(self.core.mw_size)
      self.move(self.core.mw_pos)

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

      self.save_action = QAction("&Save",self)
      self.save_action.setShortcut("Ctrl+s")
      file.addAction(self.save_action)
      if not self.core.tempcwd:
         self.save_action.setEnabled(False)

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
         self.openprojectdialogue()
      elif q.text() == "&Save":
         self.saveprojectdialogue()
      elif q.text() == "&Quit":
         self.quit()

   def openprojectdialogue(self):
      print("open")

   def newprojectdialogue(self):
      projectname = QFileDialog.getSaveFileName(self, 'New Project', '')
      # TODO: no file type
      try:
         if not os.path.isdir(projectname[0]):
            self.core.initnewproject(projectname[0])
         else:
            print("folder already exists")
            # TODO: check if is cascade folder
      except Exception as e:
         pass

   def saveprojectdialogue(self, quit=False):
      projectname = QFileDialog.getSaveFileName(self, 'Save Project', '')
      # TODO: no file type
      try:
         if not os.path.isdir(projectname[0]):
            self.core.saveproject(projectname[0])
            self.save_action.setEnabled(False)
            if quit:
               self.quit()
         else:
            print("folder already exists")
            # TODO: check if is cascade folder
      except Exception as e:
         pass

   def quit(self):
      print("Quit")
      if self.core.tempcwd:
         buttonReply = QMessageBox.question(self, 'Project Not Saved', "Do you want to save your current project before quiting?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
         if buttonReply == QMessageBox.Yes:
            self.saveprojectdialogue(quit=True)
         if buttonReply == QMessageBox.No:
            self.core.quit()
      else:
         self.core.quit()

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

      self.viewtab = view.ViewTab(self.core)
      self.contenttab = content.ContentTab(self.core)
      self.versiontab = QLabel("Version (git).")


      self.tabwidget.addTab(self.viewtab, "View")
      self.tabwidget.addTab(self.contenttab, "Content")
      self.tabwidget.addTab(self.versiontab, "Version")

      self.setCentralWidget(self.tabwidget)


def main():
   app = QApplication(sys.argv)
   core = Core()
   mainappwindow = MainWindow(core)
   core.mainwindow = mainappwindow
   sys.exit(app.exec_())



if __name__ == "__main__":
   main()
