#!/usr/bin/python
# -*- coding: iso8859-1 -*-

from config import *


def weekday2date(weekday, mode):
  """Returns a datetime object for the
     for the next weekday, that follows today.
     wd is isoweekday (sunday=0)"""
  import datetime
  tmp =datetime.datetime.now()
  w = tmp.isoweekday()
  if( w == 7):
    w = 0
  delta = weekday - w
  if (delta < 0 and mode > 0):
    delta = delta + 7
  elif (delta > 0 and mode < 0):
    delta = delta - 7
  elif (mode == 0):
    if (delta > 3):
      delta = delta - 7
    elif (delta < -3):
      delta = delta + 7

  #D: print 'wd,tday,delta: %s,%s,%s' %(weekday,w,delta)
  tmp = tmp +datetime.timedelta(days=delta)

  return tmp


def media_file_list(dir):
  import os,re
  all_files =  os.listdir(dir)
  file_list = []
  regex = ('.*[.]')
  mf = map(lambda x: x+'$', media_formats)
  regex = regex + '|'.join(mf)
  #D: print regex
  sufix = re.compile(regex)
  def do_it (x):
    if(sufix.search(x) != None): 
      return True
    return False
  file_list = filter(do_it , all_files)

  #for file in all_files:
  #    if (sufix.search(file) != None):
  #        #print file
  #        file_list.append(file)
  return file_list

def file_exists(file):
  from os import F_OK,R_OK,W_OK,X_OK
  import os
  tmp = os.access(file, F_OK)
  return tmp


