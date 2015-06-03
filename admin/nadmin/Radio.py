#!/usr/bin/python
# -*- coding: iso8859-1 -*-

import Show

from aux import *
from config import *

class Radio:
  def __init__(self, config=''):
    self.shows = []
    if len(config) != 0:
      self.load_shows(config)

  def load_shows(self,file):
    """Method that loads the show list from a csv
    config file. «First» field will be filled with
    the next date to broadcast the file. «Last» will be
    filled with the near repetition"""
    import csv
    try:
      table = csv.reader( open(file, 'r'),
          delimiter=',', quoting = csv.QUOTE_MINIMAL)
    except:
      return -1
    
    for row in table:
      s= row
      bprefix = s[0].strip('" ')
      pprefix = s[7].strip(' "\n')
      first = weekday2date(int(s[3]), 1)
      ttime = s[4].split(':')
      first= first.replace(hour=int(ttime[0]),minute=int(ttime[1]),second=0,microsecond=0)

      last  = weekday2date(int(s[5]), 0)
      ttime = s[6].split(':')
      last =last.replace(hour=int(ttime[0]), minute=int(ttime[1]),second=0,microsecond=0)
      
      live = False
      if (int(s[1]) == 1):
          live = True

      tmp = Show.Show(bprefix = bprefix,pprefix = pprefix,
          length = int(s[2]),live = live,
          first=first, last=last)

      self.shows.append(tmp)
    return

  def search_by_name(self, name):
    """returns a Show instance if finds any that
    matches by «bprefix» or None otherwise"""
    for i in self.shows:
      if (i.bcast_prefix == name):
        return i
    return None


  def print_shows(self, item=-1):
    if (item < 0):
      for i in self.shows:
        print i.bcast_prefix,i.podcast_prefix,i.live,i.length,i.first, i.last


  def get_radio_shows(self):
    """ Returns a list with all the prefixes"""

    lst = map(lambda x: x.bcast_prefix, self.shows)
    lst.sort()
    return lst

  def podcast_log(self, fname='podcast.cron',dt=60):
    ''' Creates the podcast cron.Algoritm:
    * for live shows: 2dt after the live broadcast
    * for others: dt after the first broadcast
    '''

    f = open(fname,'w')
    f.write('''
####################################################################
#minute (0-59),                                                    #
#|      hour (0-23),                                               #
#|      |       day of the month (1-31),                           #
#|      |       |       month of the year (1-12),                  #
#|      |       |       |       day of the week (0-6 with 0=Sunday)#
#|      |       |       |       |       commands                   #
####################################################################
''')

    def algorithm(x):
      if(x.live):
        delta = detetime.timedelta(minutes=2*dt)
      else:
        delta = datetime.timedelta(minutes=dt)
      TIME = x.first + delta
      f.write('%2i      %2i      *       *       %1i      %s %s\n'
          %(TIME.minute, TIME.hour, TIME.day, script, x.podcast_prefix))
      return

    map(x, self.shows)
    f.close()
    return



