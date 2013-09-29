from fabric.api import local

env.user = 'dedalus'

def inside():
    env.hosts = ['brick.local']

def outside():
    env.hosts = ['dedalusj.dyndns.org']

def run_celery():
    local("celery -A paperchase.tasks worker -B --loglevel=debug")