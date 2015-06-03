#! /usr/bin/python
# -*- coding: iso8859-1 -*-

import re,os,datetime

from Archive import Archive
from Show import Show
from config import *
from aux import *


class File:
  path = ''
  atime = None
  def __init__(self, path=''):
    if file_exists(path):
      self.path=path
      stats = os.stat(path)
      self.atime = datetime.datetime.fromtimestamp(stats.st_mtime)
    else:
      self.path='err'
    return

class SchedLog:
  ltime = None
  type = ''
  msg = ''
  def __init__(self, ltime=None, type='',msg=''):
    self.ltime=ltime
    self.type=type
    self.msg=msg
    return



class SchedFile(File):
  played = None
  link = ''
  def __init__(self,file,played=None,link=''):
    File.__init__(self, path=file.path)
    self.link = link
    self.played = played
    return


class SchedShow(Show):
  def __init__(self, show,first=None,last=None, log=[]):
    Show.__init__(self,
        bprefix=show.bcast_prefix,
        pprefix=show.podcast_prefix,
        live=show.live,
        length=show.length,
        first=show.first,
        last=show.last
        )
    self.files={'pbcast': first,'bcast': last}
    self.log=log
    return

  def nth_broadcast(self,n):
    N = len(self.log)
    if(N>0):
      if(n>0 and n<N) or (n<0 and n>=-N):
        return self.log[n]
    return  SchedLog()



  def check_status(self,bcast=2):
    """checks the status of the schedule for the
    current Show
    returns:"""

    linkA = self.files['pbcast'].link.split('/')
    pathA = self.files['pbcast'].path.split('/')

    linkB = self.files['bcast'].link.split('/')
    pathB = self.files['bcast'].path.split('/')

    if(len(self.log) != 0):
      msg = self.nth_broadcast(-1).msg
      pathP = msg.split(':')
      log = True
    else:
      pathP = ['']
      log = False

    now = datetime.datetime.now()
    if self.live and bcast == 1:
      link = ''
      relpath = '.'
      value= 10
    elif self.live and bcast ==2:
      relpath = linkB[-2]
      link = linkB[-1]
      if(link == ''): #There's no file in bcast: red alert
        value = -1
      elif(pathB[-1] != pathP[-1] and log): #new live las
        value = 1
      elif(pathB[-1] == pathP[-1] and log): #repetion?
        value = 2
      elif(not(log)):
        value = 1 #there's no history
      else:
        value = 2 #it sounds like repetition 
    elif(self.last < self.first and not(self.live) and bcast==1): #last is coming first so we need to chek pbcast
        relpath = linkA[-2]
        link = linkA[-1]
        if(pathB[-1] == 'err'):#There's no file in bcast: red alert
          #print [self.bcast_prefix, pathB]
          value = -1
        elif(link == ''): #There's no file in pbcast orange alert
          value = -2
        elif(pathA[-1] != pathP[-1] and log ): #good
          value = 0
        elif(not(log)):
          value = 1 #there's no history
        else:
          value = 2 #it sounds like repetition
    else:
      relpath = linkB[-2]
      link = linkB[-1]
      if(link == ''): #There's no file in bcast: red alert
        value = -1
      elif(pathB[-1] != pathP[-1] and bcast==1 and log ): #good 1st bcast
          value = 0
      elif(pathB[-1] == pathP[-1] and bcast==2\
          and now <= self.last and log): #good last bcast
        value = 0
      elif(pathB[-1] != pathP[-1] and bcast==2\
          and now > self.last and log): #good last bcast
        value = 0
      elif(pathB[-1] != pathP[-1] and bcast==2\
          and log and now < self.last): #strange last bcast
        value = 20
      elif(not(log)):
        value = 1 #there's no history
      else:
        value = 2 #it sounds like repetition
    return {'value':value,'link':link,'relpath':relpath}














class Schedule:
  bcast=''
  pbcast=''
  archive=None
  def __init__(self,bcast=sched,pbcast=presched,archive=None):
    self.bcast = bcast
    self.pbcast = pbcast
    if isinstance(archive, Archive):
      self.archive=archive
    else:
      self.archive=Archive()

  def next_show_files(self, show):
    """Receives a Show instance and
    returns a filled SchedShow instance """
    import os
    from os.path import islink,isfile
    
    
    regex = '^%s[.]*' % show.bcast_prefix
    sufix = re.compile(regex)
    def ffilter(x):
      if(sufix.search(x) != None):
        return True
      return False
    
    def do_path(x):
      if show.first < show.last:
        return self.bcast + '/' + x
      return self.pbcast + '/' + x

    files = media_file_list(self.pbcast)
    files = filter(ffilter, files)
    lst = map(do_path, files)

    if len(lst) != 1:
      link = self.pbcast + '/'
      first = SchedFile(file=File('err'), link=link)
    else:
      if( islink(lst[0]) and isfile(lst[0])):
        fname = os.readlink(lst[0])
        ft = File(fname)
        link =  lst[0]
        first = SchedFile(file=ft, link=link)
      else:
        link = self.pbcast + '/'
        first = SchedFile(file=File('err'), link=link)

    files = media_file_list(self.bcast)
    files = filter(ffilter, files)
    lst = map(lambda x:self.bcast + '/' + x, files)
    if len(lst) != 1:
      link = self.bcast + '/'
      last = SchedFile(file=File(), link=link)
    else:
      if( islink(lst[0]) and isfile(lst[0])):
        fname = os.readlink(lst[0])
        ft = File(fname)
        link = lst[0]
        last = SchedFile(file=ft, link=link)
      else:
        link = self.bcast + '/'
        first = SchedFile(file=File('err'), link=link)

    return SchedShow(show, first=first, last=last)

  def load_log(self, show, n=5):
    """Receives a SchedShow instance and
    returns it filled with the last n lines ,
    of the info in the 'bcast/bcast_prefix.log' file"""

    path = self.bcast + '/.' + show.bcast_prefix + '.log'
    #print path
    try:
      f = open(path, 'r')
    except  IOError:
      #print IOError
      show.log = []
      return
    Log = []
    for line in f:
      l = line.split(':')
      ds = l[0].split('-')
      ds = map(lambda x: int(x),ds)
      #print l,ds
      dt = datetime.datetime(year=ds[0], month=ds[1], day=ds[2],
          hour=0,minute=0,second=0,microsecond=0)
      Log.append(SchedLog(ltime=dt, type=l[1],msg=l[2].strip(' \n')))
      #print ['i',Log[-1].msg]
      if(n>0 and len(Log) > n):
        Log.pop(0)
    f.close()
    show.log = Log
    #print Log
    #print show.log
    return





