#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, QLabel, QStackedWidget, QFileDialog, QMessageBox

from classes import design, content, docsetdialog



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

   #     __  ___                 ____
   #    /  |/  /__  ____  __  __/ __ )____ ______
   #   / /|_/ / _ \/ __ \/ / / / __  / __ `/ ___/
   #  / /  / /  __/ / / / /_/ / /_/ / /_/ / /
   # /_/  /_/\___/_/ /_/\__,_/_____/\__,_/_/
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

      self.save_action = QAction("&Save Project as",self)
      self.save_action.setShortcut("Ctrl+Shift+s")
      file.addAction(self.save_action)

      self.docset_action = QAction("&Document Settings",self)
      self.docset_action.setShortcut("Ctrl+d")
      file.addAction(self.docset_action)

      self.pdf_action = QAction("&PDF",self)
      self.pdf_action.setShortcut("Ctrl+p")
      file.addAction(self.pdf_action)

      self.quit_action = QAction("&Quit",self)
      self.quit_action.setShortcut("Ctrl+q")
      file.addAction(self.quit_action)

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
      elif q.text() == "&Document Settings":
         self.onDocSettings()
      elif q.text() == "&PDF":
         self.genPDF()
      elif q.text() == "&Quit":
         self.quit()

   def openprojectdialogue(self):
      print("open")
      dialog = QFileDialog()
      dialog.setFileMode(QFileDialog.Directory)
      dialog.setAcceptMode(QFileDialog.AcceptOpen)
      options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
      folder = dialog.getExistingDirectory(
         self,
         'Open Project',
         self.core.dialog_path,
         options
      )
      try:
         head, tail = os.path.split(folder)
         self.core.dialog_path = head
         # TODO: check if is cascade folder
         print(folder)
         if os.path.isdir(folder):
            self.core.openproject(folder)
         else:
            print("folder doesn't exists")
      except Exception as e:
         print('Exception', e)
         pass

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

   def onDocSettings(self):
      d = docsetdialog.DocsetDialog(self)
      d.exec_()
      self.core.recordDocSettings({
         "np":d.np.text(),
         "pw":d.pw.text(),
         "ph":d.ph.text(),
         "mt":d.mt.text(),
         "mb":d.mb.text(),
         "me":d.me.text(),
         "mi":d.mi.text(),
         "cs":d.cs.text(),
         "bs":d.bs.text(),
         "cn":d.cn.text(),
         "cg":d.cg.text(),
         "rn":d.rn.text(),
         "rg":d.rg.text(),
         "lh":d.lh.text()
      })

   def genPDF(self):
      print('PDF')
      self.designstack.webkitview.ongenPDF()

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

   #     __  ___      _      _____ __             __
   #    /  |/  /___ _(_)___ / ___// /_____ ______/ /__
   #   / /|_/ / __ `/ / __ \\__ \/ __/ __ `/ ___/ //_/
   #  / /  / / /_/ / / / / /__/ / /_/ /_/ / /__/ ,<
   # /_/  /_/\__,_/_/_/ /_/____/\__/\__,_/\___/_/|_|
   def initMainStack(self):
      self.mainstack = QStackedWidget()

      self.designstack = design.DesignStack(self.core)
      self.contentstack = content.ContentStack(self.core)
      self.versionstack = QLabel("Version (git).")

      self.mainstack.addWidget(self.designstack)
      self.mainstack.addWidget(self.contentstack)
      self.mainstack.addWidget(self.versionstack)

      self.mainstack.setCurrentIndex(self.core.mw_curstack)

      # TODO: add an app console window (show sass compilation errors for example)

      self.setCentralWidget(self.mainstack)
