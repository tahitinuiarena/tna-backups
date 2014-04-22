from fabric.api import *
from os import path
import yaml

stream = open("conf.yaml", 'r')
conf = yaml.load(stream)

def getconfig(server, what, password):
    if what == 'all':
        if 'ldap' in conf[server]:
            print 'LDAP'
            with cd('/var/backups/fabric/db'):
                for database in conf[server]['ldap']:
                    ldapdump(conf[server]['config']['ldapuser'], password, database)
        if 'mysql' in conf[server]:
            print 'MYSQL'
            with cd('/var/backups/fabric/db'):
                for database in conf[server]['mysql']:
                    mysqldump(conf[server]['config']['mysqluser'], password, database)
        if 'files' in conf[server]:
            print 'FILE'
            with cd('/var/backups/fabric/files'):
                for archives in conf[server]['files']:
                    directory = ''
                    for directories in conf[server]['files'][archives]:
                        directory = directory + ' '+ directories
                    filedump(archives, directory)
    else:
        if what in conf[server]:
            if what == 'ldap':
                with cd('/var/backups/fabric/db'):
                    for database in conf[server]['ldap']:
                        ldapdump(conf[server]['config']['ldapuser'], password, database)
            if what == 'mysql':
                with cd('/var/backups/fabric/db'):
                    for database in conf[server]['mysql']:
                        mysqldump(conf[server]['config']['mysqluser'], password, database)
            if what == 'files':
                with cd('/var/backups/fabric/files'):
                    for archives in conf[server]['files']:
                        directory = ''
                        for directories in conf[server]['files'][archives]:
                            directory = directory + ' '+ directories
                        filedump(archives, directory)
        else:
            print("No %s in config file." %what)

def filedump(files, directory):
    sudo('tar -cvzf %s.tar.gz %s' %(files, directory))

def mysqldump(user, password, database):
    sudo('mysqldump -u %s -p%s %s > %s.sql' %(user, password, database, database))

def ldapdump(user, password, database):
    sudo ('slapcat > annuaire.ldif')

def dbbackup(password):
    dbdump(password)
    slapdump()
    filedump()
    sudo ('cd /var/backups/fabric/db && rm *.bz2 && bzip2 *')
    get('/var/backups/fabric/db/*', 'databases/')
    get('/var/backups/fabric/files/*', 'files/')

@task
def backup(hostname = 'all', what = 'all', password = ''):
    if hostname == 'all':
        for server in conf:
            if conf[server]['config']['sudo'] == False:
                env.user = 'root'
            else:
                env.user = conf[server]['config']['user']
            env.host_string = server
            getconfig(server, what, password)
    else:
        for server in conf:
            if conf[server]['config']['sudo'] == False:
                env.user = 'root'
            else:
                env.user = conf[server]['config']['user']
            if server == hostname:
                env.host_string = server
                getconfig(server, what, password)

@task
def sync():
    print "Copy files"
    for server in conf:
        env.host_string = server
        local('mkdir -p data/'+server)
        with cd('/var/backups/fabric/db'):
            sudo('rm -fr *.bz2')
            sudo('bzip2 *')
            get('*.bz2','databases/')


