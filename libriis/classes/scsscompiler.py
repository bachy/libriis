#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   30-05-2017
# @Email:  bachir@figureslibres.io
# @Filename: scsscompiler.py
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

from __future__ import absolute_import, print_function, division, unicode_literals

import os
from PyQt5.QtCore import QFileSystemWatcher
import scss

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
      print("compiling scss")
      try:
         import_path = ['./assets/css/']
         print("import path",import_path)
         comp = scss.Compiler(output_style="compressed", search_path=import_path)
         # Compiler().compile_string("a { color: red + green; }")
         scss_file = open(os.path.join(self.parent.cwd,'assets/css/main.scss'),"r")
         css = comp.compile_string(scss_file.read())
         # print("css : %s" % css)
         with open(os.path.join(self.parent.cwd,'assets/css/main.css'), 'w') as fp:
            fp.write(css)
      except Exception as e:
         print("Error compiling scss", e)
         pass

   def refreshPaths(self):
      self.paths = [
         os.path.join(self.parent.cwd,'assets'),
         os.path.join(self.parent.cwd,'assets/css')
      ]
      # os.path.join(self.parent.cwd,'assets/css/styles.scss')
      for f in os.listdir(os.path.join(self.parent.cwd,'assets/css')):
         if f.endswith("scss"):
            self.paths.append(os.path.join(self.parent.cwd,'assets/css',f))

   def reload(self):
      print('Reload scss compiler')
      self.fs_watcher.removePaths(self.paths)
      self.refreshPaths()
      print('paths', self.paths)
      self.fs_watcher.addPaths(self.paths)
      print('files', self.fs_watcher.files())
      self.compile_scss()
