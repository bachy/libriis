#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Filename: design.py
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

import os, re
# sys,
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSettings, QSizeF, Qt
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPlainTextEdit, QShortcut, QPushButton, QCheckBox, QSpinBox, QLabel
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebInspector
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter

from classes import highlighter


#  _       __     __  _    ___
# | |     / /__  / /_| |  / (_)__ _      __
# | | /| / / _ \/ __ \ | / / / _ \ | /| / /
# | |/ |/ /  __/ /_/ / |/ / /  __/ |/ |/ /
# |__/|__/\___/_.___/|___/_/\___/|__/|__/
class WebkitView(QWebView):
   def __init__(self, parent, core):
      self.parent = parent
      self.core = core
      self.port = core.server.port
      self.view = QWebView.__init__(self, parent)
      self.setZoomFactor(1)
      self.loadFinished.connect(self.onLoaded)
      self.load(QUrl('http://localhost:'+str(self.port)))
      self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
      # self.settings().setAttribute(QWebSettings.PluginsEnabled, True)

      self.initPDF()
      # self.mainframe = self.page.mainFrame()
      # print(self.mainframe)

   def onLoaded(self):
      print("WebView : onLoaded")
      self.parent.webviewtoolbar.onRefresh()

   def initPDF(self):
      self.printer = QPrinter(QPrinter.HighResolution)
      self.printer.setFullPage(True)
      # self.printer.setPageMargins(0,0,0,0,QPrinter.Millimeter)
      self.printer.setFontEmbeddingEnabled(True)
      self.printer.setColorMode(QPrinter.Color)
      # TODO: set the page size and orientation from doc settings
      # (need to do doc settings before that)
      # self.printer.setPageSize(QPrinter.A4)
      self.printer.setPaperSize(QSizeF(210, 300), QPrinter.Millimeter)
      # self.printer.setOrientation(QPrinter.Portrait)
      self.printer.setOutputFormat(QPrinter.PdfFormat)
      self.printer.setCreator('Cascade')
      self.printer.setDocName(self.core.projectname)
      self.printer.setOutputFileName(self.core.projectname+".pdf")
      # self.setFixedWidth(1000)

   def ongenPDF(self):
      # QPrinter::Custom
      # dialog = QPrintPreviewDialog(self.printer)
      # dialog.setWindowState(Qt.WindowMaximized)
      # dialog.paintRequested.connect(self.print_)
      # dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
      # dialog.exec()
      # TODO: open a dialogue to ask where to save the pdf
      # TODO: reload webview and wait for it before printing
      # TODO: addd a progress bar
      # self.webview.
      self.print_(self.printer)

   def refresh(self):
      self.initPDF()
      self.reload()

   def toggleDocClass(self, c="",a=True):
      if a :
         togg = "add"
      else :
         togg = "remove"
      command = """document.documentElement.classList."""+togg+"""('"""+c+"""')"""
      self.evaluateJS(command)

   def zoom(self,z):
      self.setZoomFactor(z/100)
      # command = """
      #    var zoomLevel = """+str(z)+""" / 100;
      #    var elt = document.documentElement.querySelector("#pages");
      #    elt.style.webkitTransform = "scale(" + zoomLevel + ")";
      #    elt.style.webkitTransformOrigin = "0 0";
      # """
      # self.evaluateJS(command)

   def changePage(self,p=0):
      command = """
         var pageNumber = """+str(p-1)+""";
         var target = document.documentElement.querySelectorAll('.paper')[pageNumber];
         var offsetTop = target.offsetTop;
         var offsetLeft = target.offsetLeft;
         document.documentElement.querySelector('body').scrollTop = offsetTop;
         document.documentElement.querySelector('body').scrollLeft = offsetLeft;
      """
      self.evaluateJS(command)

   def evaluateJS(self, command):
      self.page().mainFrame().evaluateJavaScript(command)

#     ____                           __
#    /  _/___  _________  ___  _____/ /_____  _____
#    / // __ \/ ___/ __ \/ _ \/ ___/ __/ __ \/ ___/
#  _/ // / / (__  ) /_/ /  __/ /__/ /_/ /_/ / /
# /___/_/ /_/____/ .___/\___/\___/\__/\____/_/
#               /_/
class WebkitInspector(QWebInspector):
   def __init__(self, parent, webkitview):
      super(WebkitInspector, self).__init__(parent)
      self.webkitview = webkitview
      self.setPage(self.webkitview.page())
      self.showMaximized()
      # TODO: webkitinspector is disappearing when chaging tabs

