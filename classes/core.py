#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import os, re, shutil, tempfile
# sys,
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings, QCoreApplication

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
         head, tail = os.path.split(self.cwd)
         print('tail', tail)
         self.projectname = tail

      self.loadDocSettings()


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

   def loadDocSettings(self):
      self.docsettings = json.loads(open(os.path.join(self.cwd,'.config/docsettings.json')).read())

   def recordDocSettings(self,docsettings):
      # print("doc settings",docsettings)
      for key in docsettings:
         self.docsettings[key] = docsettings[key]
      jsonfilepath = os.path.join(self.cwd,'.config/docsettings.json')
      with open(jsonfilepath, "w") as fp:
         json.dump(self.docsettings, fp, ensure_ascii=False, indent="\t")

      self.updateScss()

   def updateScss(self):
      # print(self.docsettings)
      sassfilepath = os.path.join(self.cwd,'assets/css/main.scss')
      # print(sassfilepath)
      sass = open(sassfilepath,"r").read()
      
      # $page-width: mm2pt(180);
      sass = re.sub(
         r'\$page-width:\smm2pt\([0-9|\.]+\);',
         '$page-width: mm2pt('+self.docsettings['pw']+');',
         sass)
      # $page-height: mm2pt(287);
      sass = re.sub(
         r'\$page-height:\smm2pt\([0-9|\.]+\);',
         '$page-height: mm2pt('+self.docsettings['ph']+');',
         sass)

      # $page-margin-outside: mm2pt(15);
      sass = re.sub(
         r'\$page-margin-outside:\smm2pt\([0-9|\.]+\);',
         '$page-margin-outside: mm2pt('+self.docsettings['me']+');',
         sass)
      # $page-margin-inside: mm2pt(7.5);
      sass = re.sub(
         r'\$page-margin-inside:\smm2pt\([0-9|\.]+\);',
         '$page-margin-inside: mm2pt('+self.docsettings['mi']+');',
         sass)
      # $page-margin-top: mm2pt(10);
      sass = re.sub(
         r'\$page-margin-top:\smm2pt\([0-9|\.]+\);',
         '$page-margin-top: mm2pt('+self.docsettings['mt']+');',
         sass)
      # $page-margin-bottom: mm2pt(10);
      sass = re.sub(
         r'\$page-margin-bottom:\smm2pt\([0-9|\.]+\);',
         '$page-margin-bottom: mm2pt('+self.docsettings['mb']+');',
         sass)

      # $crop-size: mm2pt(2);
      sass = re.sub(
         r'\$crop-size:\smm2pt\([0-9|\.]+\);',
         '$crop-size: mm2pt('+self.docsettings['cs']+');',
         sass)
      # $bleed: mm2pt(3);
      sass = re.sub(
         r'\$bleed:\smm2pt\([0-9|\.]+\);',
         '$bleed: mm2pt('+self.docsettings['bs']+');',
         sass)

      # $col-number: 9;
      sass = re.sub(
         r'\$col-number:\smm2pt\([0-9|\.]+\);',
         '$col-number: mm2pt('+self.docsettings['cn']+');',
         sass)
      # $col-gutter: mm2pt(3);
      sass = re.sub(
         r'\$col-butter:\smm2pt\([0-9|\.]+\);',
         '$col-butter: mm2pt('+self.docsettings['cg']+');',
         sass)
      #
      # $row-number: 12;
      sass = re.sub(
         r'\$row-number:\smm2pt\([0-9|\.]+\);',
         '$row-number: mm2pt('+self.docsettings['rn']+');',
         sass)
      # $row-gutter: mm2pt(4);
      sass = re.sub(
         r'\$row-butter:\smm2pt\([0-9|\.]+\);',
         '$row-butter: mm2pt('+self.docsettings['rg']+');',
         sass)
      #
      # $line-height: mm2pt(4);
      sass = re.sub(
         r'\$line-height:\smm2pt\([0-9|\.]+\);',
         '$line-height: mm2pt('+self.docsettings['lh']+');',
         sass)

      # print('sass', sass)
      open(sassfilepath,"w").write(sass)

      self._mw.designstack.webkitview.reload()


   def initnewproject(self, cwd = None):
      print('initnewproject')
      if cwd == None :
         cwd = self.cwd

      shutil.copytree(os.path.join(self.appcwd,'templates/newproject'), cwd)
      self.changeCWD(cwd)
      self.loadDocSettings()
      # self.docsettings = json.loads(open(os.path.join(cwd,'.config/docsettings.json')).read())
      self.summary = json.loads(open(os.path.join(cwd,'.config/summary.json')).read())
      self.repository = git.Repo.init(cwd)
      self.repository.index.add(['assets','contents','.config'])
      self.repository.index.commit("initial commit")


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
         self.server.reload()
         self.sasscompiler.reload()
         self.contentcompiler.reload()

      if not self.tempcwd:
         self._mw.setWindowTitle("Cascade – "+self.cwd)
         head, tail = os.path.split(self.cwd)
         print('tail', projectname)
         self.projectname = tail
         self._mw.designstack.refresh()
         self._mw.contentstack.refresh()

   def quit(self):
      self.savePreferences()
      shutil.rmtree(self.temp, ignore_errors=True)
      QCoreApplication.instance().quit()
