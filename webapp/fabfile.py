from fabric.api import *

env.user = 'paperchase'

def inside():
    env.hosts = ['brick.local']

def outside():
    env.hosts = ['dedalusj.dyndns.org']

def run_celery(loglevel="info"):
    local("celery -A paperchase.tasks worker -B --loglevel=%s" % loglevel)    
        
def setup_mysql():
    # setup mysql user and database here
    pass

def setup_redis():
    # setup redis
    pass
    
def setup_repo():
    if run("git clone https://github.com/dedalusj/PaperChase.git .").failed:
        run("git pull")

def setup_venv():
    run("curl -O https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py")
    run("python virtualenv.py PC")
    run("PC/bin/pip install -r requirements.txt")

def setup():
    code_dir = '/Users/paperchase/server'
    with cd(code_dir):
        setup_mysql()
        setup_redis()
        setup_repo()
    with cd(code_dir+'/webapp'):
        setup_venv()
        run("mkdir log")    
    
def deploy():
    code_dir = '/Users/paperchase/server/webapp'
    with cd(code_dir):
        pass