#   ______            ______
#  /_  __/___  ____  / / __ )____ ______
#   / / / __ \/ __ \/ / __  / __ `/ ___/
#  / / / /_/ / /_/ / / /_/ / /_/ / /
# /_/  \____/\____/_/_____/\__,_/_/
class WebViewToolBar(QWidget):
   def __init__(self, parent):
      super(WebViewToolBar, self).__init__(parent)
      self.parent = parent

      font = QFont()
      # font.setFamily("Droid Sans Mono")
      # font.setFixedPitch(True)
      font.setPointSize(8)
      self.setFont(font)

      self.hbox = QHBoxLayout()
      self.hbox.setContentsMargins(0,0,0,0)

      self.preview = QCheckBox('Prev&iew', self)
      self.preview.stateChanged.connect(self.onPreview)
      self.hbox.addWidget(self.preview)

      self.debug = QCheckBox('Deb&ug', self)
      self.debug.stateChanged.connect(self.onDebug)
      self.hbox.addWidget(self.debug)

      self.grid = QCheckBox('&Grid', self)
      self.grid.stateChanged.connect(self.onGrid)
      self.hbox.addWidget(self.grid)

      self.spread = QCheckBox('&Spread', self)
      self.spread.stateChanged.connect(self.onSpread)
      self.hbox.addWidget(self.spread)

      self.facing = QCheckBox('Fa&cing', self)
      self.facing.stateChanged.connect(self.onFacing)
      self.hbox.addWidget(self.facing)
      #
      self.hbox.addStretch()
      #
      # zoom
      self.hbox.addWidget(QLabel("Zoom:"))
      self.zoom = QSpinBox(self)
      self.zoom.setMinimum(-100)
      self.zoom.setMaximum(200)
      self.zoom.setSingleStep(10)
      self.zoom.setValue(90)
      self.zoom.valueChanged.connect(self.onZoomChanged)
      self.hbox.addWidget(self.zoom)

      # page
      self.gotopage = QLabel("Go to Page: /"+str(self.parent.core.docsettings['np']))
      self.hbox.addWidget(self.gotopage)
      self.page = QSpinBox(self)
      self.page.setMinimum(1)
      self.page.setMaximum(int(self.parent.core.docsettings['np']))
      self.page.valueChanged.connect(self.onChangePage)
      self.hbox.addWidget(self.page)

      self.addpage = QPushButton("&Add Page", self)
      self.addpage.clicked.connect(self.onAddPage)
      self.hbox.addWidget(self.addpage)
      self.rmpage = QPushButton("Re&move Page", self)
      self.rmpage.clicked.connect(self.onRmPage)
      self.hbox.addWidget(self.rmpage)

      #
      self.hbox.addStretch()
      #
      self.reload = QPushButton("&Reload", self)
      # self.reload.setShortcut('Ctrl+Shift+r')
      # TODO: how to define same shortcut in different places
      # self.reload.setIcon(Icon(ico)))
      self.reload.clicked.connect(self.onReload)
      self.hbox.addWidget(self.reload)

      self.genpdf = QPushButton("&PDF", self)
      # self.genpdf.setShortcut('Ctrl+Shift+r')
      # TODO: how to define same shortcut in different places
      # self.genpdf.setIcon(Icon(ico)))
      self.genpdf.clicked.connect(self.onGenPDF)
      self.hbox.addWidget(self.genpdf)

      self.setLayout(self.hbox)

   # def onCheckboxAction(self, box):
   #    self.parent.webkitview.toggleDocClass(box, self[box].isChecked())
   #    self.recToolbarState(box, self[box].isChecked())

   def onPreview(self):
      print('Toolbar : onPreview', self.preview.isChecked())
      self.parent.webkitview.toggleDocClass('preview', self.preview.isChecked())
      self.recToolbarState('preview', self.preview.isChecked())

   def onDebug(self):
      self.parent.webkitview.toggleDocClass('debug', self.debug.isChecked())
      self.recToolbarState('debug', self.debug.isChecked())

   def onGrid(self):
      self.parent.webkitview.toggleDocClass('grid', self.grid.isChecked())
      self.recToolbarState('grid', self.grid.isChecked())

   def onSpread(self):
      self.parent.webkitview.toggleDocClass('spread', self.spread.isChecked())
      self.recToolbarState('spread', self.spread.isChecked())

   def onFacing(self):
      self.parent.webkitview.toggleDocClass('facing', self.facing.isChecked())
      self.recToolbarState('facing', self.facing.isChecked())

   def onZoomChanged(self,i):
      # print("onZoomChanged : "+str(i))
      self.parent.webkitview.zoom(i)

   def onZoomOn(self):
      # print("onZoomOn")
      self.zoom.setValue(self.zoom.value()+self.zoom.singleStep())

   def onZoomOut(self):
      # print("onZoomOut")
      self.zoom.setValue(self.zoom.value()-self.zoom.singleStep())

   def onChangePage(self, i):
      # print("onChangePage : "+str(i))
      self.parent.webkitview.changePage(i)

   def onNextPage(self):
      # print('onNextPage')
      self.page.setValue(self.page.value()+self.page.singleStep())

   def onPrevPage(self):
      # print('onPrevPage')
      self.page.setValue(self.page.value()-self.page.singleStep())

   def onAddPage(self):
      # print("onAddPage")
      self.parent.core.addPage()

   def onRmPage(self):
      # print("onAddPage")
      self.parent.core.rmPage()

   def onReload(self):
      # print("onReload")
      self.parent.webkitview.reload()

   def onGenPDF(self):
      print("onGenPDF")
      self.parent.webkitview.ongenPDF()

   def recToolbarState(self, prop, val):
      # print('recToolbarState : '+prop, val)
      settings = QSettings('FiguresLibres', 'Cascade')
      settings.setValue('design/toolbar/'+prop, val)
      # print('recToolbarState after : '+prop, settings.value('design/toolbar/'+prop))

   def onRefresh(self):
      # apply precedent toolbar state
      settings = QSettings('FiguresLibres', 'Cascade')
      self.preview.setChecked(bool(settings.value('design/toolbar/preview', False, type=bool)))
      self.debug.setChecked(bool(settings.value('design/toolbar/debug', False, type=bool)))
      self.grid.setChecked(bool(settings.value('design/toolbar/grid', False, type=bool)))
      self.spread.setChecked(bool(settings.value('design/toolbar/spread', False, type=bool)))
      self.facing.setChecked(bool(settings.value('design/toolbar/facing', False, type=bool)))
      # trigger webview changes
      self.parent.webkitview.toggleDocClass('preview', self.preview.isChecked())
      self.parent.webkitview.toggleDocClass('debug', self.debug.isChecked())
      self.parent.webkitview.toggleDocClass('grid', self.grid.isChecked())
      self.parent.webkitview.toggleDocClass('spread', self.spread.isChecked())

      self.gotopage.setText("Go to Page: /"+str(self.parent.core.docsettings['np']))
      self.page.setMaximum(int(self.parent.core.docsettings['np']))
      self.parent.webkitview.changePage(self.page.value())
