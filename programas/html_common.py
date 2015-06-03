#! /usr/bin/env python
# -*- coding: iso8859-1 -*-

from config import *

def print_header():    
    print "Content-type: text/html; charset='iso-8859-1'\n"
    print "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN'\
'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>"    
    print "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>"
    print "<head>"
    print "<title>Rádio Zero</title>"
    print "<link href='%s/estilo_site.css' rel='stylesheet' type='text/css' />" %  resources_dir
    print "<link rel='icon' href='%s/favicon.ico' />" %  resources_dir
    print "</head>"


def create_help_link():
    print '<p> SOS:</p>'
    print '<p> * <a href="./help.htm">FAQ:</a>Perguntas que serão feitas frequentemente</p>'
    print '<p> * <a href=".">Help Desk</a> ( a técnica)</p>'
    return


def footer():

    print '<div style="padding:10px; bottom: 100px;clear:both;width=90%">'
    print '<a href="chooser.cgi"> Voltar</a>'
    print "<hr />"
    create_help_link()
#    print "<p><a href='http://validator.w3.org/check?uri=referer'>\
#<img src='http://www.w3.org/Icons/valid-xhtml10'\
# alt='Valid XHTML 1.0 Transitional' height='31' width='88' /></a></p>"	
    print '</div>'
    print "</body>"
    print "</html>"
