from fabric.api import *

env.user = 'paperchase'

# Define host names for inside and outside the LAN
def inside():
    env.hosts = ['brick.local']

def outside():
    env.hosts = ['dedalusj.dyndns.org']

# Run Celery worker locally
def run_celery(loglevel="info"):
    local("celery -A paperchase.tasks worker -B --loglevel=%s" % loglevel)    
    
# Setup and maintenance of the remote server
def setup_repo():
    with settings(warn_only=True):
        if run("git clone https://github.com/dedalusj/PaperChase.git .").failed:
            run("git pull")

def setup_venv():
    run("curl -O https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py")
    run("python virtualenv.py PC")
    run("PC/bin/pip install -r requirements.txt")

def setup():
    code_dir = '/Users/paperchase/server'
    local('mysqldump -u paperchase -p development > development.sql')
    with cd(code_dir):
        setup_repo()
        
    with cd(code_dir+'/webapp'):
        setup_venv()
        put('development.sql', code_dir+'/webapp')
        run('mysql --host=localhost --port=3306 --user=paperchase -p --reconnect development < development.sql')
        run("mkdir log")
    
def deploy():
    code_dir = '/Users/paperchase/server/webapp'
    put('paperchase/settings.py', code_dir+'/paperchase/')
    with cd(code_dir):
        pass
        
def update_database():
    run("alembic upgrade head")