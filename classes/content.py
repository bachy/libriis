#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSplitter, QListWidget, QListWidgetItem, QAbstractItemView, QButtonGroup, QPushButton, QInputDialog

import markdown
import re
import json

# from classes import orderablelist


class Summary(QWidget):
   def __init__(self, core):
      super(Summary, self).__init__()
      self.core = core

      self.jsonfilepath = os.path.join(self.core.cwd,'.config/summary.json')
      sum_json = open(self.jsonfilepath).read()
      self.sum = json.loads(sum_json)

      vbox = QVBoxLayout()
      vbox.setContentsMargins(0,0,0,0)

      self.list = SummaryList(self)
      vbox.addWidget(self.list)

      self.actions = SummaryActions(self, core)
      vbox.addWidget(self.actions)

      self.setLayout(vbox)

   def addItem(self, text):
      # file
      filename = re.sub(r'\W', "_", text)+".md"
      # TODO: check if file does not already exists
      filepath = os.path.join(self.core.cwd,'contents',filename)
      with open(filepath, 'w') as fp:
         fp.write('#'+text)
      # json
      item = {"title":text,"file":filename}
      self.sum.append(item)
      with open(self.jsonfilepath, "w") as fp:
         json.dump(self.sum, fp, ensure_ascii=False, indent="\t")
      # refresh list
      self.list.addNewItem(item)

   def recordNewList(self):

      newdata = []
      for i in range(0,self.list.count()):
         # print(self.item(i).item['title'])
         newdata.append(self.list.item(i).item)

      # print(newdata)
      self.sum = newdata
      with open(self.jsonfilepath, "w") as fp:
         json.dump(newdata, fp, ensure_ascii=False, indent="\t")


class SummaryList(QListWidget):
   def __init__(self, parent):
      super(SummaryList, self).__init__(parent)
      self.parent = parent
      # self.sum = sum
      # print(self.sum)
      # self.setSortingEnabled(True)
      self.setDragEnabled(True)
      self.setSelectionMode(QAbstractItemView.SingleSelection)
      self.setAcceptDrops(True)
      self.setDropIndicatorShown(True)
      self.setDragDropMode(QAbstractItemView.InternalMove)

      self.model().rowsMoved.connect(self.onRowsMoved)
      print(self.model())

      for item in self.parent.sum:
         self.addNewItem(item)

   def onRowsMoved(self, model, start, end, dest):
      # print("onRowsMoved")
      self.parent.recordNewList()

   def addNewItem(self, item):
      # slw = SummaryListWidgetItem(self,item)
      # lwi = QListWidgetItem(self)
      # # Set size hint
      # lwi.setSizeHint(slw.sizeHint())
      # self.addItem(lwi)
      # self.setItemWidget(lwi, slw)
      # # self.addItem(QListWidgetItem())
      self.addItem(SummaryListWidgetItem(self,item))

class SummaryListWidgetItem(QListWidgetItem):
   def __init__(self,parent,item):
      super(SummaryListWidgetItem, self).__init__(parent)
      self.parent = parent
      self.item = item

      self.setText(item['title'])
      self.setToolTip(item['file'])


class SummaryActions(QWidget):
   def __init__(self,parent,core):
      super(SummaryActions, self).__init__(parent)

      self.parent = parent
      self.core = core

      self.hbox = QHBoxLayout()
      self.hbox.setContentsMargins(0,0,0,0)

      new = QPushButton("New Page", self)
      new.setShortcut('Ctrl+Shift+n')
      # new.setIcon(Icon(ico)))
      new.clicked.connect(self.onAddPage)
      self.hbox.addWidget(new)

      delete = QPushButton("Delete Page", self)
      delete.setShortcut('Ctrl+Shift+sup')
      # delete.setIcon(Icon(ico)))
      delete.clicked.connect(self.onDeletePage)
      self.hbox.addWidget(delete)


      self.setLayout(self.hbox)

   def onAddPage(self):
      text, ok = QInputDialog.getText(self, 'Input Dialog', 'Page Name:')
      if ok:
         self.parent.addItem(text)

   def onDeletePage(self):
      print("onDeletePage")
      # TODO: get the current selected page
      # TODO: ask for confirmation for deleting the current selecred page
      # TODO: call for summary widget to delete the page

class ContentStack(QWidget):
   def __init__(self, core):
      super(ContentStack, self).__init__()

      # self.grid = QGridLayout()
      hbox = QHBoxLayout()
      hbox.setContentsMargins(0,0,0,0)
      self.setLayout(hbox)

      self.hsplitter = QSplitter(QtCore.Qt.Horizontal)

      self.summary = Summary(core)
      self.hsplitter.addWidget(self.summary)

      self.mdsource = QLabel("Content (markdown src).")
      self.hsplitter.addWidget(self.mdsource)

      self.mdpreview = QLabel("Content (markdown preview).")
      self.hsplitter.addWidget(self.mdpreview)

      self.hsplitter.splitterMoved.connect(self.movedSplitter)

      hbox.addWidget(self.hsplitter)

      self.restorePrefs()


   def restorePrefs(self):
      settings = QSettings('FiguresLibres', 'Cascade')
      vals = settings.value('content/hsplitter/sizes', None)
      if vals:
         sizes = []
         for size in vals: sizes.append(int(size))
         self.hsplitter.setSizes(sizes)

   def movedSplitter(self):
      settings = QSettings('FiguresLibres', 'Cascade')
      # print(self.hsplitter.sizes())
      settings.setValue('content/hsplitter/sizes', self.hsplitter.sizes())
