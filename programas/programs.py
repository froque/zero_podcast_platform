#! /usr/bin/env python
# -*- coding: iso8859-1 -*-

import cgi, Cookie, smtplib, shutil, os, re
import datetime

from config import *
from zero_aux import *

#import pdb
#pdb.set_trace()
class Program:
    def __init__(self):
        self.description = ""
        self.name_prefix = ""
        self.podcast_prefix = ""
        self.SoD_status  = False
        self.emission_status = True
        self.cookie = Cookie.SimpleCookie()
        self.feed = ""
        self.media_file =  ""
        self.live = False
        self.length = 0
        self.first = datetime.datetime.now()
        self.last  = datetime.datetime.now()

    #TODO: substituir as strings 'Yes' e 'No' por
    #      'True' e 'False' para compatibilidade
    #      com str(True) e str(False)
    #      Aqui estao as validacoes;
    #      As fontes estao nos ficheiros que geram
    #      os ficheiros html-->forms!
    
    def load_form(self, form):        
        if form.has_key('program_name'):
            self.name_prefix = form['program_name'].value
        if form.has_key('SoD'):
            if (form['SoD'].value == 'Yes'):
                self.SoD_status = True
            else:
                self.SoD_satus = False
        if form.has_key('next'):
            if (form['next'].value == 'Yes'):
                self.emission_status = True
            else:
                self.emission_status = False                
        if form.has_key('program_file'):
            self.media_file = form['program_file'].value
        return

    def load_config(self,program):
      """loads config parameters from similar structure"""
      if len(program.name_prefix) > 0:
        self.name_prefix = program.name_prefix
      if len(program.podcast_prefix) > 0:
        self.podacast_prefix = program.podcast_prefix
      self.live = program.live
      self.first = program.first
      self.last = program.last
      return
      



    def archive(self,archive):
        src = program_pending + "/" + self.media_file
        dst = archive.data + "/" + self.media_file
        #D: print src, dst
        if (copy_file (src, dst)):
            return True
        else:
            return False

        
    
    def enable_podcast(self, archive):
        import pwd
        import grp


        from stat import S_IRUSR, S_IWUSR,  S_IRGRP, S_IWGRP, S_IROTH
        ret = {}
        #D: print "|%s|" % self.name_prefix
        tmp = archive.search_by_name(self.name_prefix)
        if tmp == False:
          ret['err'] = "A feed não foi publicada, erro interno: feed nao encontrada"
          return ret
        elif tmp.name_prefix != self.name_prefix:
          ret['err'] = "A feed não foi publicada, erro interno: nomes distintos"
          return ret

                

        xml_ = tmp.podcast_prefix + ".xml"
        src = program_pending + "/" + xml_

 
        fname = share_pre + "/" + xml_

        #D: print "Feed: %s" % xml_
        #D: print "files: src %s| dest: %s|)" % (src, fname)

        if (not mv_file (src,fname)):
            ret['err'] = "A feed não foi publicada"
        
       
        #USER = 'radiologo'
        #UID = os.geteuid()
        #GID = grp.getgrnam('radiologo')[2]
        #os.chown(fname, UID,GID)
        #os.chmod(fname, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH)

        fname = share_pre + "/" + self.media_file
        fd = open(fname, "w")
        fd.close()
        #os.chown(fname, UID,GID)
        #os.chmod(fname, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP)

        if (len(ret) == 0):
          return None
        return ret

    def force_feed(self, archive):
        import pwd
        import grp

        from stat import S_IRUSR, S_IWUSR,  S_IRGRP, S_IWGRP, S_IROTH
        
        #D: print "|%s|" % self.name_prefix
        tmp = archive.search_by_name(self.name_prefix)
        if tmp == False:
          return  {'err': "A feed não foi publicada, \
              erro interno: nome  nao encontrada"}
        elif tmp.name_prefix != self.name_prefix:
          return  {'err': "A feed não foi publicada, \
              erro interno: nomes distintos"}

        xml_ = tmp.podcast_prefix + ".xml"
        src = program_pending + "/" + xml_
 
        fname = archive.share + "/" + xml_

        #D: print "Feed: %s" % xml_
        #D: print "files: src %s| dest: %s|)" % (src, fname)

        if (not file_exists(src)):
          return {'err': 'A feed não se encontra no ftp'}
        if (not mv_file (src,fname)):
            return {'err': "A feed não foi publicada"}
   
 
        #UID = os.geteuid()
        #GID = grp.getgrnam('radiologo')[2]
        #os.chown(fname, UID,GID)
        #os.chmod(fname, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH)
        return


    def force_publish(self, archive, file):
      """ Make link from the archive dir to the public podcast dir"""
      src = archive.data  + "/" + file
      dst  = archive.share + "/" + file
      
      if(link_file(src,dst)):
          return None

    def force_emission(self, archive, file):
      """ Make link from the archive dir to the public podcast dir"""
      src = archive.data  + "/" + file
      dst  = sched  + "/%s.mp3" %  self.name_prefix
      
      if(link_file(src,dst)):
          return None


 

    def clean_pending_dir(self):
        src = program_pending + "/" + self.media_file
        #print src
        try:
            os.remove(src)
        except:
            #TODO: mail para a tecnica a informar da situação.
            # possiveis campos:
            #  * data | nome_ficheiro | nome_programas
            #print "nao apaguei o devido"
            pass

        return

    def mail_new_podcast(self,url):
        sub =  "[podcast] %s-%s " % (self.name_prefix, self.podcast_prefix)
        if type(self.first) is datetime.datetime:
          dat = self.first.strftime("%F %a").split()
          sub = "[podcast %s] %s-%s %s" % (dat[1],self.name_prefix, self.podcast_prefix, dat[0])
        msg = datetime.datetime.now().strftime("%F, %R\n\n\n")
        msg += "O radiólogo responsável pelo programa '%s' actualizou o podcast\n" % self.name_prefix
        msg +="url: %s" % url
        return send_mail("radiologo@radiozero.pt", email_list['programacao'],sub,msg)


    def mail_new_emission(self):
        sub =  "[Emissao] Programa submetido" 
        msg = "O radiólogo responsável pelo programa '%s' actualizou o ficheiro para emissão" % self.name_prefix
        return send_mail("radiologo@radiozero.pt", email_list['programacao'],sub,msg)

    def mail_check_emission(self):
        sub =  "[Emissao] Programa NAO submetido"         
        msg = "O radiólogo responsável pelo programa '%s' tentou actualizar o \
programa para emissão mas vocês ainda não trataram do anterior!" % self.name_prefix
        return send_mail("radiologo@radiozero.pt", email_list['programacao'],sub,msg)

    def mail_check_archive(self):
        sub =  "[Arquivo] programa NAO arquivado"      
        msg = "O radiólogo responsável pelo programa '%s' tentou adicionar o\
programa no arquivo mas não consegui; Ficheiro: %s" % (self.name_prefix, self.media_file)
        return send_mail("radiologo@radiozero.pt", email_list['tecnica'],sub,msg)

        
    
    def get_date_stamp(self):
        today = datetime.date.today()
        return  today.strftime("%Y%m%d")
        
    def get_program_filename(self):
        return self.name_prefix + "." + self.file_format 

    def get_SoD_filename(self):
        return self.name_prefix + self.date_stamp + "." + self.file_format 

    def send_mail_radio(self, from_, to_):
        subject =  "[Programa submetido] %s" % self.name_prefix
        # Add the From: and To: headers at the start!
        
        head = "From: %s\r\nTo: %s\r\nSubject: %s\r\n" %(from_, to_, subject)
        msg = "O radiólogo responsável pelo programa '%s' actualizou o ficheiro para emissão" %(self.name_prefix)
        
        msg = head + msg 
        
        try:
            server = smtplib.SMTP(smtp_server)
        except:
            return "Não me consegui ligar ao servidor de mail. Tenta mais tarde"
        server.set_debuglevel(0)
        try:
            server.sendmail(from_, to_, msg)
        except:
            return "Não consegui enviar o mail de aviso para a programação"
        server.quit()
        return None

    def check_xml_file(self):
        all_files =  os.listdir(path_root + SoD_dir)
        if (all_files.count(self.name_prefix + '.xml') > 0):
            return self.name_prefix + '.xml'
        return None

    def mv_xml_file(self):
        self.feed = self.check_xml_file()
        if self.feed != None:
            src_path = path_root + SoD_dir + '/' + self.feed
            dst_path = path_root + SoD_end_dir + '/' + self.feed
            #print src_path, dst_path
            if mv_file(src_path, dst_path):
                #print "<p /> Feed (%s) movida correctamente" % (self.feed)                
                return None
            else:
                #print "<p /> Nao consegui mover a feed: %s" % (self.feed)
                return {'err': 'Não consegui mover a feed: ' + self.feed}
        else:
            return {'err': 'A feed não foi encontrada!'}

    def check_media_files(self):
        all_files   = os.listdir(path_root + SoD_dir)
        media_re    = re.compile(self.name_prefix + '.*.mp3')
        media_files = []
        for file in all_files:
            if (media_re.search(file) != None):
                media_files.append(file)
        #print media_files
        if len(media_files) > 0:
            return media_files
        return None

    def mv_media_files(self):
        self.media_files = self.check_media_files()
        #print media_files
        tmp = {}
        if self.media_files != None:
            for file in self.media_files:
                src_path = path_root + SoD_dir + '/' + file
                dst_path = path_root + SoD_end_dir + '/' + file
                if mv_file(src_path, dst_path):
                    #print "<p />" + file + ": OK!"
                    tmp[file] = 'OK'
                else:
                    #print "<p /> Nao consegui mover o ficheiro: " + file
                    tmp[file] = 'Falhou'
                    #print file
        else:
            tmp = {'err': 'Nao foram encontrados ficheiros ' + self.file_format}
        #print "<p>Nao foram encontrados ficheiros mp3. Volte ao <a href='/programas/index.cgi'>inicio</a></p>"
        return tmp

