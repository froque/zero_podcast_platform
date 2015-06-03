#!/usr/bin/python
# -*- coding: iso8859-1 -*-


import datetime



class Show:
  bcast_prefix = ''
  podcast_prefix = ''
  live = False
  length = -1
  first = datetime.datetime.now()
  last = first
  def __init__(self,
      bprefix = '',
      pprefix='',
      live=False,
      length=0,
      first = datetime.datetime.now(),
      last = datetime.datetime.now()):
    self.bcast_prefix = bprefix
    self.podcast_prefix = pprefix
    self.live = live
    self.length = length
    self.first = first
    self.last = last
    return








