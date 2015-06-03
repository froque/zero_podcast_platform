#!/usr/bin/python
# -*- coding: iso8859-1 -*-


import profile
import cgi
from cgi import *
import cgitb; cgitb.enable()
import os
from config import *

from Radio import Radio
from Archive import Archive
from Schedule import Schedule
from Timetable import TimetableWeb


class RadioWebApp:
  form=None
  profile=''
  file=''
  schedule=None
  archive=None
  config=None
  timetable=None
  def __init__(self, form, file='',
      sched=None,arch=None,config=None):
    if len(file)  > 0:
      if os.path.isfile(file):
        self.file=file
    self.form=form
    self.schedule=sched
    self.archive=arch
    self.config=config
    self.get_profile()
    return

  def get_profile(self):
    env = os.environ
    self.state=dict()
    self.state['operation']=''
    if env.has_key('PATH_INFO'):
      self.url_state = env['PATH_INFO']
      ls = self.url_state.split('/')
      if len(ls) > 1:
        self.state['operation']=ls[1]
      else:
        self.state['operation']=''
      if len(ls) > 2:
       self.state['show']=ls[2]
      else:
       self.state['show']=''

    if env.has_key('REMOTE_USER'):
      user = env['REMOTE_USER']
    else:
      user = ''
    if user == 'riist' or user == 'radiologo':
     self.profile = 'author'
    if user == 'programacao':
      self.profile = 'broadcaster'
    return

  def run_operation(self):
    if self.state['operation'] == 'broadcast':
      self.broadcast_view()
    elif self.state['operation'] == 'archive':
      self.archive_view()
    else:
      self.default_page()
    return


  def load_radio_config(self,config):
   if isinstance(config, Radio):
      self.config=config
      return
   self.config = None
   return

  def load_archive(self,arch):
    if isinstance(arch,Archive):
      self.archive = arch
      return
    self.archive = None
    return

  def load_schedule(self, sched):
    if isinstance(sched, Schedule):
      self.schedule=sched
      return
    self.schedule=None
    return

  def load_timetable(self, tt):
    if isinstance(tt, TimetableWeb):
      self.timetable = tt
      return
    self.timetable = None
    return

  def archive_url(self):
    path=self.archive.data_path.split('/')
    return '/nadmin/' + '/'.join([path[-2],path[-1]])


  def html_header(self):
    print "Content-type: text/html; charset='iso-8859-1'\n"
    print "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN'\
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>"
    print "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>"
    print "<head>"
    print "<title>Rádio Zero</title>"
    print "<link href='%s/estilo_site.css' rel='stylesheet' type='text/css' />" %  resources_dir
    print "<link href='%s/broadcast.css' rel='stylesheet' type='text/css' />" % resources_dir 
    print "<link rel='icon' href='%s/favicon.ico' />" %  resources_dir
    print "</head>"
    print '<body>'
    return

  def html_footer(self):
    print '<div id="footer">'
    print '<hr />'
    print '</div>'
    print '</body></html>'
    return

  def html_error(self, error='Erro não identificado'):
    print '<h1>Erro!</h1>\n<h2>%s</h2>' % error
    return









  def archive_view(self):
    self.html_header()
    radio = Radio(self.file)
    self.load_radio_config(radio)
    self.load_archive(Archive(config=radio))
    self.load_schedule(Schedule(archive=self.archive))

    show = self.config.search_by_name(self.state['show'])

    if show == None:
      self.html_error('Programa <em>%s</em> não encontrado' % self.state['show'])
      return
    sshow = self.schedule.next_show_files(show)
    print '<div style=" bottom:100px; top:15%;width: 95%; padding: 10px">'
    print '<h1> Gestão de programas da Rádio Zero: %s </h1>'   % show.bcast_prefix
    print '<div id="show_info"'
    print '<h2>Informação do programa</h2>'
    print '<ul>'
    print '<li>Directo?', show.live, '</li>'
    print '<li>Duração:', show.length, '</li>'
    print '<li>Primeira emissão:',show.first,'</li>'
    print '<li>Ultima repetição:',show.last,'</li>'
    print '<li>Prefixo de podcast:',show.podcast_prefix, '</li>'
    print '</ul>'
    print '</div>'
    if self.profile == 'broadcaster':
      print '<div id="broadcast">'
      print '<h2>Emissões</h2>'
      print '<h3>Log</h3>'
      def print_log(x):
        print '<tr>'
        print '<td>',x.ltime.strftime('%d/%M/%Y'),'</td>'
        print '<td>',x.type,'</td>'
        print '<td>',x.msg,'</td>'
        print '</tr>'
        return
      self.schedule.load_log(sshow, n=-1)
      if len(sshow.log) > 0:
        print '<table class="bcast_log">'
        sshow.log.reverse()
        map(print_log, sshow.log)
        print '</table>'
      else:
        print 'Não há ficheiro de log'
      print '<h3>Ficheiro de emissão</h3>'
      if sshow.files['bcast'].path != 'err':
        print sshow.files['bcast'].path.split('/')[-1]
      if sshow.files['pbcast'].path != 'err':
        print '<h3>Ficheiros pendentes</h3>'
        print sshow.files['pbcast'].path.split('/')[-1]
      else:
        print '<ul><li>Nenhum ficheiro pendente</li></ul>'
      print '</div>'


    print '<div id="podcast_waiting">'
    print ' <h2>Podcast</h2>'
    print ' <h3>Acesso rápido</h3>'
    print ' <form method="POST" name="operation" action=".">'
    print ' <ul>'
    print '   <li>Link para a  <a href="%s/%s.xml">Feed</a></li>' % (archive_url,show.podcast_prefix)
    print '   <li>Link para o <a href="http://welles.radiozero.pt/garden/listgardencgi.pl?feedname=%s&currenttab=Items"> garden</a></li>'  % show.podcast_prefix
    print ' </ul>'
    files = self.archive.waiting_show_files(show)
    print ' <h3>Ficheiros pendentes</h3>'
    if (len(files)== 0):
      print ' <ul><li>Nenhum ficheiro em espera</li></ul>'
    else:
      print ' <ul>'
      for f in files:
        print '   <li><a href="/nadmin/archive/%s/%s">%s</a></li>' % (self.archive.data_path.split('/')[-1], f,f)
    print ' </ul>'
    print '</div>'
    print '<div id=archive_list>'
    print ' <h2> Arquivo </h2>'
    print ' <input type="hidden" name="program_name" value="%s"/>' % show.bcast_prefix
    print ' <input type="submit" name="program:Ufeed" value="Carregar a feed"/>'
    print ' <input type="submit" name="program:Pfiles" value="Tornar públicos"/>'
  
    print '  <div style="width: 40%;float: left">'
    print '  <fieldset> <legend> Ficheiros arquivados</legend>'
    
    files = self.archive.show_files(show)
    N = len(files)
    if (N > 0):
      for i in xrange(0,N):
        print '   <input type="radio" name="programs" value="%s" id="%s" />' % (files[i], files[i])
        #print '<label for="%s"> %s </label>'  % (files[i], files[i])
        print '   <a href="%s/%s"> %s</a>' %(self.archive_url(), files[i], files[i])
        if( i   % 10  == 9):
          print '  <br />'
          print '  <hr />'
        print '  <br />'

    print '  </fieldset>'
    print '  </div>'
    
    print '  <div style="width: 40%;float: left">'
    print '  <fieldset> <legend> Ficheiros públicos(podcast)</legend>'
    #files = arch.get_public(program)
    #N = len(files)
    #if (N > 0):
    #  for i in xrange(0,N):
    #    print '<input type="checkbox" name="publicprograms" value="%s" id="%s" />' % (files[i], files[i])
    #    print '<label for="%s"> %s </label>'  % (files[i], files[i])
    #    if( (i   % 10) == 9):
    #      print '<br />'
    #      print '<hr />'
    #    print '<br />'

    print '  </fieldset>'
    print '  </div>'
    print ' </div>'
    print '</div>'
    print '</form>'
    self.html_footer()
    return

  def broadcast_view(self):
    self.html_header()
    radio = Radio(self.file)
    self.load_radio_config(radio)
    self.load_timetable(TimetableWeb(radio))
    
    print '<div id="main">'
    print '<hr />'
    print '<p>Bah!</p>'
    print '  <div id="left">'
    print '  <h1>Programas</h1>'
    print '<ul>'
    def print_options(x):
      print '<li>'
      print '<a href="./archive/%s">%s</a>' % (x,x)
      print '</li>'
      return
    map(print_options, self.config.get_radio_shows())
    print ' </ul>'
    print '  <hr />'
    print '  </div>'
    print '  <div id="right">'
    #print '  <hr />'
    print '<h1> Tabela de programação</h1>'
    #print '</div>'
    self.timetable.print_timetableW()
    #print '    <div id="legend">'
    print '  <br />'
    print '  <table dir="ltr" class="timetable" title="legenda">'
    print '  <tr><th colspan="8">Legenda(com ordem  de precedência)</th></tr>'
    print '  <tr>'#<th>1ª emissão</th>'
    print '  <td class="direct1">Emissão directa</td>'
    print '  <td class="red_alert1">Não há ficheiro na pasta emissão!</td>'
    print '  <td class="orange_alert1">Não há ficheiro na pasta de pré-emissão!</td>'
    print '  <td class="green_ok1">Tudo nos conformes</td>'
    print '  <td class="not_rep2">A repetição não coincide com a última emissão</td>'
    print '  <td class="yellow_log1">Não há informação sobre o passado do programa</td>'
    print '  <td class="yellow_rep1">O programa vai repetir!</td>'
    print '  <td class="TNA">Teoria dos Números aleatorios e outros...</td>'
    print '  </tr></table>'
    #print '    </div>'
    print '  </div>'
    print '  <div style="clear:both">'
    print '<p>Buh!</p>'
    print '</div>'
    print '</div>'
    self.html_footer()
    return
  
  def default_page(self):
    self.html_header()
    print '<h1> Page not Found!</h1>'
    self.html_footer()



form= cgi.FieldStorage()
app = RadioWebApp(form,file='/usr/local/var/archive/etc/grelhaS.csv')

app.run_operation()


