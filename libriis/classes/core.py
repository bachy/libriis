#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

from __future__ import absolute_import, print_function, division, unicode_literals

import os, re, shutil, tempfile
# sys,
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings, QCoreApplication

import json
# import git
# from pygit2 import Repository

from . import server, sasscompiler, md2html

#    ______
#   / ____/___  ________
#  / /   / __ \/ ___/ _ \
# / /___/ /_/ / /  /  __/
# \____/\____/_/   \___/
class Core():
   def __init__(self, apppath):
      # restore previous preferences
      self.appcwd = apppath

      self.restorePreferences()
      self._mw = False
      self.temp = tempfile.mkdtemp()
      # print(self.temp)
      self.projectname = "Libriis"

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
            self._mw.setWindowTitle("Libriis – "+self.cwd)

   #     ____            ____
   #    / __ \________  / __/____
   #   / /_/ / ___/ _ \/ /_/ ___/
   #  / ____/ /  /  __/ __(__  )
   # /_/   /_/   \___/_/ /____/
   def restorePreferences(self):
      # print("restorePreferences")
      settings = QSettings('FiguresLibres', 'Libriis')
      # settings.clear()
      # print(settings.allKeys())

      self.cwd = settings.value('core/cwd', None)
      self.dialog_path = settings.value('core/dialog_path', os.path.expanduser('~'))

      self.mw_size = settings.value('mainwindow/size', QtCore.QSize(1024, 768))
      self.mw_pos = settings.value('mainwindow/pos', QtCore.QPoint(0, 0))
      self.mw_curstack = int(settings.value('mainwindow/curstack', 0))

   def savePreferences(self):
      # print("savePreferences")
      settings = QSettings('FiguresLibres', 'Libriis')
      # print(settings.allKeys())

      if not self.tempcwd:
         settings.setValue('core/cwd', self.cwd)

      settings.setValue('core/dialog_path', self.dialog_path)

      settings.setValue('mainwindow/size', self._mw.size())
      settings.setValue('mainwindow/pos', self._mw.pos())
      settings.setValue('mainwindow/curstack', self._mw.mainstack.currentIndex())

   #     ____                _____      __  __  _
   #    / __ \____  _____   / ___/___  / /_/ /_(_)___  ____ ______
   #   / / / / __ \/ ___/   \__ \/ _ \/ __/ __/ / __ \/ __ `/ ___/
   #  / /_/ / /_/ / /__    ___/ /  __/ /_/ /_/ / / / / /_/ (__  )
   # /_____/\____/\___/   /____/\___/\__/\__/_/_/ /_/\__, /____/
   #                                                /____/
   def loadDocSettings(self):
      print('loadDocSettings')
      self.docsettings = json.loads(open(os.path.join(self.cwd,'.config/docsettings.json')).read())

   def recordDocSettings(self,docsettings):
      # print("doc settings",docsettings)
      for key in docsettings:
         self.docsettings[key] = docsettings[key]
      jsonfilepath = os.path.join(self.cwd,'.config/docsettings.json')
      with open(jsonfilepath, "w") as fp:
         json.dump(self.docsettings, fp, ensure_ascii=False, indent="\t")

      self.updateScss(False)
      self.updateJs()

   def updateScss(self, reload=True):
      # print(self.docsettings)
      sassfilepath = os.path.join(self.cwd,'assets/css/setup.scss')
      # print(sassfilepath)
      sass = open(sassfilepath,"r").read()
      sets = {
         'pw':'page-width',
         'ph':'page-height',
         'mt':'page-margin-top',
         'mb':'page-margin-bottom',
         'me':'page-margin-outside',
         'mi':'page-margin-inside',
         'cs':'crop-size',
         'bs':'bleed',
         'cg':'col-gutter',
         'rg':'row-gutter',
         'lh':'line-height'
      }
      for s in sets:
         sass = re.sub(
            r'\$'+sets[s]+':\smm2pt\([0-9|\.]+\);',
            '$'+sets[s]+': mm2pt('+self.docsettings[s]+');',
            sass)

      # $col-number: 9;
      sass = re.sub(
         r'\$col-number:\s[0-9|\.]+;',
         '$col-number: '+self.docsettings['cn']+';',
         sass)
      # $row-number: 12;
      sass = re.sub(
         r'\$row-number:\s[0-9|\.]+;',
         '$row-number: '+self.docsettings['rn']+';',
         sass)
      #$header-odd: "Libriis, default header";
      sass = re.sub(
         r'\$header-odd:\s".+";',
         '$header-odd: "'+self.docsettings['ho']+'";',
         sass)
      # $header-even: "Libriis, default header";
      sass = re.sub(
         r'\$header-even:\s".+";',
         '$header-even: "'+self.docsettings['he']+'";',
         sass)

      # print('sass', sass)
      open(sassfilepath,"w").write(sass)

      if reload:
         self._mw.designstack.webkitview.reload()

   def updateJs(self, reload=True):
      # print(self.docsettings)
      jsfilepath = os.path.join(self.cwd,'assets/js/setup.js')
      # print(jsfilepath)
      js = open(jsfilepath,"r").read()

      # $row-number: 12;
      js = re.sub(
         r'nb_page=[0-9]+;',
         'nb_page='+str(self.docsettings['np'])+';',
         js)

      # print('sass', sass)
      open(jsfilepath,"w").write(js)

      if reload:
         self._mw.designstack.webkitview.reload()

   def addPage(self):
      self.docsettings['np'] = int(self.docsettings['np'])+1
      self.updateJs()

   def rmPage(self):
      self.docsettings['np'] = int(self.docsettings['np'])-1
      self.updateJs()

   #     ____               _           __
   #    / __ \_________    (_)__  _____/ /_
   #   / /_/ / ___/ __ \  / / _ \/ ___/ __/
   #  / ____/ /  / /_/ / / /  __/ /__/ /_
   # /_/   /_/   \____/_/ /\___/\___/\__/
   #                 /___/
   def initnewproject(self, cwd = None):
      print('initnewproject')
      if cwd == None :
         cwd = self.cwd

      shutil.copytree(os.path.join(self.appcwd,'templates/newproject'), cwd)
      self.changeCWD(cwd)
      self.loadDocSettings()
      self.summary = json.loads(open(os.path.join(cwd,'.config/summary.json')).read())
      print('summary', summary)
      # TODO: try python-pygit2 arch package
      # self.repository = git.Repo.init(cwd)
      # TODO: set git config user.name & user.email
      # self.repository
      # self.repository.index.add(['assets','contents','.config'])
      # self.repository.index.commit("initial commit")


   def saveproject(self, cwd = None):
      if not cwd == None:
         shutil.copytree(self.cwd, cwd)
         self.tempcwd = False
         self.changeCWD(cwd)

   def openproject(self, cwd=None):
      if not cwd == None:
         self.changeCWD(cwd)

   #         __                           _______       ______
   #   _____/ /_  ____ _____  ____ ____  / ____/ |     / / __ \
   #  / ___/ __ \/ __ `/ __ \/ __ `/ _ \/ /    | | /| / / / / /
   # / /__/ / / / /_/ / / / / /_/ /  __/ /___  | |/ |/ / /_/ /
   # \___/_/ /_/\__,_/_/ /_/\__, /\___/\____/  |__/|__/_____/
   #                       /____/
   def changeCWD(self, cwd):
      print('changeCWD :: cwd', cwd)
      if not cwd == self.cwd:
         self.cwd = cwd
         self.server.reload()
         self.sasscompiler.reload()
         self.contentcompiler.reload()

      if not self.tempcwd:
         self._mw.setWindowTitle("Libriis – "+self.cwd)
         head, tail = os.path.split(self.cwd)
         print('changeCWD :: tail', tail)
         self.projectname = tail
         self._mw.designstack.refresh()
         self._mw.contentstack.refresh()

   #    ____        _ __
   #   / __ \__  __(_) /_
   #  / / / / / / / / __/
   # / /_/ / /_/ / / /_
   # \___\_\__,_/_/\__/
   def quit(self):
      self.savePreferences()
      shutil.rmtree(self.temp, ignore_errors=True)
      QCoreApplication.instance().quit()
