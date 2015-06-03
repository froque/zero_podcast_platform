#! /usr/bin/env python
# -*- coding: iso8859-1 -*-

import cgi
import cgitb; cgitb.enable ()
import os,re
import datetime

from config import *
from html_common  import *
import archive, programs




def main():
    print "Content-type: text/html; charset='iso-8859-1'\n"
    print "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' \
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>"

    print "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='pt'>"

    print "<head>"
    print "\t<title> Gestão de programas</title>"
    print "\t<link href='%s/estilo_site.css' rel='stylesheet' type='text/css' />" % resources_dir
    print "\t<link rel='icon' href='%s/favicon.ico'/>" % resources_dir
    print "</head>"

    print "<body>"
    print "<div>"
    print "<h1>Programa</h1>"
    print "<form method='post' name='f1' action='./manager.cgi'>"
    print "<div> Nome do programa </div>"
    print "<select name='program_name' size='1'>"
    for pg in arch.programs:
        print "<option value='" + pg.name_prefix + "'>" + pg.name_prefix + "</option>"
    print "</select>"
    
    print "<div>"
    print "<input type='submit' name='program:add' value='Adicionar' />"
    #print "<input type='submit' name='program:listar' value='Listar Programas' />" #TODO!!!
    print '<input type="submit" name="program:publish" value="Editar podcast">'
    print "</div>"


    print "</form>"    
    print "</div>"
    
    print "<hr />"
    print "<p><a href='http://validator.w3.org/check?uri=referer'>\
<img src='http://www.w3.org/Icons/valid-xhtml10'\
 alt='Valid XHTML 1.0 Transitional' height='31' width='88' /></a></p>"	
    print "</body>"
    print "</html>"

arch = archive.Archive()
arch.load_archive(archive_config)
main()
