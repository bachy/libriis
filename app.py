#!/usr/bin/python
# -*- coding: utf-8 -*-


# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   23-05-2017
# @Email:  bachir@figureslibres.io
# @Last modified by:   bach
# @Last modified time: 21-04-2017
# @License: GPL-V3

import sys

from socket import socket
import socketserver
import http.server
import threading

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QUrl
from PyQt5.QtWidgets import (QAction, QApplication, QLineEdit, QMainWindow, QSizePolicy, QStyle, QTextEdit)
from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKitWidgets import QWebPage, QWebView

# find free port
sock = socket()
sock.bind(('', 0))
PORT = sock.getsockname()[1]
sock.close()
# PORT = 8000
# web werver
# Handler = http.server.SimpleHTTPRequestHandler
# httpd = socketserver.TCPServer(("", PORT), Handler)
# httpd.serve_forever()
httpd = http.server.HTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler)
thread = threading.Thread(target=httpd.serve_forever)
thread.start()
print("serving at port", PORT)


# QT webkit
app = QApplication(sys.argv)

browser = QWebView()
# browser.settings().setAttribute(QWebSettings.PluginsEnabled, True)
browser.load(QUrl('http://localhost:'+str(PORT)))
browser.show()

sys.exit(app.exec_())
