#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import QFileSystemWatcher
import json


class Compiler():
   def __init__(self,parent):
      self.parent = parent
      self.initWatching()
      self.compileContents()

   def initWatching(self):
      self.refreshPaths()
      self.fs_watcher = QFileSystemWatcher(self.paths)
      # self.fs_watcher.directoryChanged.connect(self.directory_changed)
      self.fs_watcher.fileChanged.connect(self.onMdFileChanged)

   def onMdFileChanged(self):
      print("onMdFileChanged")
      try:
         self.compileContents()
      except Exception as e:
         print("Error compiling MD files", e)
         pass

   def refreshPaths(self):
      jsonfilepath = os.path.join(self.parent.cwd,'.config/summary.json')
      sum_json = open(jsonfilepath).read()
      self.sum = json.loads(sum_json)

      self.paths = [os.path.join(self.parent.cwd,'contents')]
      for item in self.sum:
         self.paths.append(os.path.join(self.parent.cwd,'contents',item['file']))

   def reload(self):
      self.fs_watcher.removePaths(self.paths)
      self.refreshPaths()
      self.fs_watcher.addPaths(self.paths)
      self.compileContents()

   def compileContents(self):
      print('Compiling md')
