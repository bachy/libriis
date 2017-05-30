#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os
from socket import socket
import socketserver
import http.server
import threading


class Server():

   def __init__(self, parent):

      self.parent = parent
      # find free port
      sock = socket()
      sock.bind(('', 0))

      self._port = sock.getsockname()[1]
      sock.close()

      # self.initial_cwd = os.getcwd()
      self.thread = threading.Thread(target=self.webserver)
      self.thread.daemon = True
      self.thread.start()
      # os.chdir(self.initial_cwd)

   def webserver(self):
      os.chdir(self.parent.cwd)
      self.httpd = http.server.HTTPServer(('', self.port), http.server.SimpleHTTPRequestHandler)
      self.httpd.serve_forever()
      print("serving at port", self._port)

   @property
   def port(self):
        return self._port

   def reload(self):
      # self.thread.shutdown()
      os.chdir(self.parent.cwd)
      # self.thread.start()
      # os.chdir(self.initial_cwd)
