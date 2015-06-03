# -*- coding: iso8859-1 -*-



host = "welles.ist.utl.pt"
host = "radiologo.radiozero.pt"

site = "http://" + host #+ "/programas/"
stream_url = "http://archive.radiozero.pt"
resources_dir = "/resources"

#path_root = "/usr/local/var/"
path_root = "/srv"
programs_dir = "ftp/emissao"
SoD_dir = "SoD_preview"
SoD_end_dir = "SoD"

#SoD_pending = "/usr/local/var/SoD_preview"
#SoD_final = "/usr/local/var/SoD"



SoD_preview = "/home/radiologo/SoD"
program_pending = "/home/radiologo/ftp/archive"
sched   = "/home/programacao/emissao"
sched_pre = "/home/programacao/emissao_pre" 

#archive_path = "/usr/local/var/archive"
archive_path = "/srv/archive.legacy"
archive_data = "%s/data"  % archive_path
archive_share= "%s/share" % archive_path
archive_config = "%s/etc/grelhaS.csv" % archive_path
share_pre    = "%s/share_tmp" % archive_path 

toaddr = "programacao@radiozero.pt"
toaddr = "tecnica@radiozero.pt"
fromaddr = "submissao_programa@radiozero.pt"

smtp_server="smtp1.ist.utl.pt"



email_list={
    'programacao': 'programacao@radiozero.pt',
    #'programacao': 'tecnica@radiozero.pt',
    'tecnica'    : 'tecnica@radiozero.pt'
    }

email_symbol='[AT]'
media_formats = ['mp3', 'ogg']
