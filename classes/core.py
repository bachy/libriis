#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import os, shutil, tempfile
# sys,
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings

import json
import git

from classes import server, sasscompiler, md2html


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
         self.initDeamons()
      else:
         self.initDeamons()


   def initDeamons(self):
      self.server = server.Server(self)
      self.sasscompiler = sasscompiler.Compiler(self)
      self.contentcompiler = md2html.Compiler(self)

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
      print('initnewproject')
      if cwd == None :
         cwd = self.cwd

      shutil.copytree(os.path.join(self.appcwd,'templates/newproject'), cwd)
      self.prefs = json.loads(open(os.path.join(cwd,'.config/prefs.json')).read())
      self.summary = json.loads(open(os.path.join(cwd,'.config/summary.json')).read())
      self.repository = git.Repo.init(cwd)
      self.repository.index.add(['assets','contents','.config'])
      self.repository.index.commit("initial commit")

      self.changeCWD(cwd)

   def saveproject(self, cwd = None):
      if not cwd == None:
         shutil.copytree(self.cwd, cwd)
         self.tempcwd = False
         self.changeCWD(cwd)

   def openproject(self, cwd=None):
      if not cwd == None:
         self.changeCWD(cwd)

   def changeCWD(self, cwd):
      if not cwd == self.cwd:
         self.cwd = cwd
         self._mw.setWindowTitle("Cascade – "+self.cwd)
         self.server.reload()
         self.sasscompiler.reload()
         self.contentcompiler.reload()
         self._mw.designstack.refresh()
         self._mw.contentstack.refresh()

   def quit(self):
      self.savePreferences()
      shutil.rmtree(self.temp, ignore_errors=True)
      QCoreApplication.instance().quit()
