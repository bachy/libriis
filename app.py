#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys, os

from socket import socket
import socketserver
import http.server
import threading

from PyQt5.QtCore import QUrl, QFileSystemWatcher
from PyQt5.QtWidgets import (QAction, QApplication, QLineEdit, QMainWindow, QSizePolicy, QStyle, QTextEdit)
from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKitWidgets import QWebPage, QWebView

import sass


class Server():

   def __init__(self, parent=None):

      # find free port
      sock = socket()
      sock.bind(('', 0))

      self._port = sock.getsockname()[1]
      sock.close()

      self.httpd = http.server.HTTPServer(('', self.port), http.server.SimpleHTTPRequestHandler)
      self.thread = threading.Thread(target=self.httpd.serve_forever)
      self.thread.start()
      print("serving at port", self._port)


   @property
   def port(self):
        return self._port


class Compiler():
   def __init__(self,parent=None):
      paths = [
         'assets',
         'assets/scss',
         'assets/scss/styles.scss'
      ]
      self.fs_watcher = QFileSystemWatcher(paths)
      self.fs_watcher.directoryChanged.connect(self.directory_changed)
      self.fs_watcher.fileChanged.connect(self.compile_scss)
      # self.compile_scss()


   def directory_changed(path):
      print("Directory changed : %s" % path)

   def compile_scss(path = ""):
      print("compiling sass : %s" % path)
      # src = open( 'assets/scss/main.scss' ).read()
      scss = sass.compile_file(b'assets/scss/main.scss')
      with open('assets/scss/main.css', 'w') as fp:
         fp.write(scss.decode('utf8'))


class WebkitView(QWebView):
   def __init__(self, port):
      self.port = port
      # QT webkit
      self.view = QWebView.__init__(self)
      # browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)

      self.load(QUrl('http://localhost:'+str(self.port)))
      # self.show()


# class MainWindow():
#    def __init__(self, )

def main():
   # app = QtCore.QCoreApplication(sys.argv)
   app = QApplication(sys.argv)

   server = Server()
   compiler = Compiler()
   webkitview = WebkitView(server.port)
   webkitview.show()


   # sys.exit(app.exec_())
   app.exec_()

if __name__ == "__main__":
   main()
