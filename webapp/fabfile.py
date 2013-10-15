import string
from random import choice

from fabric.api import *
from fabric.operations import prompt

env.user = 'paperchase'

# Define host names for inside and outside the LAN
def inside():
    env.hosts = ['brick.local']

def outside():
    env.hosts = ['dedalusj.dyndns.org']
    
def vm():
    env.hosts = ['paperchasevm.local']

# Run Celery worker locally
def run_celery(loglevel="info"):
    local("celery -A paperchase.tasks worker -B --loglevel=%s" % loglevel)    
    
# Setup and maintenance of the remote server
def make_dir():
    run("mkdir PaperChase")

def setup_repo(path="PaperChase"):
    """Original clone of the repo"""
    with cd(path):
        run("git clone https://github.com/dedalusj/PaperChase.git .")
        with cd('webapp'):
            run("mkdir log")

def setup_venv(path="PaperChase/webapp"):
    with cd(path):
        run("curl -O https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py")
        run("python virtualenv.py venv")
        run("venv/bin/pip install -r requirements.txt")
    fix_feedparser(path)
        
def fix_feedparser(path="PaperChase/webapp"):
    with cd(path):
        run("mkdir temp")
        cd("temp")
        run("git clone https://github.com/dedalusj/feedparser.git .")
        run("mv feedparser/feedparser.py ../venv/lib/python2.7/")
        cd("..")
        run("rm -fdr temp")
        
def prompt_for_settings():
    prompt("What's the MySQL database?", key="database", default="paperchase_development")
    prompt("Enter the paperchase user password for the database, ", key="db_password")
    prompt("Enter an email address for mail notifications, ", key="mail_address")
    prompt("What's the mail server?", key="mail_server")
    prompt("What's the mail port?", key="mail_port", default="465")
    prompt("Does the mail service use SSL?", key="mail_ssl", default="True")
    prompt("Enter a username for the mail service, ", key="mail_username")
    prompt("Enter a password for the mail service, ", key="mail_password") 

def setup_settings(path="PaperChase/webapp/paperchase"):
    prompt_for_settings()
    with cd(path):
        run("cp settings.py.example settings.py")
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$database',env.database))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$db_password',env.db_password))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$mail_address',env.mail_address))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$mail_server',env.mail_server))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$mail_port',env.mail_port))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$mail_ssl',env.mail_ssl))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$mail_username',env.mail_username))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$mail_password',env.mail_password))
        
        chars = string.letters + string.digits
        length = 10
        secret_key = ''.join(choice(chars) for _ in range(length))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$secret_key',secret_key))
        
        length = 22
        password_salt = ''.join(choice(chars) for _ in range(length))
        run('sed -i "" "s/{0}/{1}/" settings.py'.format('$password_salt',password_salt))

def setup():
    code_dir = '/Users/paperchase/server'
    local('mysqldump -u paperchase -p development > development.sql')
    with cd(code_dir):
        setup_repo()
        
    with cd(code_dir + '/webapp'):
        setup_venv()
        put('development.sql', code_dir + '/webapp')
        run('mysql --host=localhost --port=3306 --user=paperchase -p --reconnect development < development.sql')
        run("mkdir log")

def update_repo(path="PaperChase"):
    """Update the repo"""
    with cd(path):
        run("git pull")
    
def deploy():
    code_dir = '/Users/paperchase/server/webapp'
    put('paperchase/settings.py', code_dir+'/paperchase/')
    with cd(code_dir):
        pass
        
def update_database():
    run("alembic upgrade head")