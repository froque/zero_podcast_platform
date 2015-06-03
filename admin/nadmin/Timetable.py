#!/usr/bin/python
# -*- coding: iso8859-1 -*-


import datetime
from Archive import Archive
from Schedule import Schedule
import Radio

class Timeslot:
  bcast=-1
  show=None
  file=None
  def __init__(self,bcast=-1,
      show = None, file=None):
    self.bcast=bcast
    self.show=show
    self.file=file
    
  def get_date(self):
    if (self.show != None and self.bcast >0):
      if(self.bcast == 1):
        return self.show.first
      elif(self.bcast == 2):
        return self.show.last
    return None



class TimeslotW:
  bcast_time = None
  week = None
  def __init__(self, tm=None, week=dict()):
    self.bcast_time = tm
    self.week = week
    return



class Timetable:
  def __init__(self, config=None):
    self.archive = Archive()
    self.schedule = Schedule(archive=self.archive)
    self.now = datetime.datetime.now()
    self.sorted=[]
    self.timetable=[]
    self.timecol = []
    self.timeW = []
    if isinstance(config, Radio.Radio):
      self.config = config
    else:
      self.config = None
    return

  def nsort(self):
    """Sorts in the first to come on top
    """
    if self.config == None:
      print 'err: rad'
      return None
    if len(self.sorted) != 0:
      del self.sorted
      self.sorted = []

    N = len(self.config.shows)
    if N == 0:
      return None
    for i in xrange(N):
      t1 = self.config.shows[i]
      n = len(self.sorted)
      if(n == 0): t2= datetime.datetime(day=1,month=1,year=1900)
      else:t2 = self.sorted[0].get_date()
      j=0
      while(j <= (n-1) and  t2 < t1.first):
          j = j + 1
          if(j>=n): break #little hack to jump the n=1 problem
          t2 = self.sorted[j].get_date()
      tmp = Timeslot (show=t1, bcast=1)
      self.sorted.insert(j, tmp)
      
      n = len(self.sorted);j=0
      if(n < 1): t2= datetime.datetime(day=1,month=1,year=1900)
      else:t2 = self.sorted[0].get_date()
      
      while(j <= (n-1) and  t2 < t1.last):
          j = j + 1
          if(j>=n): break
          t2 = self.sorted[j].get_date()
      tmp = Timeslot (show=t1, bcast=2)
      if(t1.last != t1.first):
        self.sorted.insert(j, tmp)
      
    return

  def do_timecol(self):
    for i in self.sorted:
      d1 = i.get_date()
      df = d1 + datetime.timedelta(minutes=i.show.length)
      t1 = d1.time()
      tf = df.time()
      for j in xrange(len(self.timecol)):
        t2 = self.timecol[j]
        if( t2 == t1):
          self.timecol.pop(j)
          break
      self.timecol.append(t1)
      for j in xrange(len(self.timecol)):
        t2 = self.timecol[j]
        if( t2 == tf):
          self.timecol.pop(j)
          break
      self.timecol.append(t1)
    self.timecol.sort()
    return

  def do_timetable(self):
   self.nsort()
   self.do_timecol()

   week=dict()
   for j in xrange(7):
    day = []
    for k in self.sorted:
      d1 = k.get_date()
      if d1.weekday() == j:
        day.append(k)
    week[j] = day

   NN=0
   for i in self.timecol:
     line = i.strftime("%H:%m | ")
     for j in xrange(7):
       day = week[j]
       #print day
       pg = ''
       for show in day:
         d1 = show.get_date()
         t1 = d1.time()
         if(t1 == i):
           NN = NN + 1
           pg = show.show.bcast_prefix

       if(len(pg) == 0):
         pg = '-'
       line = line + pg.center(20, ' ') + '|'
     print line
   print NN
   return

  def do_timeW(self):
    def check_ocurrence(what,where):
      for i in where:
        if what.show.bcast_prefix == i.show.bcast_prefix:
          return True
      return False

    self.nsort()
    self.do_timecol()

    for i in self.timecol:
      tmp = TimeslotW (tm=i)
      week = dict()
      for j in xrange(7):
        PG =[]
        for k in self.sorted:
          d1 = k.get_date()
          t1 = d1.time()
          if (d1.weekday() == j and t1 == i):
            if(not(check_ocurrence(k, pg))):
              pg.append(k)
        week[j] = pg
