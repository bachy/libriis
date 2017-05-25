#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os

from socket import socket

import socketserver
import http.server
import threading


class Server():

   def __init__(self, parent=None):

      # find free port
      sock = socket()
      sock.bind(('', 0))

      self._port = sock.getsockname()[1]
      sock.close()

      self.httpd = http.server.HTTPServer(('', self.port), http.server.SimpleHTTPRequestHandler)
      self.thread = threading.Thread(target=self.httpd.serve_forever)
      self.thread.daemon = True
      self.thread.start()
      print("serving at port", self._port)


   @property
   def port(self):
        return self._port
