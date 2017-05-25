#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QFileSystemWatcher
import sass

class Compiler():
   def __init__(self,parent=None):
      paths = [
         'assets',
         'assets/scss',
         'assets/scss/styles.scss'
      ]
      self.fs_watcher = QFileSystemWatcher(paths)
      # self.fs_watcher.directoryChanged.connect(self.directory_changed)
      self.fs_watcher.fileChanged.connect(self.compile_scss)
      self.compile_scss()

   # def directory_changed(path):
   #    print("Directory changed : %s" % path)

   def compile_scss(path = ""):
      print("compiling sass : %s" % path)
      scss = sass.compile_file(b'assets/scss/main.scss')
      with open('assets/scss/main.css', 'w') as fp:
         fp.write(scss.decode('utf8'))
