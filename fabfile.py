from fabric.api import *

env.hosts = ['srv1.tna.pf']

def filebackup():
    sudo('cd /var/backups/fabric/files && tar -cvzf www.tna.pf.tar.gz /var/www/www.tna.pf')
    sudo('cd /var/backups/fabric/files && tar -cvzf doc.tna.pf.tar.gz /var/www/doc.tna.pf')

def dbdump(password):
    sudo ('cd /var/backups/fabric/db && mysqldump -u root -p%s wwwtnapf > wwwtnapf.sql' %password)
    sudo ('cd /var/backups/fabric/db && mysqldump -u root -p%s mediawiki > mediawiki.sql' %password)
    sudo ('cd /var/backups/fabric/db && mysqldump -u root -p%s mumble > mumble.sql' %password)
    sudo ('cd /var/backups/fabric/db && mysqldump -u root -p%s archivetnapf > archivetnapf.sql' %password)

def slapdump():
    sudo ('cd /var/backups/fabric/db && slapcat > annuaire.ldif')

def dbbackup(password):
    dbdump(password)
    slapdump()
    filebackup()
    sudo ('cd /var/backups/fabric/db && rm *.bz2 && bzip2 *')
    get('/var/backups/fabric/db/*', 'databases/')
    get('/var/backups/fabric/files/*', 'files/')
