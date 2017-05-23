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

# from PyQt5.QtWebKit import QWebView
# from PyQt5.QtGui import QApplication
# from PyQt5.QtCore import QUrl

# web werver
sock = socket()
sock.bind(('', 0))
PORT = sock.getsockname()[1]
print(PORT)
sock.close()
# PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
# QT webkit
# app = QApplication(sys.argv)
# browser = QWebView()
# browser.load(index.html)
# browser.show()

# app.exec_()
