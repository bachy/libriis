#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
from PyQt5.QtCore import QFileSystemWatcher
import json
from bs4 import BeautifulSoup
import pypandoc


class Compiler():
   def __init__(self,core):
      self.core = core
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
      jsonfilepath = os.path.join(self.core.cwd,'.config/summary.json')
      sum_json = open(jsonfilepath).read()
      self.sum = json.loads(sum_json)

      self.paths = [os.path.join(self.core.cwd,'contents')]
      for item in self.sum:
         self.paths.append(os.path.join(self.core.cwd,'contents',item['file']))

   def reload(self):
      self.fs_watcher.removePaths(self.paths)
      self.refreshPaths()
      self.fs_watcher.addPaths(self.paths)
      self.compileContents()

   def compileContents(self):
      print('Compiling md')

      # create main html dom from template
      template_f = open(os.path.join(self.core.appcwd,"templates/main.tpl.html"), "r")
      template_html = template_f.read()
      template_dom = BeautifulSoup(template_html, 'html.parser')

      # get story div
      story_dom = template_dom.find('div', {"id":"flow-main"})

      pi = 0
      for p in self.sum:
         # print(toc[p])
         pagename = p['title']
         pageid = re.sub('[^a-z0-9]+', '-', pagename.lower())
         print(pageid)

         # files
         in_f = os.path.join(self.core.cwd, "contents", p['file'])
         if not os.path.isfile(in_f):
            print("Source path is not a file, can't generate html : "+in_f)
            continue
         # print('in_f : '+in_f)

         pdoc_args = ['--mathjax',
                      '--smart']

         pdoc_filters = []

         output = pypandoc.convert_file(in_f,
                                  to='html5',
                                  format='markdown+header_attributes+link_attributes+bracketed_spans',
                                  extra_args=pdoc_args,
                                  filters=pdoc_filters)

         output_dom = BeautifulSoup(output, 'html.parser')

         # append html story page to template_dom
         story_page = BeautifulSoup(
            '<div class="story-page story-page-'+str(pi)+'" id="'+pageid+'"></div>',
            'html.parser'
         )
         story_page.div.append(output_dom)
         story_dom.append(story_page)


         pi = pi+1

      # create main html file from filled template html dom
      book_html_f = os.path.join(self.core.cwd,'index.html')
      with open(book_html_f, 'w') as fp:
         fp.write(template_dom.prettify())








      #
