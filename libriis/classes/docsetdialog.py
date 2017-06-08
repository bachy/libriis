#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

from __future__ import absolute_import, print_function, division, unicode_literals

import os
# from PyQt5.QtCore import QLine
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QGroupBox, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox, QFrame

class DocsetDialog(QDialog):
   def __init__(self, parent):
      super(DocsetDialog, self).__init__(parent)
      self.parent = parent
      self.createFormGroupBox()

      buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      buttonBox.accepted.connect(self.accept)
      buttonBox.rejected.connect(self.reject)

      mainLayout = QVBoxLayout()
      mainLayout.addWidget(self.formGroupBox)
      mainLayout.addWidget(buttonBox)
      self.setLayout(mainLayout)

      self.setWindowTitle("Document settings")

   def createFormGroupBox(self):
      ds = self.parent.core.docsettings

      self.formGroupBox = QWidget()
      vbox = QVBoxLayout()
      vbox.setContentsMargins(0,0,0,0)
      self.formGroupBox.setLayout(vbox)

      topGroupBox = QWidget()
      topformlayout = QFormLayout()
      topformlayout.setContentsMargins(0,0,0,0)
      topGroupBox.setLayout(topformlayout)
      vbox.addWidget(topGroupBox)

      colsGroupBox = QWidget()
      hbox = QHBoxLayout()
      hbox.setContentsMargins(0,0,0,0)
      colsGroupBox.setLayout(hbox)
      vbox.addWidget(colsGroupBox)

      leftGroupBox = QGroupBox()
      leftformlayout = QFormLayout()
      # leftformlayout.setContentsMargins(0,0,0,0)
      leftGroupBox.setLayout(leftformlayout)
      hbox.addWidget(leftGroupBox)

      rightGroupBox = QGroupBox()
      rightformlayout = QFormLayout()
      # rightformlayout.setContentsMargins(0,0,0,0)
      rightGroupBox.setLayout(rightformlayout)
      hbox.addWidget(rightGroupBox)

      # headers
      self.headerOdd = QLineEdit(str(ds['ho']))
      topformlayout.addRow(QLabel("Header odd:"), self.headerOdd)
      self.headerEven = QLineEdit(str(ds['he']))
      topformlayout.addRow(QLabel("Header even:"), self.headerEven)

      self.np = NumLineEdit(str(ds['np']),3,True)
      leftformlayout.addRow(QLabel("Numbers of Pages:"), self.np)
      #
      leftformlayout.addRow(Line(self))
      #
      self.pw = NumLineEdit(str(ds['pw']))
      leftformlayout.addRow(QLabel("Page Width (mm):"), self.pw)
      self.ph = NumLineEdit(str(ds['ph']))
      leftformlayout.addRow(QLabel("Page Height (mm):"), self.ph)
      #
      leftformlayout.addRow(Line(self))
      #
      self.mt = NumLineEdit(str(ds['mt']),3)
      leftformlayout.addRow(QLabel("Margin Top (mm):"), self.mt)
      self.mb = NumLineEdit(str(ds['mb']),3)
      leftformlayout.addRow(QLabel("Margin Bottom (mm):"), self.mb)
      self.mi = NumLineEdit(str(ds['mi']),3)
      leftformlayout.addRow(QLabel("Margin inner (mm):"), self.mi)
      self.me = NumLineEdit(str(ds['me']),3)
      leftformlayout.addRow(QLabel("Margin external (mm):"), self.me)

      #
      self.cs = NumLineEdit(str(ds['cs']),3)
      rightformlayout.addRow(QLabel("Crop size (mm):"), self.cs)
      self.bs = NumLineEdit(str(ds['bs']),3)
      rightformlayout.addRow(QLabel("Bleed size (mm):"), self.bs)
      #
      rightformlayout.addRow(Line(self))
      #
      self.cn = NumLineEdit(str(ds['cn']),2,True)
      rightformlayout.addRow(QLabel("Columns number:"), self.cn)
      self.cg = NumLineEdit(str(ds['cg']),2)
      rightformlayout.addRow(QLabel("Columns gutters:"), self.cg)
      #
      self.rn = NumLineEdit(str(ds['rn']),2,True)
      rightformlayout.addRow(QLabel("Rows number:"), self.rn)
      self.rg = NumLineEdit(str(ds['rg']),2)
      rightformlayout.addRow(QLabel("Rows gutters:"), self.rg)
      #
      rightformlayout.addRow(Line(self))
      #
      self.lh = NumLineEdit(str(ds['lh']),2,True)
      rightformlayout.addRow(QLabel("Line height:"), self.lh)

      # self.formGroupBox.setLayout(layout)

class NumLineEdit(QLineEdit):
   def __init__(self, parent, ml=5, int=False, mw=60):
      super(NumLineEdit, self).__init__(parent)
      self.setFixedWidth(mw)
      self.setMaxLength(ml)
      if int:
         self.setValidator(QIntValidator())
      else:
         # TODO: set float validator
         self.setValidator(QIntValidator())

class Line(QFrame):
   def __init__(self, parent):
      super(Line, self).__init__(parent)
      self.setFrameShape(QFrame.HLine)
      self.setFrameShadow(QFrame.Sunken)