#     ______    ___ __
#    / ____/___/ (_) /_____  _____
#   / __/ / __  / / __/ __ \/ ___/
#  / /___/ /_/ / / /_/ /_/ / /
# /_____/\__,_/_/\__/\____/_/
class CodeEditor(QPlainTextEdit):
   def __init__(self, parent, core, tabs, file, mode):
      super(CodeEditor, self).__init__()
      self.parent = parent
      self.core = core
      self.tabs = tabs
      self.file = file
      self.hl= highlighter.Highlighter(self.document(),mode)
      self.setText()
      self.setTabStopWidth(15)

      self.textChanged.connect(self.onTextChanged)

      self.save_shortcut = QShortcut(QKeySequence("Ctrl+s"), self)
      self.save_shortcut.activated.connect(self.save)

   def setText(self):
      # try:
      #    self.textChanged.disconnect(self.onTextChanged)
      # except Exception as e:
      #    print(e)

      self.filepath = os.path.join(self.core.cwd,self.file)
      self.clear()
      self.insertPlainText(open(self.filepath, 'r').read())
      self.changed = False

      font = QFont()
      font.setFamily("Droid Sans Mono")
      font.setFixedPitch(True)
      font.setPointSize(12)
      self.setFont(font)


   def onTextChanged(self):
      print('textChanged')
      # print(self.toPlainText())
      # open(self.filepath, 'w').write(self.toPlainText())
      if not self.changed:
         self.changed = True
         i = self.tabs.currentIndex()
         # self.tabs.setTabText(i, re.sub(r'^\**\s', '', self.tabs.tabText(i)))
         self.tabs.setTabText(i, "* "+self.tabs.tabText(i))
         # TODO: indicate that webview needs to be reloaded

   def save(self):
      if self.changed:
         open(self.filepath, 'w').write(self.toPlainText())
         i = self.tabs.currentIndex()
         self.tabs.setTabText(i, re.sub(r'^\**\s', '', self.tabs.tabText(i)))
         self.parent.reloadView()
         self.changed = False
         # TODO: how to combine file save and project save

