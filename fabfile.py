from fabric.api import *
from os import path
import yaml

stream = open("tna.yaml", 'r')
conf = yaml.load(stream)

env.hosts = ['srv1.tna.pf']

def filecopy(path, archive_name):
    with cd('/var/backups/fabric/files'):
        sudo('tar -cvzf %s.tar.gz %s' %(archive_name, path))

def filedump():
    filecopy('/var/www/www.tna.pf', 'www.tna.pf')
    filecopy('/var/www/doc.tna.pf', 'doc.tna.pf')

#def config():
#    print conf['srv1.tna.pf']['config']

def mysqldump(user, password, database):
    sudo('mysqldump -u %s -p%s %s > %s.sql' %(user, password, database, database))

def dbdump(user,password):
    with cd('/var/backups/fabric/db'):
        mysqldump(user, password, 'wwwtnapf')
        mysqldump(user, password, 'mediawiki')
        mysqldump(user, password, 'mumble')
        mysqldump(user, password, 'archivetnapf')

def slapdump():
    with cd('/var/backups/fabric/db'):
        sudo ('slapcat > annuaire.ldif')

def dbbackup(password):
    dbdump(password)
    slapdump()
    filedump()
    sudo ('cd /var/backups/fabric/db && rm *.bz2 && bzip2 *')
    get('/var/backups/fabric/db/*', 'databases/')
    get('/var/backups/fabric/files/*', 'files/')
