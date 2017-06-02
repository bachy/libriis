#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import os
# from PyQt5.QtCore import QLine
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QGroupBox, QDialogButtonBox, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox, QFrame

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

      self.setWindowTitle("Doc settings")

   def createFormGroupBox(self):
      ds = self.parent.core.docsettings

      self.formGroupBox = QGroupBox()
      layout = QFormLayout()

      self.pw = FormLineEdit(str(ds['pw']))
      layout.addRow(QLabel("Page Width (mm):"), self.pw)
      self.ph = FormLineEdit(str(ds['ph']))
      layout.addRow(QLabel("Page Height (mm):"), self.ph)
      #
      layout.addRow(Line(self))
      #
      self.mt = FormLineEdit(str(ds['mt']),3)
      layout.addRow(QLabel("Margin Top (mm):"), self.mt)
      self.mb = FormLineEdit(str(ds['mb']),3)
      layout.addRow(QLabel("Margin Bottom (mm):"), self.mb)
      self.mi = FormLineEdit(str(ds['mi']),3)
      layout.addRow(QLabel("Margin inner (mm):"), self.mi)
      self.me = FormLineEdit(str(ds['me']),3)
      layout.addRow(QLabel("Margin external (mm):"), self.me)
      #
      layout.addRow(Line(self))
      #
      self.cs = FormLineEdit(str(ds['cs']),3)
      layout.addRow(QLabel("Crop size (mm):"), self.cs)
      self.bs = FormLineEdit(str(ds['bs']),3)
      layout.addRow(QLabel("Bleed size (mm):"), self.bs)
      #
      layout.addRow(Line(self))
      #
      self.cn = FormLineEdit(str(ds['cn']),2,True)
      layout.addRow(QLabel("Columns number:"), self.cn)
      self.cg = FormLineEdit(str(ds['cg']),2)
      layout.addRow(QLabel("Columns gutters:"), self.cg)
      #
      self.rn = FormLineEdit(str(ds['rn']),2,True)
      layout.addRow(QLabel("Rows number:"), self.rn)
      self.rg = FormLineEdit(str(ds['rg']),2)
      layout.addRow(QLabel("Rows gutters:"), self.rg)
      #
      layout.addRow(Line(self))
      #
      self.lh = FormLineEdit(str(ds['lh']),2,True)
      layout.addRow(QLabel("Line height:"), self.lh)

      self.formGroupBox.setLayout(layout)

class FormLineEdit(QLineEdit):
   def __init__(self, parent, ml=5, int=False, mw=60):
      super(FormLineEdit, self).__init__(parent)
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
