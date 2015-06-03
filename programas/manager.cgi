#! /usr/bin/env python
# -*- coding: iso8859-1 -*-

import cgi
import cgitb; cgitb.enable ()
import os,re
import datetime

from config import *
from zero_aux import *
from html_common import  *
import archive, programs




def header():
    print "Content-type: text/html; charset='iso-8859-1'\n"
    print "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' \
    'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>"
    print "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='pt'>"
    print "<head>"
    print "\t<title>Gestão de programas</title>"
    print "\t<link href='%s/estilo_site.css' rel='stylesheet' type='text/css' />" % resources_dir
    print "\t<link rel='icon' href='%s/favicon.ico'/>" % resources_dir
    print "</head>"
    return


def add_program():
    
    print "<body>"
    print "<div>"
    print "<h1>Programa: %s</h1>" % program.name_prefix
    print "<form method='post' name='f1' action='./add.cgi'>"
    print "<p class='texto_branco'> Nome do ficheiro"
    print "<select name='program_file' size='1'>"
    #D: print program_pending
    for pg in media_file_list(program_pending):
        regex = "^%s*" % program.name_prefix
        if(re.search(regex, pg) != None):
            print "<option value='" + pg + "'>" + pg + "</option>"
    print "</select></p>"
    #print "</div>"
    print "<p class='texto'>Próxima Emissão?"
    print "<input type='hidden'name='program_name' value='%s' />" % program.name_prefix
    print "<input type='radio' name='next' value='Yes' id='next:yes' checked='checked' /><label for='next:yes'>Sim</label>"
    print "<input type='radio' name='next' value='No' id='next:no'                     /><label for='next:no' >Não</label>"
    print "</p>"
    print "<p class='texto'>Podcast?"
    print "<input type='radio' name='SoD' value='Yes' checked='checked'id='SoD:yes' /><label for='SoD:yes'>Sim</label>"
    print "<input type='radio' name='SoD' value='No'                   id='SoD:no'  /><label for='SoD:no'>Não</label>"
    print "</p>"
    print "<div>"
    print "<input class='small' type='submit' name='program:submit' value='OK' />"
    print "</div>"
    print "</form>"
    print "</div>"





def edit_podcast():
        #D: print N
    print '<body>'
    print '<div style=" bottom:100px; top:15%;width: 95%; padding: 10px">'
    print '<h1> Gestão de programas da Rádio Zero: %s </h1>'  % program.name_prefix
    print '<form method="POST" name="operation" action="./edit.cgi">'
    print '<h2> Acesso rápido</h2>'
    print '<ul>'
    print '\t<li>Link para a  <a href="%s/%s.xml">Feed</a></li>' % (stream_url,program.podcast_prefix)
    print '\t<li>Link para o <a href="http://radiologo.radiozero.pt/garden/listgardencgi.pl?feedname=%s&currenttab=Items"> garden</a></li>'  %program.podcast_prefix
    print '</ul>'
    print '<h2> Ficheiros em espera </h2>'
    files = arch.get_waiting(program)
    if (len(files)== 0):
      print '<div> Nenhum ficheiro em espera</div>'
      #print '<br/>'
    else:
      print '<ul>'
      for file in files:
        print '\t<li>%s</li>' % file
    print '</ul>'
    print '<h2> Arquivo </h2>'
    print '<input type="hidden" name="program_name" value="%s"/>' % program.name_prefix
    print '<input type="submit" name="program:Ufeed" value="Carregar a feed"/>' 
    print '<input type="submit" name="program:Pfiles" value="Tornar públicos"/>'

    print '<div style="width: 40%;float: left">'
    
    print '<fieldset> <legend> Ficheiros arquivados</legend>'
    files = arch.get_archived(program)
    N = len(files)
    if (N > 0):
      for i in xrange(0,N):
        print '<input type="checkbox" name="programs" value="%s" id="%s" />' % (files[i], files[i])
        print '<label for="%s"> %s </label>'  % (files[i], files[i])
        if( i   % 10  == 9):
          print '<br />'
          print '<hr />'
        print '<br />'

      # FOR USABILY REQUEST REMOVED 3 files per line
      #for i in xrange(0,N,3):
      #  print '<input type="checkbox" name="programs" value="%s" id="%s" />' % (files[i], files[i])
      #  print '<label for="%s"> %s </label>'  % (files[i], files[i])
      #  if(i + 1<N):
      #    print '<input type="checkbox" name="programs" value="%s" id="%s"/>' % (files[i+1],files[i+1])
      #    print '<label for="%s"> %s </label>'  % (files[i+1], files[i+1])
      #
      #  if(i +2<N):
      #    print '<input type="checkbox" name="programs" value="%s" id="%s" />' % (files[i+2], files[i+2])
      #    print '<label for="%s"> %s </label>'  % (files[i+2], files[i+2])
      #  #D: print  ((i  ) % (10 * 3))
      #  if( (i   % (10 * 3)) == 27):     #ATENCAO N COLUNAS =3/ N LINHAS=10
      #    print '<br />'
      #    print '<hr />'
      #  print '<br />'
    print '</fieldset>'
    print '</div>'
    
    print '<div style="width: 40%;float: left">'
    print '<fieldset> <legend> Ficheiros públicos(podcast)</legend>'
    files = arch.get_public(program)
    N = len(files)
    if (N > 0): 
      for i in xrange(0,N): 
        print '<input type="checkbox" name="publicprograms" value="%s" id="%s" />' % (files[i], files[i])
        print '<label for="%s"> %s </label>'  % (files[i], files[i])
        if( (i   % 10) == 9): 
          print '<br />'
          print '<hr />'
        print '<br />'

    print '</fieldset>'
    print '</div>'
    print '</div>'
    print '</form>' 
       



    return 





#def footer():
#    print '<div style="bottom: 10px;clear:both;width=90%">'
#    print '<br /><a href="./chooser.cgi">Voltar</a>'
#    print "<hr />"
##    print "<p><a href='http://validator.w3.org/check?uri=referer'>\
#<img src='http://www.w3.org/Icons/valid-xhtml10'\
# alt='Valid XHTML 1.0 Transitional' height='31' width='88' /></a></p>"	
#    print '</div>'
#    print "</body>"
#    print "</html>"


form = cgi.FieldStorage()
program = programs.Program()

header()


try:
    program.load_form(form)
except:
    exit
    #TODO: implementar notificacao de erro

arch = archive.Archive()
arch.load_archive(archive_config)

#if (program.name_prefix == str(arch.programs[0].name_prefix)):
#    print arch.programs[1].name_prefix

program=arch.search_by_name(program.name_prefix)

if ( program != False):
    if (form.has_key('program:add')):
        add_program()
    elif (form.has_key('program:publish')):
        edit_podcast()
        
else:
    print "<p /> Programa não encontrado"

footer()


