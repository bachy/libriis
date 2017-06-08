#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

from __future__ import absolute_import, print_function, division, unicode_literals

import sys, os
from PyQt5.QtWidgets import QApplication

from .classes import (core, mainwindow)

def main():
   app = QApplication(sys.argv)
   app.setOrganizationName('figli')
   app.setApplicationName('Cascade')
   app.path = os.path.dirname(os.path.abspath(__file__))
   mainappcore = core.Core(app.path)
   mainappwindow = mainwindow.MainWindow(mainappcore)
   mainappcore.mainwindow = mainappwindow
   sys.exit(app.exec_())

# if __name__ == "__main__":
#    main()
