#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import QFileSystemWatcher
import sass

class Compiler():
   def __init__(self,parent):
      self.parent = parent
      self.initWatching()
      self.compile_scss()
   # def directory_changed(path):
   #    print("Directory changed : %s" % path)

   def initWatching(self):
      self.refreshPaths()
      self.fs_watcher = QFileSystemWatcher(self.paths)
      # self.fs_watcher.directoryChanged.connect(self.directory_changed)
      self.fs_watcher.fileChanged.connect(self.compile_scss)

   def compile_scss(self):
      print("compiling sass")
      try:
         scss = sass.compile_file(str.encode(os.path.join(self.parent.cwd,'assets/css/main.scss')))
         with open(os.path.join(self.parent.cwd,'assets/css/main.css'), 'w') as fp:
            fp.write(scss.decode('utf8'))
      except Exception as e:
         print("Error compiling Sass", e)
         pass


   def refreshPaths(self):
      self.paths = [
         os.path.join(self.parent.cwd,'assets'),
         os.path.join(self.parent.cwd,'assets/css'),
         os.path.join(self.parent.cwd,'assets/css/styles.scss')
      ]

   def reload(self):
      self.fs_watcher.removePaths(self.paths)
      self.refreshPaths()
      self.fs_watcher.addPaths(self.paths)
