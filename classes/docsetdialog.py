#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import os
# from PyQt5.QtCore import
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QGroupBox, QDialogButtonBox, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox

class DocsetDialog(QDialog):
   def __init__(self, parent):
      super(DocsetDialog, self).__init__(parent)

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
      self.formGroupBox = QGroupBox("Form layout")
      layout = QFormLayout()

      pw = QLineEdit(str(210))
      pw.setValidator(QIntValidator())
      pw.setMaxLength(5)
      layout.addRow(QLabel("Page Width (mm):"), pw)

      ph = QLineEdit(str(297))
      ph.setValidator(QIntValidator())
      ph.setMaxLength(5)
      layout.addRow(QLabel("Page Height (mm):"), ph)
      #
      mt = QLineEdit(str(15))
      mt.setValidator(QIntValidator())
      mt.setMaxLength(3)
      layout.addRow(QLabel("Margin Top (mm):"), mt)
      mb = QLineEdit(str(15))
      mb.setValidator(QIntValidator())
      mb.setMaxLength(3)
      layout.addRow(QLabel("Margin Bottom (mm):"), mb)
      mi = QLineEdit(str(15))
      mi.setValidator(QIntValidator())
      mi.setMaxLength(3)
      layout.addRow(QLabel("Margin inner (mm):"), mi)
      me = QLineEdit(str(10))
      me.setValidator(QIntValidator())
      me.setMaxLength(3)
      layout.addRow(QLabel("Margin external (mm):"), me)
      #
      cs = QLineEdit(str(5))
      cs.setValidator(QIntValidator())
      cs.setMaxLength(3)
      layout.addRow(QLabel("Crop size (mm):"), cs)
      bs = QLineEdit(str(5))
      bs.setValidator(QIntValidator())
      bs.setMaxLength(3)
      layout.addRow(QLabel("Bleed size (mm):"), bs)
      # # layout.addRow(QLabel("Country:"), QComboBox())
      # layout.addRow(QLabel("Age:"), QSpinBox())

      self.formGroupBox.setLayout(layout)
