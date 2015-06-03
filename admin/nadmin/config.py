# -*- coding: iso8859-1 -*-



archive_url = "http://archive.radiozero.pt"
resources_dir = "/resources"

ftp = "/home/radiologo/ftp/archive"

sched = "/home/programacao/emissao"
presched = "/home/programacao/emissao_pre" 

archive_path = "/usr/local/var/archive"
archive_data = "%s/data"  % archive_path
archive_share= "%s/share" % archive_path
archive_config = "%s/etc/grelhaS.csv" % archive_path
share_pre    = "%s/share_tmp" % archive_path 

toaddr = "programacao@radio.ist.utl.pt"
toaddr = "tecnica@radio.ist.utl.pt"
fromaddr = "submissao_programa@radio.ist.utl.pt"

smtp_server="smtp1.ist.utl.pt"



email_list={
    #'programacao': 'programacao@radio.ist.utl.pt',
    'programacao': 'tecnica@radiozero.pt',
    'tecnica'    : 'tecnica@radiozero.pt'
    }

email_symbol='[AT]'
media_formats = ['mp3', 'ogg']
