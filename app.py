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

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QUrl, QFileSystemWatcher
from PyQt5.QtWidgets import (QAction, QApplication, QLineEdit, QMainWindow, QSizePolicy, QStyle, QTextEdit)
from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKitWidgets import QWebPage, QWebView

import sass

_PORT=0

def main():
   server()
   compiler()
   app()

def server():
   # find free port
   sock = socket()
   sock.bind(('', 0))
   global _PORT
   _PORT = sock.getsockname()[1]
   sock.close()
   # PORT = 8000
   # web werver
   # Handler = http.server.SimpleHTTPRequestHandler
   # httpd = socketserver.TCPServer(("", PORT), Handler)
   # httpd.serve_forever()
   httpd = http.server.HTTPServer(('', _PORT), http.server.SimpleHTTPRequestHandler)
   thread = threading.Thread(target=httpd.serve_forever)
   thread.start()
   print("serving at port", _PORT)

def compiler():
   fs_watcher = QFileSystemWatcher(['assets/scss'])
   fs_watcher.directoryChanged.connect(compile_scss)
   compile_scss()

def compile_scss():
   # src = open( 'assets/scss/main.scss' ).read()
   scss = sass.compile_file(b'assets/scss/main.scss')
   with open('assets/scss/main.css', 'w') as fp:
      fp.write(scss.decode('utf8'))


def app():

   # QT webkit
   app = QApplication(sys.argv)

   browser = QWebView()
   # browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)
   global _PORT
   browser.load(QUrl('http://localhost:'+str(_PORT)))
   browser.show()

   sys.exit(app.exec_())

if __name__ == "__main__":
   main()
