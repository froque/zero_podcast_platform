#!/usr/bin/python
# -*- coding: latin-1 -*-

import cgi
import cgitb; cgitb.enable()

from config import *
from zero_aux import *
from html_common  import *
import programs,archive






def check_form(form):
    if not form.has_key("program_name"):
        return {'err': 'Erro desconhecido'}
    
    return None


def force_newfeed():
  p = program.force_feed(arch)
  
  print "  <body bgcolor='#FFFFF' text='#000000'>"
  print "<h1>%s</h1>" % program.name_prefix
  
  if (p == None):
    print "<p> Nova feed disponível </p>"
  else:    
    print "<p>Erro: %s</p>" % p['err']


  return


def make_public():
  print "  <body bgcolor='#FFFFF' text='#000000'>"
  print "<h1>%s</h1>" % program.name_prefix
  
  if not form.has_key("programs"):
      print '<p>Não seleccionu programas para tornar públicos</p>'
      return

  if  isinstance(form['programs'],list):
    tmp = form.getlist('programs')
  else:
    tmp = [form['programs'].value]

  N = len(tmp)

  for i in tmp:
    p = program.force_publish(arch, i)
    if (p == None):
      print '<p>Ficheiro disponivel através de: %s/%s<p/>' % (stream_url, i)
    else:
      print '<p>O ficheiro %s já estava de disponível. \
          Se tal não for o caso contacte a «técnica»</p>' % (i)
    return



def list_program():
    print "  <body bgcolor='#FFFFF' text='#000000'>"
    allfiles = media_file_list(arch.data)
    files = []
    
    for i in xrange(len(allfiles)):
        regex = "^%s.*mp3" % program.podcast_prefix
        if(re.search(regex, allfiles[i]) != None):
          files.append(allfiles[i])
    import string
    files.sort(key=string.lower)
    files.reverse()




    N = len(files)
    #D: print N

    print '<form method="POST" name="operation">'
    print '<fieldset> <legend> Ficheros arquivados</legend>'
    if (N > 0):      
      for i in xrange(0,N,3): 
        print '<input type="checkbox" name="programs" value="%s" id="%s" />' % (files[i], files[i])
        print '<label for="%s"> %s </label>'  % (files[i], files[i])

        if(i + 1<N):
          print '<input type="checkbox" name="programs" value="%s" id="%s"/>' % (files[i+1],files[i+1])
          print '<label for="%s"> %s </label>'  % (files[i+1], files[i+1])

        if(i +2<N):
          print '<input type="checkbox" name="programs" value="%s" id="%s" />' % (files[i+2], files[i+2])
          print '<label for="%s"> %s </label>'  % (files[i+2], files[i+2])
        #D: print  ((i  ) % (10 * 3))
        if( (i   % (10 * 3)) == 27):     #ATENCAO N COLUNAS =3/ N LINHAS=10
          print '<br />'
          print '<hr />'
        print '<br />'
    print '<input type="submit" value="Tornar públicos">'
    print '</fieldset>'
    print '</form>' 
       
    print "  </body>"
    print "</html>"

    print "<body>"
    print "<h1> Gestão de programas da Rádio Zero</h1>"
    print "<h2> Programa: %s </h2>" % program.name_prefix
    print "<ul>"


    print "</ul>"
    return 



form = cgi.FieldStorage()
program = programs.Program()
arch  = archive.Archive()

form_status = check_form(form)



def print_error(err):
    print_header()
    print "<p /> erro %s" % err

def print_unknown_error():
    print_error('desconhecido')






if ( form_status != None):
    if form_status.has_key('err'):
        print_error(form_status['err'])
    else:
        print_unknown_error()
else:
    try:
        program.load_form(form)
        arch.load_archive(archive_config)
    except:
        print_unknow_error()
    print_header()
    if   form.has_key('program:Ufeed'):
        force_newfeed()
    elif form.has_key('program:Pfiles'):
        make_public()

    
footer()    



