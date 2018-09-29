#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Filename: md2html.py
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

from __future__ import absolute_import, print_function, division, unicode_literals

import os
import re
from PyQt5.QtCore import QFileSystemWatcher
import json
from bs4 import BeautifulSoup
import pypandoc
import pyphen


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

      # hyphenator
      self._H_FR = pyphen.Pyphen(lang='fr')
      # TODO: add to settings language choice

      # create main html dom from template
      template_f = open(os.path.join(self.core.appcwd,"templates/main.tpl.html"), "r")
      template_html = template_f.read()
      template_dom = BeautifulSoup(template_html, 'html.parser')

      # get story div
      story_dom = template_dom.find('div', {"id":"flow-main"})

      # page index
      pi = 0
      # loop through pages following summary (pages liste)
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

         pdoc_args = ['--mathjax']

         pdoc_filters = []

         # convert markdown from file to html
         output = pypandoc.convert_file(in_f,
                               to='html5',
                               format='markdown+smart+header_attributes+link_attributes+bracketed_spans',
                               extra_args=pdoc_args,
                               filters=pdoc_filters)
         # print(output)

         # convert html string to parseable html dom
         output_dom = BeautifulSoup(output, 'html.parser')

         # hyphenate paragraphes
         # for node in output_dom.find_all('p'):
         #    self.hyphenate(node)

         # append html story page to template_dom
         # create a page dom
         story_page = BeautifulSoup(
            '<div class="story-page story-page-'+str(pi)+'" id="'+pageid+'"></div>',
            'html.parser'
         )
         # append to page dom the converted content
         story_page.div.append(output_dom)
         # append to global dom content the page with contents
         story_dom.append(story_page)

         # increment pahe index
         pi = pi+1

      # create main html file from filled template html dom
      book_html_f = os.path.join(self.core.cwd,'index.html')
      with open(book_html_f, 'w') as fp:
         fp.write(template_dom.prettify())


   #     __  __            __
   #    / / / /_  ______  / /_  ___  ____  _____
   #   / /_/ / / / / __ \/ __ \/ _ \/ __ \/ ___/
   #  / __  / /_/ / /_/ / / / /  __/ / / (__  )
   # /_/ /_/\__, / .___/_/ /_/\___/_/ /_/____/
   #       /____/_/
   def hyphenate(self, node):
      # print("hyphenate")
      nodetext = node.get_text()
      # print(nodetext)

      nodestr = str(node)
      # print(nodestr)
      for word in nodetext.split(' '):

         # do not hyphenate if it's not a real word
         if len(word) < 5 or re.search('\w+', word) == None:
            continue

         # cleaning word
         # remove all non-alphanumerical characteres duplicated or more
         word = re.sub('\W{2,}', '', word)
         # remove all non-alphanumerical at the begining of word
         word = re.sub('^\W', '', word)
         # remove all non-alphanumerical at the end of word
         word = re.sub('\W$', '', word)

         # remove all word remaing having special chars
         if re.search('\W+', word):
            continue

         # hyphenate word
         word_hyphenated = self._H_FR.inserted(word)
         # remove hyphen precedeted by less than 3 letters
         word_hyphenated = re.sub(r'^(\w{,2})-', r'\1', word_hyphenated)
         # remove hyphen followed by less than 3 letters
         word_hyphenated = re.sub(r'-(\w{,2})$', r'\1', word_hyphenated)
         # replace scores by html elemt &shy;
         word_hyphenated = re.sub(r'(\w)-(\w)', r'\1&shy;\2', word_hyphenated)
         # replace double scores by score+$shy;
         word_hyphenated = re.sub(r'--', r'-&shy;', word_hyphenated)
         # TODO: attention au date 1950-1960, le tiret disparait

         # print(word_hyphenated)

         if re.search('\b+', word):
            print(word+" | "+word_hyphenated)

         try:
            # replace word by hyhanated_word on source
            nodestr = re.sub(word, word_hyphenated, nodestr)
            # replaced_str_dom = BeautifulSoup(replaced_str, 'html.parser')
            # node.string = replaced_str
            # node.string.replace_with(node.string)
         except Exception as e:
            print(_ERROR_PREF+'Replacement error with \033[1m'+word+'\033[0m | \033[1m'+word_hyphenated+"\033[0m")
            print(e)
            print(node.string)
            print('[//]')
            pass

      # add none breaking spaces
      nbspzr_before = ['»', '\!', '\?', ':', ';']
      for char in nbspzr_before:
         nodestr = re.sub(r'(\w|>)\s('+char+')', r'\1&nbsp;\2', nodestr)

      nbspzr_after = ['«']
      for char in nbspzr_after:
         nodestr = re.sub(r'('+char+')\s(\w|<)', r'\1&nbsp;\2', nodestr)

      # print(nodestr)
      # replace node by hyphenated one
      node.replace_with(nodestr)