#      print week
      tmp.week = week
      self.timeW.append(tmp)
    return

  def print_timetableW(self):
     N=len(self.timeW)
     i = 0
     while( i<N):
       timeW = self.timeW[i]
       line = timeW.bcast_time.strftime("%H:%M | ")
       for day in xrange(7):
         names = []
         if (not(timeW.week.has_key(day))):
           names.append('-d-')
         else:
           pgList = timeW.week[day]
           for pg in pgList:
             names.append(pg.show.bcast_prefix)
             tmp = self.timeW[i-1]
             tList = tmp.week[day]
#             print day,tmp
             for tpg in tList:
               min = tpg.show.length
               d1 = tpg.get_date()
               d2 = d1 + datetime.timedelta(minutes=min)
               t2 = d2.time()
               if( t2 > timeW.bcast_time):
                 names.append('v')
         if(len(names) == 0):
           line= line + '-'.center(19) + '||'
         else:
           line= line + '|'.join(names).center(19) + '||'
       print line
       i = i + 1
  


  def print_timecol(self):
    for i in self.timecol:
      print i


  def nprint_list(self):
    for i in self.sorted:
      print i.get_date(),i.bcast,i.show.bcast_prefix
    return













class TimetableWeb(Timetable):
 
  def __init__(self, config):
    Timetable.__init__(self,config)


  def do_timecolWeb(self):
    self.timecolWeb= dict()
    for h in range(24):
      tmp = []
      def btime(n,mode):
        dd=n.get_date()
        tt=dd.time()
        df = dd + datetime.timedelta(minutes=n.show.length)
        tf = df.time()
        t0=datetime.time(hour=h,minute=03)
        if(h+1<24):
          t1=datetime.time(hour=h+1,minute=03)
        else:
          t1=datetime.time(hour=0,minute=03)
        #if (h== 23):
        #  print t0,tt,t1

        if(h < 23):
          if(tt >= t0 and tt < t1 and mode == 1):
            return True
          elif(tf >t0 and tf <= t1 and mode == 2):
            return True
          else:
            return False
        else:
          if(tt>= t0 and mode == 1):
            return True
          elif(tf >=t0 and mode == 2):
            return True
        return

        
      for i in self.sorted:
        if(btime(i,1)):
          d1=i.get_date()
          t1=d1.time()
          if(tmp.count(t1) == 0):
            tmp.append(t1)
        #if(btime(i,2)):
        #  d1=i.get_date() + datetime.timedelta(minutes=i.show.length)
        #  t1=d1.time()
        #  if(tmp.count(t1) == 0):
        #    tmp.append(t1)

      tmp.sort()
      self.timecolWeb[h] = tmp
      
    #for i,j in self.timecolWeb.iteritems():
    #  def get_time(x):
    #    d1=x.get_date()
    #    return d1.time()
    #  print i, map(lambda x:x.strftime('%H:%M'),j )

  def do_timeheadWeb(self):
    self.timeheadWeb = dict()
    #tmp =  ['mon','tues','wens','thurs','fri', 'satur', 'sun']
    for d in xrange(7):
      tmp = 0
      for h in self.timecol:
        n=0
        for k in self.sorted:
          d1 = k.get_date()
          t1 = d1.time()
          if(d1.weekday() == d and t1 == h):
            #print n,d,t1, k.show.bcast_prefix
            n = n + 1
        if n > tmp: tmp = n
      #print tmp
      self.timeheadWeb[d] = tmp


  def do_timeW(self):
    def check_ocurrence(what,where):
      for i in where:
        if what.show.bcast_prefix == i.show.bcast_prefix:
          return True
      return False

    self.nsort()
    self.do_timecol()

    for i in self.timecol:
      tmp = TimeslotW (tm=i)
      week = dict()
      for j in xrange(7):
        pg =[]
        for k in self.sorted:
          d1 = k.get_date()
          t1 = d1.time()
          if (d1.weekday() == j and t1 == i):
            if( check_ocurrence(k, pg) == False):
              pg.append(k)
        week[j] = pg
      #print week
      tmp.week = week
      self.timeW.append(tmp)
    return


  def print_timetableW(self):

    def get_style(val,bcast=2):
      styles={-1:'red_alert',
          -2:'orange_alert',
          0:'green_ok',
          1:'yellow_log',
          2:'yellow_rep',
          10:'direct',
          20:'not_rep'}
      if styles.has_key(val):
        return styles[val] + str(bcast)
      return ''
    def small_string(s,MAX=10):
      n = 3
      N = MAX - n
      l = len(s)
      if(l >= MAX):
        r=s[0:MAX]
      else:
        r=s
      return r.ljust(MAX,' ')
    def get_tip(show):
      if(show.bcast == 1):
        return show.show.first.strftime("%d-%m-%Y")
      else:
        return show.show.last.strftime("%d-%m-%Y")

    self.do_timeW()
    self.do_timecolWeb()
    self.do_timeheadWeb()

     
    header={0:'2ª',1:'3ª',2:'4ª',3:'5ª',4:'6ª',5:'Sábado',6:'Domingo'}
    
    #Table header
    print '<table dir="ltr" class="timetable">'
    print '\t<tr>'
    print '\t\t<th> Horas</th>'
    for i in xrange(7):
      print '\t\t<th colspan="%i"> %s</th>' \
          % (self.timeheadWeb[i], header[i])
    print '\t</tr>'


    #TABLE BODY

    for row,hourList in self.timecolWeb.iteritems():
      rowspan = len(hourList)
      for hour in hourList:
        timeW=self.find_timeW_by_time(hour) #TDO: pseudo broadcast hours
        line = timeW.bcast_time.strftime("%H:%M")
        print '\t<tr>'
        print '\t\t<th>%s</th>' % (line)
        for day in xrange(7):
          if (not(timeW.week.has_key(day))):
            print '\t<td>-d-</td>'
          else:
            pgList = timeW.week[day]
            m = self.timeheadWeb[day]
            n = len(pgList)
            if(n == 1 and m > 1):
              sch=self.schedule.next_show_files(pgList[0].show)
              self.schedule.load_log(sch)
              st = sch.check_status(pgList[0].bcast)

              link = './' + st['relpath'] + '/' + st['link']
              style=get_style(st['value'],pgList[0].bcast)
              name = small_string(pgList[0].show.bcast_prefix)
              tip = get_tip(pgList[0])
              print '\t\t<td colspan="%i" class="%s"><a href="%s" class="%s" title="%s">%s</a></td>'% \
                    (m, style, link,style, tip, name)
            elif(n==0 and m>1):
              print '\t\t<td colspan="%i" class="TNA">-</td>' % m
            else:
              for i in xrange(m):
                style='TNA'
                if(i < n):
                  sch=self.schedule.next_show_files(pgList[i].show)
                  self.schedule.load_log(sch)
                  st = sch.check_status(pgList[i].bcast)

                  link = './' + st['relpath'] + '/' + st['link']
                  style= get_style(st['value'], pgList[i].bcast)
                  name = small_string(pgList[i].show.bcast_prefix,8)
                  tip = get_tip(pgList[i]) + " : " + sch.files['bcast'].path.split('/')[-1]

                  print '\t\t<td colspan="1" class="%s"><a href="%s" class="%s" title="%s">%s</a></td>' %\
                      (style, link,style,tip,name)
                else:
                   print '\t\t<td colspan="1" class="%s">-</td>' % style
        print '\t</tr>' 
    print '</table>'
    #print '<h2> list</h2>'
    #self.nprint_list()
    #print '<h2> config</h2>'
    #self.print_config()


  def nprint_list(self):
    print '<ul>'
    for i in self.sorted:
      print '\t<li>', i.get_date(),i.bcast,i.show.bcast_prefix, '</li>'
    print '</ul>'

  def print_config(self):
    def do_it(x):
        print '<li>',x.bcast_prefix
        print '<ul class="config_sublist">'
        print '<li> 1ª Emissao:', x.first,'</li>'
        print '<li> Repetição:', x.last,'</li>'
        print '<li> Directo:', x.live,'</li>'
        print '<li> Duração:', x.length,'</li>'
        print '<li> Nome de Podcast:', x.podcast_prefix,'</li>'
        print '</ul></li>'
        return
    print '<ul class="config_list">'
    map(do_it, self.config.shows)
    print '</ul>'

  def find_timeW_by_time(self, tm):

   for i in self.timeW:
     if tm == i.bcast_time:
       return i
   return False


    





#f='/usr/local/var/archive/etc/grelha.csv'
#A=TimetableWeb(config=f)
#A.nsort()
#A.nprint_list()
#A.do_timecol()
#A.do_timeW()
#A.print_timetableW()






