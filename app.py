#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys
from PyQt5.QtWidgets import QApplication

from classes import core, mainwindow

def main():
   app = QApplication(sys.argv)
   app.setOrganizationName('figli')
   app.setApplicationName('Cascade')
   mainappcore = core.Core()
   mainappwindow = mainwindow.MainWindow(mainappcore)
   mainappcore.mainwindow = mainappwindow
   sys.exit(app.exec_())

if __name__ == "__main__":
   main()
