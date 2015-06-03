#! /usr/bin/env python
# -*- coding: iso8859-1 -*-


import cgi, Cookie, smtplib, shutil, datetime
import cgitb; cgitb.enable ()

from config import *
from zero_aux import *
from html_common  import *
import programs, archive


def check_form(form):
    #por ordem decrescente
    if not form.has_key("program_file"):
        return {'err': 'Não foi submetido nenhum ficheiro!'} 
    if not form.has_key("next"):
        return {'err': 'Erro: O programa é para emitir?'} 
    if not form.has_key("SoD"):
        return {'err': 'Erro: O programa é para Podcast?'}
    if not form.has_key("program_name"):
        return {'err': 'Erro desconhecido'}
    
    return None




def main():

    print "<body>"
    print "<h1> Programa: %s </h1>" % program.name_prefix
    print "<ul>"
    if (program.archive(arch)): #salvaguarda do ficheiro para arquivo
            print "<li>O ficheiro <em>%s</em> foi arquivado</li>" % program.media_file
    else:
        print "<li>O ficheiro <em>%s</em> <b>NÃO</b> foi adicionado ao arquivo!</li>" % program.media_file
        
        #Necessario repensar este return:
        #  se for necessario arquivar entao está correcto
        #  caso contrario, é necessario modificar; cuidado
        #  com a tag em baixo: pensada para o return.
        program.mail_check_archive()    
        print "</ul>"
        return
    #ENDIF
    if (program.emission_status == True):
        import grp, datetime
        from stat import S_IRUSR, S_IWUSR,  S_IRGRP, S_IWGRP, S_IROTH
        now = datetime.datetime.now()
        print '<p>DEBUG: Ultima emissao:', program.last, ' agora:',now, ' primeira;', program.first, '</p>'
        if (now < program.last and program.live == False ):
          src = arch.data + "/" + program.media_file
          #fd = open(src,  "w")
          #fd.close()

          #UID = os.geteuid()
          #GID = grp.getgrnam('radiologo')[2]
          #os.chown(src, UID,GID)
          #os.chmod(src, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP)
          ext = program.media_file.split('.')[-1]
          dst = sched_pre + '/' + program.name_prefix + '.' + ext
          link_file(src, dst)
            


          print '<p> DEBUG: Na lista de espera</p>'
        else:
          print '<p> DEBUG: Na pasta de emissão</p>'
          program.force_emission(arch,program.media_file) 

        
        print "\t<li>O ficheiro %s será emitido na próxima emissão.</li>" % program.media_file
        
    elif (program.emission_status == False): 
        print "\t<li> O ficheiro arquivado não será emitido.</li>"
    #ENDIF
    if (program.SoD_status == True):
        print "\t<li><em>Podcast:</em></li>"
        print "\t<ul>"
        print "\t<li>Seguir para o <a href='http://radiologo.radiozero.pt/garden' target='_blank'> listgarden</a></li>"
        print "\t<li>Depois de configurado, é necessario <b>sair</b>!</li>"
        print "\t</ul>"
        print "<form method='post' name='exit' action='./add.cgi'>"
        print "<input class='small' type='hidden' name='program_file' value='%s' />" % program.media_file
        if (program.emission_status == True):
          print "<input class='small' type='hidden' name='next' value='Yes' />" 
        else:
          print "<input class='small' type='hidden' name='next' value='No' />" 
        print "<input class='small' type='hidden' name='SoD' value='%s' />"% str(program.SoD_status)
        print "<input class='small' type='hidden' name='program_name' value='%s' />"% program.name_prefix
        print "<input class='small' type='submit' name='program:exit' value='Sair' />"
        print "</form>"
    else:
        program.clean_pending_dir()
    #ENDIF
    
    print "</ul>"    
    return
            
    


def add_exit():    
    print "<body>"
    print "<h1> Status da entrada no podcast</h1>"
    url='%s/%s' % (stream_url, program.media_file)
    
    if(program.emission_status == False or program.live == True):
      err=program.force_publish(arch, program.media_file)
      print '<ul>'
      if( err == None):
        url='%s/%s' % (stream_url, program.media_file)
        print '<li>Ficheiro %s está publicamente disponível no endereço <a href="%s">%s</a></li>' % (program.media_file, url, url)
        program.clean_pending_dir()
        program.mail_new_podcast(url)
      else:
        print '<li>Ficheiro não está disponível para podcast</li>'
      del err; err = program.force_feed(arch)
      if ( err == None):
        print '<li>A feed foi actualizada</li>'
      else:
        print '<li>A feed <b>NÃO</b> foi actualizada'
      print '</ul>'
      return
    
    p = program.enable_podcast(arch) 
     
    #D: print p
    if (p != None):
        print "<p>erro: %s</p>" % p['err']
    else:
        print "<p><em>Podcast</em> estará disponível depois da primeira emissão</p>"
        print "<p><a href='%s'> Voltar</a></p>" % (site)
        program.mail_new_podcast(url)
        program.clean_pending_dir()
    return


    
def print_error(err):
    print "<p /> erro %s" % err

def print_unknown_error():
    print_error('desconhecido')


form = cgi.FieldStorage()
program = programs.Program()

print_header()

arch  = archive.Archive()
arch.load_archive(archive_config)

form_status = check_form(form)
if ( form_status != None):
    if form_status.has_key('err'):
        print_error(form_status['err'])
    else:
        print_unknown_error()
else:
    try:
        program.load_form(form)
        #D: print "|%s|" % program.name_prefix
    except:
        print_error('errp')
    tmp = arch.search_by_name(program.name_prefix)
    if tmp == False:
          print '<p>erro1</p>'
    elif tmp.name_prefix != program.name_prefix:
          print '<p>erro2</p>'
    else:
          program.load_config(tmp)

    if   form.has_key('program:submit'):
        main()
    elif form.has_key('program:exit'):
        add_exit()

footer()