class Editor(QWidget):
   def __init__(self, parent):
      super(Editor, self).__init__()
      self.parent = parent

      self.layout = QVBoxLayout(self)
      self.layout.setContentsMargins(0,0,0,0)

      # Initialize tab screen
      self.tabs = QTabWidget()

      self.scsstab = CodeEditor(self, self.parent.core, self.tabs, 'assets/css/styles.scss', "sass")
      self.jstab = CodeEditor(self, self.parent.core, self.tabs, 'assets/js/script.js', 'js')

      # Add tabs
      self.tabs.addTab(self.scsstab,"scss")
      self.tabs.addTab(self.jstab,"js")

      # Add tabs to widget
      self.layout.addWidget(self.tabs)
      self.setLayout(self.layout)

   def refresh(self):
      self.scsstab.setText()
      self.jstab.setText()

   def reloadView(self):
      self.parent.webkitview.reload()

#    _____ __             __
#   / ___// /_____ ______/ /__
#   \__ \/ __/ __ `/ ___/ //_/
#  ___/ / /_/ /_/ / /__/ ,<
# /____/\__/\__,_/\___/_/|_|
class DesignStack(QWidget):
   def __init__(self, core):
      super(DesignStack, self).__init__()
      self.core = core

      # self.grid = QGridLayout()
      self.hbox = QHBoxLayout()
      self.hbox.setContentsMargins(0,0,0,0)
      self.setLayout(self.hbox)


      self.webview = QWidget()
      self.webview.vbox = QVBoxLayout()
      self.webview.setLayout(self.webview.vbox)
      self.webview.vbox.setContentsMargins(0,0,0,0)

      # toolbar
      self.webviewtoolbar = WebViewToolBar(self)
      self.webview.vbox.addWidget(self.webviewtoolbar)

      # webkitview
      self.webkitview = WebkitView(self, core)

      # webkitinspector
      self.webkitinspector = WebkitInspector(self, self.webkitview)

      # V layout
      self.vsplitter = QSplitter(QtCore.Qt.Vertical)
      self.vsplitter.addWidget(self.webkitview)
      self.vsplitter.addWidget(self.webkitinspector)
      self.vsplitter.splitterMoved.connect(self.movedSplitter)

      self.webview.vbox.addWidget(self.vsplitter)

      # H layout
      self.hsplitter = QSplitter(QtCore.Qt.Horizontal)
      self.hsplitter.addWidget(self.webview)

      # editor
      self.editor = Editor(self)
      self.hsplitter.addWidget(self.editor)

      self.hsplitter.splitterMoved.connect(self.movedSplitter)

      self.hbox.addWidget(self.hsplitter)

      self.restorePrefs()

   def toggleInspector(self):
      self.webkitinspector.setVisible(not self.webkitinspector.isVisible())

   def initShortcuts(self):
      # inspector
      shortcut = QShortcut(self)
      shortcut.setKey("F12")
      shortcut.activated.connect(self.toggleInspector)
      self.webkitinspector.setVisible(False)

      # pages
      # self.pagenext_shortcut = QShortcut(QKeySequence(Qt.ControlModifier+Qt.ShiftModifier+Qt.Key_Right), self)
      # self.pagenext_shortcut.activated.connect(self.webviewtoolbar.onNextPage)
      # self.pageprev_shortcut = QShortcut(QKeySequence(Qt.ControlModifier+Qt.ShiftModifier+Qt.Key_Left), self)
      # self.pageprev_shortcut.activated.connect(self.webviewtoolbar.onPrevPage)

      # zoom
      # self.zoomon_shortcut = QShortcut(QKeySequence(Qt.ControlModifier+Qt.Key_Plus), self)
      # self.zoomon_shortcut.activated.connect(self.webviewtoolbar.onZoomOn)
      # self.zoomout_shortcut = QShortcut(QKeySequence(Qt.ControlModifier+Qt.Key_Minus), self)
      # self.zoomout_shortcut.activated.connect(self.webviewtoolbar.onZoomOut)



   def restorePrefs(self):
      settings = QSettings('FiguresLibres', 'Cascade')
      print(settings.value('design/vsplitter/sizes', self.vsplitter.sizes()))
      vals = settings.value('design/vsplitter/sizes', None)
      if vals:
         sizes = []
         for size in vals: sizes.append(int(size))
         self.vsplitter.setSizes(sizes)

      vals = settings.value('design/hsplitter/sizes', None)
      if vals:
         sizes = []
         for size in vals: sizes.append(int(size))
         self.hsplitter.setSizes(sizes)

   def movedSplitter(self):
      settings = QSettings('FiguresLibres', 'Cascade')
      # print(self.vsplitter.sizes())
      settings.setValue('design/vsplitter/sizes', self.vsplitter.sizes())
      settings.setValue('design/hsplitter/sizes', self.hsplitter.sizes())

   def refresh(self):
      self.editor.refresh()
      self.webkitview.refresh()
