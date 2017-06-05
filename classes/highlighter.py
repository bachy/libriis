#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author: Bachir Soussi Chiadmi <bach>
# @Date:   02-06-2017
# @Email:  bachir@figureslibres.io
# @Filename: highlighter.py
# @Last modified by:   bach
# @Last modified time: 03-06-2017
# @License: GPL-V3

# based on code from :
# Copyright (C) 2008 Christophe Kibleur <kib2@free.fr>


import sys
import re
# from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from pygments import highlight
from pygments.lexers import *
from pygments.formatter import Formatter
from pygments.styles import get_all_styles, get_style_by_name
# import time


def hex2QColor(c):
   r=int(c[0:2],16)
   g=int(c[2:4],16)
   b=int(c[4:6],16)
   return QColor(r,g,b)


class QFormatter(Formatter):
   def __init__(self, linenos=True, style="default"): #, style
      Formatter.__init__(self)
      self.data=[]
      self.style = get_style_by_name(style)
      # self.linenos = linenos

      # styles = list(get_all_styles())
      # print(styles)

      # Create a dictionary of text styles, indexed
      # by pygments token names, containing QTextCharFormat
      # instances according to pygments' description
      # of each style

      self.styles={}
      for token, style in self.style:
         qtf=QTextCharFormat()

         if style['color']:
            qtf.setForeground(hex2QColor(style['color']))
         if style['bgcolor']:
            qtf.setBackground(hex2QColor(style['bgcolor']))
         if style['bold']:
            qtf.setFontWeight(QFont.Bold)
         if style['italic']:
            qtf.setFontItalic(True)
         if style['underline']:
            qtf.setFontUnderline(True)

         self.styles[str(token)]=qtf

   def format(self, tokensource, outfile):
      global styles
      # We ignore outfile, keep output in a buffer
      self.data=[]

      # Just store a list of styles, one for each character
      # in the input. Obviously a smarter thing with
      # offsets and lengths is a good idea!
      print(tokensource)

      for ttype, value in tokensource:
         l=len(value)
         t=str(ttype)
         self.data.extend([self.styles[t],]*l)


class Highlighter(QSyntaxHighlighter):

   def __init__(self, parent, mode):
      QSyntaxHighlighter.__init__(self, parent)
      # self.tstamp=time.time()

      # Keep the formatter and lexer, initializing them
      # may be costly.
      if not mode == "md":
         self.formatter=QFormatter(linenos=True, style="monokai-hcb")
      else:
         self.formatter=QFormatter(linenos=False, style="github")

      self.lexer=get_lexer_by_name(mode)

   def highlightBlock(self, text):
      """Takes a block, applies format to the document.
      according to what's in it.
      """

      # I need to know where in the document we are,
      # because our formatting info is global to
      # the document
      cb = self.currentBlock()
      p = cb.position()

      # The \n is not really needed, but sometimes
      # you are in an empty last block, so your position is
      # **after** the end of the document.
      text=str(self.document().toPlainText())+'\n'

      # Yes, re-highlight the whole document.
      # There **must** be some optimizacion possibilities
      # but it seems fast enough.
      highlight(text,self.lexer,self.formatter)

      # Just apply the formatting to this block.
      # For titles, it may be necessary to backtrack
      # and format a couple of blocks **earlier**.
      for i in range(len(str(text))):
         try:
            self.setFormat(i,1,self.formatter.data[p+i])
         except IndexError:
            pass

      # I may need to do something about this being called
      # too quickly.
      # self.tstamp=time.time()
