#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QKeySequence
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSplitter, QListWidget, QListWidgetItem, QAbstractItemView, QButtonGroup, QPushButton, QInputDialog, QPlainTextEdit, QTextEdit,QShortcut

import markdown2
import re
import json


#    _____
#   / ___/__  ______ ___  ____ ___  ____ ________  __
#   \__ \/ / / / __ `__ \/ __ `__ \/ __ `/ ___/ / / /
#  ___/ / /_/ / / / / / / / / / / / /_/ / /  / /_/ /
# /____/\__,_/_/ /_/ /_/_/ /_/ /_/\__,_/_/   \__, /
#                                           /____/
class Summary(QWidget):
   def __init__(self, parent):
      super(Summary, self).__init__(parent)
      self.parent = parent

      jsonfilepath = os.path.join(self.parent.core.cwd,'.config/summary.json')
      sum_json = open(jsonfilepath).read()
      self.sum = json.loads(sum_json)

      vbox = QVBoxLayout()
      vbox.setContentsMargins(0,0,0,0)

      self.list = SummaryList(self)
      vbox.addWidget(self.list)

      self.actions = SummaryActions(self)
      vbox.addWidget(self.actions)

      self.setLayout(vbox)

   def addItem(self, text):
      # file
      filename = re.sub(r'\W', "_", text)+".md"
      # TODO: check if file does not already exists
      filepath = os.path.join(self.parent.core.cwd,'contents',filename)
      with open(filepath, 'w') as fp:
         fp.write('#'+text)
      # json
      item = {"title":text,"file":filename}
      self.sum.append(item)
      jsonfilepath = os.path.join(self.parent.core.cwd,'.config/summary.json')
      with open(jsonfilepath, "w") as fp:
         json.dump(self.sum, fp, ensure_ascii=False, indent="\t")
      # refresh list
      self.list.addNewItem(item)

   def recordNewList(self):

      newdata = []
      for i in range(0,self.list.count()):
         # print(self.item(i).item['title'])
         newdata.append(self.list.item(i).data)

      # print(newdata)
      self.sum = newdata
      jsonfilepath = os.path.join(self.parent.core.cwd,'.config/summary.json')
      with open(jsonfilepath, "w") as fp:
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
      # print(self.model())

      self.itemActivated.connect(self.onItemActivated)

      # add markdown files to the list
      for itemdata in self.parent.sum:
         self.addNewItem(itemdata)

      # self.setCurrentRow(0)
      # self.setCurrentIndex()
      # self.setCurrentItem()
      self.item(0).setSelected(True)
      # TODO: activate first item by default as it will open it with editor

      # TODO: show activated item on the list
      # TODO: show modifed item on the list

   def onRowsMoved(self, model, start, end, dest):
      # print("onRowsMoved")
      self.parent.recordNewList()

   def addNewItem(self, item):
      self.addItem(SummaryListWidgetItem(self,item))

   def onItemActivated(self, item):
      # print('onItemActivated', item.data)
      self.parent.parent.editor.openFile()


class SummaryListWidgetItem(QListWidgetItem):
   def __init__(self,parent,data):
      super(SummaryListWidgetItem, self).__init__(parent)
      self.parent = parent
      self.data = data

      self.setText(data['title'])
      self.setToolTip(data['file'])


class SummaryActions(QWidget):
   def __init__(self,parent):
      super(SummaryActions, self).__init__(parent)

      self.parent = parent

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

#     ______    ___ __
#    / ____/___/ (_) /_____  _____
#   / __/ / __  / / __/ __ \/ ___/
#  / /___/ /_/ / / /_/ /_/ / /
# /_____/\__,_/_/\__/\____/_/
class MarkdownEditor(QWidget):
   def __init__(self,parent):
      super(MarkdownEditor, self).__init__(parent)
      self.parent = parent
      self.changed = False

      self.hbox = QHBoxLayout()
      self.hbox.setContentsMargins(0,0,0,0)

      self.styles = """
         background-color:white;
         color:black;
         padding:20px;
      """

      self.editor = QPlainTextEdit(self)
      self.editor.setStyleSheet(self.styles)
      self.hbox.addWidget(self.editor)

      self.viewer = QTextEdit(self)
      self.viewer.setReadOnly(True)
      self.viewer.setStyleSheet(self.styles)
      # TODO: show all html blocks on viewer
      self.hbox.addWidget(self.viewer)

      self.setLayout(self.hbox)

      self.editor.textChanged.connect(self.onTextChanged)
      self.openFile()

      self.shortcut = QShortcut(QKeySequence("Ctrl+s"), self)
      self.shortcut.activated.connect(self.save)

      self.refreshViewer()

   def openFile(self):
      # print("openFile")
      sumlist = self.parent.summary.list
      currentitem = sumlist.currentItem()
      if currentitem:
         if not self.changed:
            self.editor.textChanged.disconnect(self.onTextChanged)
            filename = currentitem.data['file']
            self.file = os.path.join(self.parent.core.cwd,'contents',filename)
            self.editor.clear()
            self.editor.insertPlainText(open(self.file, 'r').read())
            self.refreshViewer()
            self.editor.textChanged.connect(self.onTextChanged)
         else:
            print("Can't changed file, current id modified, please save first")
            # TODO: ask for saving current file

   def onTextChanged(self):
      self.refreshViewer()
      if not self.changed:
         self.changed = True
         # i = self.tabs.currentIndex()
         # self.tabs.setTabText(i, "* "+self.tabs.tabText(i))

   def refreshViewer(self):
      markdown = self.editor.toPlainText()
      html = markdown2.markdown(markdown)
      self.viewer.setHtml(html)

   def save(self):
      if self.changed:
         open(self.file, 'w').write(self.editor.toPlainText())
         self.changed = False
         # i = self.tabs.currentIndex()
         # self.tabs.setTabText(i, re.sub(r'^\*\s', '', self.tabs.tabText(i)))
         # TODO: how to combine file save and project save

#     __  ___      _
#    /  |/  /___ _(_)___
#   / /|_/ / __ `/ / __ \
#  / /  / / /_/ / / / / /
# /_/  /_/\__,_/_/_/ /_/
class ContentStack(QWidget):
   def __init__(self, core):
      super(ContentStack, self).__init__()
      self.core = core

      hbox = QHBoxLayout()
      hbox.setContentsMargins(0,0,0,0)
      self.setLayout(hbox)

      self.hsplitter = QSplitter(QtCore.Qt.Horizontal)

      self.summary = Summary(self)
      # TODO: detect external changes (file changed or new file)
      self.hsplitter.addWidget(self.summary)

      self.editor = MarkdownEditor(self)
      self.hsplitter.addWidget(self.editor)

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
