#!/usr/bin/python
# -*- coding: iso8859-1 -*-


import os,re
import string
from Radio import  Radio
from config import *
from aux import *

class Archive:
  def __init__(self,
      data=archive_data,
      public=archive_share,
      ppublic=share_pre,
      config = None):
    """Archive's constructor. If defined, tries to load
    an csv file with show config"""

    self.data_path = data
    self.public_path = public
    self.public_path_tmp = ppublic
    #if( config != ''):
    #  self.config = Radio.Radio(config=config)
    #else:
    #  self.config = None
    if isinstance(config, Radio):
      self.config = config
    return

  def show_files(self,show):
    """Returns a list with all show files"""

    regex = '^%s*' % show.podcast_prefix
    #print regex
    sufix = re.compile(regex)

    def ffilter(x):
      if(sufix.search(x) != None):
        return True
      return False

    all_files = media_file_list(self.data_path)
    file_list=filter(ffilter, all_files)
    file_list.sort()
    return file_list
  
  def waiting_show_files(self, show):
    """returns a list with all files that are waiting
    to be published in the future"""

    regex = "^%s.*" % show.podcast_prefix
    sufix= re.compile(regex)

    def ffilter(x):
      if(sufix.search(x) != None):
        return True
      return False

    all_files = os.listdir(self.public_path_tmp)
    file_list = filter(ffilter, all_files)

    file_list.sort(key=string.lower)
    file_list.reverse()
    return file_list








class ArchiveWeb(Archive):
  def __init__(self, data=archive_data,public=archive_share,
      ppublic=share_pre,config=None):
    """Class constructor"""
    
    Archive.__init__(self, data=data,public=public,
        ppublic=ppublic,config=config)

    return













