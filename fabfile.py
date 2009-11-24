from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['f4ntasmic.com']
env.user = 'f4nt'

def deploy():
    local('python setup.py egg_info -dbDEV sdist rotate -m.tar.gz -k1')
    with cd('~/djtracker-builds/'):
        run('rm -f *.tar.gz')
    put('dist/*.tar.gz', '~/djtracker-builds/')
    with cd('~/djtracker-builds/'):
        sudo('easy_install -UaZ *.tar.gz')
