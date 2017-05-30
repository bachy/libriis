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
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QApplication, QShortcut, QGridLayout, QLabel, QTabWidget, QStackedWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSplitterHandle, QPlainTextEdit, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton
# from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage, QWebView, QWebInspector

import json
import git

from classes import server, sasscompiler, design, content

class Core():
   def __init__(self, parent=None):
      # restore previous preferences
      self.appcwd = os.getcwd()

      self.restorePreferences()
      self._mw = False
      self.temp = tempfile.mkdtemp()
      # print(self.temp)

      self.tempcwd = False
      # if ther's not current project folder from restorepref
      # initaite a new temp project
      if(self.cwd == None or not os.path.isdir(self.cwd)):
         self.cwd = os.path.join(self.temp, 'cwd')
         self.tempcwd = True
         self.initnewproject()

      self.server = server.Server(self)
      self.sasscompiler = sasscompiler.Compiler(self)

   @property
   def mainwindow(self):
      return self.mainwindow

   @mainwindow.setter
   def mainwindow(self, mw):
      if not self._mw:
         self._mw = mw
         if not self.tempcwd:
            self._mw.setWindowTitle("Cascade – "+self.cwd)


   def restorePreferences(self):
      # print("restorePreferences")
      settings = QSettings('FiguresLibres', 'Cascade')
      # settings.clear()
      # print(settings.allKeys())

      self.cwd = settings.value('core/cwd', None)
      self.dialog_path = settings.value('core/dialog_path', os.path.expanduser('~'))

      self.mw_size = settings.value('mainwindow/size', QtCore.QSize(1024, 768))
      self.mw_pos = settings.value('mainwindow/pos', QtCore.QPoint(0, 0))
      self.mw_curstack = int(settings.value('mainwindow/curstack', 0))


   def savePreferences(self):
      # print("savePreferences")
      settings = QSettings('FiguresLibres', 'Cascade')
      # print(settings.allKeys())

      if not self.tempcwd:
         settings.setValue('core/cwd', self.cwd)

      settings.setValue('core/dialog_path', self.dialog_path)

      settings.setValue('mainwindow/size', self._mw.size())
      settings.setValue('mainwindow/pos', self._mw.pos())
      settings.setValue('mainwindow/curstack', self._mw.mainstack.currentIndex())

   def initnewproject(self, cwd = None):
      if cwd == None :
         cwd = self.cwd
      else :
         self.changeCWD(cwd)

      shutil.copytree('templates/newproject', cwd)
      self.prefs = json.loads(open(os.path.join(cwd,'.config/prefs.json')).read())
      self.summary = json.loads(open(os.path.join(cwd,'.config/summary.json')).read())
      self.repository = git.Repo.init(cwd)
      self.repository.index.add(['assets','contents','.config'])
      self.repository.index.commit("initial commit")
      # TODO: set mdtohtml compiler from project md to app index.html
      # TODO: embed project styles.scss to app scss frame work

   def saveproject(self, cwd = None):
      if not cwd == None:
         shutil.copytree(self.cwd, cwd)
         self.tempcwd = False
         self.changeCWD(cwd)

   def changeCWD(self, cwd):
      self.cwd = cwd
      self.server.reload()
      self.sasscompiler.reload()
      # if not self.tempcwd:
      self._mw.setWindowTitle("Cascade – "+self.cwd)

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
      self.setWindowIcon(QIcon(os.path.join(self.core.appcwd,'assets/images/icon.png')))

      self.resize(self.core.mw_size)
      self.move(self.core.mw_pos)

      self.initMenuBar()

      self.initMainStack()

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

      self.save_action = QAction("&Save Project as",self)
      self.save_action.setShortcut("Ctrl+Shift+s")
      file.addAction(self.save_action)

      quit = QAction("&Quit",self)
      quit.setShortcut("Ctrl+q")
      file.addAction(quit)

      file.triggered[QAction].connect(self.onfilemenutrigger)

      # edit menu
      edit = bar.addMenu("&Edit")
      # edit.addAction("&copy")
      # edit.addAction("&paste")
      edit.addAction("&build")

      self.reload_action = QAction("&Reload",self)
      self.reload_action.setShortcut("Ctrl+r")
      edit.addAction(self.reload_action)

      edit.addAction("&preferences")

      edit.triggered[QAction].connect(self.oneditmenutrigger)


      # view menu
      view = bar.addMenu("&View")

      designview = QAction("&Design",self)
      designview.setShortcut("F1")
      view.addAction(designview)

      contentview = QAction("&Content",self)
      contentview.setShortcut("F2")
      view.addAction(contentview)

      versionview = QAction("&Version",self)
      versionview.setShortcut("F3")
      view.addAction(versionview)

      view.triggered[QAction].connect(self.onviewmenutrigger)

      # about menu
      about = bar.addMenu("About")
      about.addAction("&Website")


   def onfilemenutrigger(self, q):
      print(q.text()+" is triggered")
      if q.text() == "&New Project":
         self.newprojectdialogue()
      elif q.text() == "&Open":
         self.openprojectdialogue()
      elif q.text() == "&Save Project as":
         self.saveprojectdialogue()
      elif q.text() == "&Quit":
         self.quit()

   def openprojectdialogue(self):
      print("open")

   def newprojectdialogue(self):
      dialog = QFileDialog()
      dialog.setFileMode(QFileDialog.Directory)
      dialog.setAcceptMode(QFileDialog.AcceptOpen)
      projectname = dialog.getSaveFileName(
         self,
         'New Project',
         self.core.dialog_path
      )[0]
      # TODO: no file type
      try:
         head, tail = os.path.split(projectname)
         self.core.dialog_path = head
         if not os.path.isdir(projectname):
            self.core.initnewproject(projectname)
         else:
            print("folder already exists")
            # TODO: check if is cascade folder
      except Exception as e:
         print('Exception', e)
         pass

   def saveprojectdialogue(self, quit=False):
      dialog = QFileDialog()
      dialog.setFileMode(QFileDialog.Directory)
      dialog.setAcceptMode(QFileDialog.AcceptOpen)
      projectname = dialog.getSaveFileName(
         self,
         'Save Project',
         self.core.dialog_path
      )[0]
      # TODO: no file type
      try:
         head, tail = os.path.split(projectname)
         self.core.dialog_path = head
         if not os.path.isdir(projectname):
            self.core.saveproject(projectname)
            if quit:
               self.quit()
         else:
            print("folder already exists")
            # TODO: check if is cascade folder
      except Exception as e:
         print('Exception', e)
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


   def oneditmenutrigger(self, q):
      print(q.text()+" is triggered")
      if q.text() == "&Reload":
         self.designstack.webkitview.reload()


   def onviewmenutrigger(self, q):
      print(q.text()+" is triggered")
      if q.text() == "&Design":
         self.mainstack.setCurrentIndex(0)
      elif q.text() == "&Content":
         self.mainstack.setCurrentIndex(1)
      elif q.text() == "&Version":
         self.mainstack.setCurrentIndex(2)


   def initMainStack(self):
      self.mainstack = QStackedWidget()

      self.designstack = design.DesignStack(self.core)
      self.contentstack = content.ContentStack(self.core)
      self.versionstack = QLabel("Version (git).")

      self.mainstack.addWidget(self.designstack)
      self.mainstack.addWidget(self.contentstack)
      self.mainstack.addWidget(self.versionstack)

      self.mainstack.setCurrentIndex(self.core.mw_curstack)

      self.setCentralWidget(self.mainstack)


def main():
   app = QApplication(sys.argv)
   app.setOrganizationName('figli')
   app.setApplicationName('Cascade')
   core = Core()
   mainappwindow = MainWindow(core)
   core.mainwindow = mainappwindow
   sys.exit(app.exec_())



if __name__ == "__main__":
   main()
