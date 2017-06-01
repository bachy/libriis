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

      self.formGroupBox = QGroupBox("Form layout")
      layout = QFormLayout()

      layout.addRow(QLabel("Page"))
      self.pw = QLineEdit(str(ds['pw']))
      self.pw.setFixedWidth(60)
      self.pw.setValidator(QIntValidator())
      self.pw.setMaxLength(5)
      layout.addRow(QLabel("Page Width (mm):"), self.pw)
      self.ph = QLineEdit(str(ds['ph']))
      self.ph.setFixedWidth(60)
      self.ph.setValidator(QIntValidator())
      self.ph.setMaxLength(5)
      layout.addRow(QLabel("Page Height (mm):"), self.ph)
      #
      line1 = QFrame()
      line1.setFrameShape(QFrame.HLine)
      line1.setFrameShadow(QFrame.Sunken)
      layout.addRow(line1)
      #
      self.mt = QLineEdit(str(ds['mt']))
      self.mt.setFixedWidth(60)
      self.mt.setValidator(QIntValidator())
      self.mt.setMaxLength(3)
      layout.addRow(QLabel("Margin Top (mm):"), self.mt)
      self.mb = QLineEdit(str(ds['mb']))
      self.mb.setFixedWidth(60)
      self.mb.setValidator(QIntValidator())
      self.mb.setMaxLength(3)
      layout.addRow(QLabel("Margin Bottom (mm):"), self.mb)
      self.mi = QLineEdit(str(ds['mi']))
      self.mi.setFixedWidth(60)
      self.mi.setValidator(QIntValidator())
      self.mi.setMaxLength(3)
      layout.addRow(QLabel("Margin inner (mm):"), self.mi)
      self.me = QLineEdit(str(ds['me']))
      self.me.setFixedWidth(60)
      self.me.setValidator(QIntValidator())
      self.me.setMaxLength(3)
      layout.addRow(QLabel("Margin external (mm):"), self.me)
      #
      line2 = QFrame()
      line2.setFrameShape(QFrame.HLine)
      line2.setFrameShadow(QFrame.Sunken)
      layout.addRow(line2)
      #
      self.cs = QLineEdit(str(ds['cs']))
      self.cs.setFixedWidth(60)
      self.cs.setValidator(QIntValidator())
      self.cs.setMaxLength(3)
      layout.addRow(QLabel("Crop size (mm):"), self.cs)
      self.bs = QLineEdit(str(ds['bs']))
      self.bs.setFixedWidth(60)
      self.bs.setValidator(QIntValidator())
      self.bs.setMaxLength(3)
      layout.addRow(QLabel("Bleed size (mm):"), self.bs)
      # # layout.addRow(QLabel("Country:"), QComboBox())
      # layout.addRow(QLabel("Age:"), QSpinBox())

      self.formGroupBox.setLayout(layout)
