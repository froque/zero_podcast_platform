#! /usr/bin/env python
# -*- coding: iso8859-1 -*-

import cgi, Cookie, smtplib, shutil, os, re

from config import *


def media_file_list(dir):
    all_files =  os.listdir(dir)
    file_list = []
    regex = ('.*[.]')
    for i in media_formats:
        regex = regex + i + '$|'
    #D: print regex
    sufix = re.compile(regex.rstrip('|'))
    for file in all_files:
        if (sufix.search(file) != None):
            #print file
            file_list.append(file)
    return file_list


def get_cookie():
    cookie      = Cookie.SimpleCookie()
    cookie_string = os.environ.get('HTTP_COOKIE')
    if not cookie_string:
           return None

    else:
        cookie.load(cookie_string)
        return cookie
    return None

def copy_to_SoD(src, dst):
    src_path = path_root + programs_dir + '/' + src
    dst_path = path_root + SoD_dir + '/' + dst
    #print src_path
    #print dst_path
    try:
        shutil.copyfile(src_path, dst_path)
    except:
        return False
    return True


def copy_file(src, dst):
    try:
        shutil.copyfile(src, dst)
    except IOError, err:
        print err
        return False
    return True


def mv_file(src,dst):
    #D: shutil.move(src, dst)
    try:
        shutil.move(src, dst)
    except:
        #D: print "erro"
        return False
    return True

def link_file(src,dst):

    if (os.path.exists(dst)):
      os.unlink(dst)
    try:
        os.symlink(src,dst)
    except:
        return False
    return True
        
def file_exists(file):
  from os import F_OK,R_OK,W_OK,X_OK
  tmp = os.access(file, F_OK)
  return tmp

def next_wd(nweeks, wd, mode):
  """Returns a datetime object for the
     for the next weekday, that follows today.
     wd is isoweekday (sunday=0)"""
  import datetime
  tm =datetime.date.today()
  w = tm.isoweekday()
  if( w == 7):
    w = 0
  delta = (nweeks*7 + wd) - w
  #D: print 'wd,tday,delta: %s,%s,%s' %(wd,w,delta)
  if   (delta < 0 and mode > 0):
    delta = 7 - delta
  elif (delta > 0 and mode < 0):
    delta = delta - 7
  tm= tm +datetime.timedelta(days=delta)  

  return tm

  
  

  return

def print_mail_html(mail):
    mail_parts = mail.split('@')
    user = mail_parts[0]
    host = mail_parts[1]
    return user + email_symbol + host


def send_mail(from_, to_, subject, msg):

    head = "From: %s\r\nTo: %s\r\nSubject: %s\r\n" %(from_, to_, subject)            
    msg = head + msg 
    
    try:
        server = smtplib.SMTP(smtp_server)
    except:
        return {'err': "Não me consegui ligar ao servidor de mail. Tenta mais tarde"}
    server.set_debuglevel(0)
    try:
        server.sendmail(from_, to_, msg)
    except:
        return {'err': "Não consegui enviar o mail."}
    server.quit()
    return None
