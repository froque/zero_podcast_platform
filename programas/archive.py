#! /usr/bin/env python
# -*- coding: iso8859-1 -*-


from config import *
from zero_aux import *
import programs

import datetime

class Archive:
    programs = []
    def __init__(self):
        # archive_***** definido em config.py        
        self.dir   = archive_path  #directoria base
        self.data  = archive_data  #directoria do arquivo
        self.share = archive_share #directoria do podcast
        self.preshare = share_pre
    
    def load_archive(self, config):
        self.load_programs(config)
        
    def load_programs (self, config):        
        try:
            f = open (config)
        except IOError:            
            return {'err': 'O ficheiro de configuração \
                do arquivo não encontrado'}

        for line in f:
            s = line.split(',')           
            #D: print s

            #tmp = programs.Program(s[0],s[1])
            tmp = programs.Program()
            tmp.name_prefix = s[0].strip()
            tmp.name_prefix = s[0].strip('" ')
            #print tmp.name_prefix
            #tmp.name_prefix = line.strip()
            tmp.podcast_prefix = s[7].strip(' "\n')
            #print tmp.podcast_prefix
            
            #D: print tmp.podcast_prefix
            import time
            
            tm = next_wd(0, int(s[3]), 1)            
            sd= "%s:%s %i/%i/%i" % (s[3],s[4], tm.day,tm.month, tm.year)            
            #D: print sd
            tmp.first = datetime.datetime(*time.strptime("%s:%s %i/%i/%i" % (s[3],s[4], tm.day,tm.month, tm.year), "%w:%H:%M %d/%m/%Y")[0:5])
            now = datetime.datetime.now()
            if (tmp.first < now):
              tmp.first = tmp.first + datetime.timedelta(weeks=1)
            tm = next_wd(0, int(s[5]), 0)
            sd= "%s:%s %i/%i/%i" % (s[5],s[6], tm.day,tm.month, tm.year)
            tmp.last = datetime.datetime(*time.strptime(sd, "%w:%H:%M %d/%m/%Y")[0:5])
            dt = tmp.last - now
            if( abs(dt.days) > 7):
              tmp.last = tmp.last - datetime.timedelta(days=7)


            self.programs.append (tmp)
            
        f.close()
        return None
      
    def get_waiting(self, program):
      import os,string
      allfiles = []
      files = []
      allfiles=os.listdir(self.preshare)
      
      regex = "^%s.*" % program.podcast_prefix

      for i in xrange(len(allfiles)):
        if(re.search(regex, allfiles[i]) != None):
          files.append(allfiles[i])   
      files.sort(key=string.lower)
      files.reverse()
      return files

    def get_archived(self,program):      
      import string
      files = [] 
      allfiles=[]
      allfiles = media_file_list(self.data)

      for i in xrange(len(allfiles)):
          regex = "^%s.*" % program.podcast_prefix
          if(re.search(regex, allfiles[i]) != None):
            files.append(allfiles[i])
      files.sort(key=string.lower)
      files.reverse()
      return files

    def get_public(self,program):
      import string
      files = [] 
      allfiles=[]
      allfiles = media_file_list(self.share)

      for i in xrange(len(allfiles)):
          regex = "^%s.*" % program.podcast_prefix
          if(re.search(regex, allfiles[i]) != None):
            files.append(allfiles[i])
      files.sort(key=string.lower)
      files.reverse()
      return files


    def search_by_name(self, name):
      #D: print "programas:",programs    
      for i in self.programs:
        #D: print '|%s|%s|'%(i.name_prefix, name)
        if (str(i.name_prefix) == name):
                return i
      return False


            

