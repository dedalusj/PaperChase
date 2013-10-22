import string
from random import choice
from datetime import date

from fabric.api import *
from fabric.operations import prompt

env.user = 'paperchase'
env.repo_path = 'PaperChase'

# Define host names for inside and outside the LAN
def inside():
    env.hosts = ['brick.local']

def outside():
    env.hosts = ['dedalusj.dyndns.org']
    
def vm():
    env.hosts = ['paperchasevm.local']  
    env.full_path = '/Users/' + env.user + '/' + env.repo_path
    
# Setup and maintenance of the remote server
def make_dir(path = env.repo_path):
    run("mkdir {0}".format(path))

def setup_repo(path = env.repo_path):
    """Original clone of the repo"""
    with cd(path):
        run("git clone https://github.com/dedalusj/PaperChase.git .")
        with cd('webapp'):
            run("mkdir log")

def setup_venv(path = env.repo_path + "/webapp"):
    with cd(path):
        run("curl -O https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py")
        run("python virtualenv.py venv")
        run("venv/bin/pip install -r requirements.txt")
    fix_feedparser(path)
        
def fix_feedparser(path = env.repo_path + "/webapp"):
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

def setup_settings(path = env.repo_path + "/webapp/paperchase"):
    prompt_for_settings()
    with cd(path):
        run("cp settings.py.example settings.py")
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$database',env.database))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$db_username','paperchase'))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$db_password',env.db_password))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$mail_address',env.mail_address))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$mail_server',env.mail_server))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$mail_port',env.mail_port))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$mail_ssl',env.mail_ssl))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$mail_username',env.mail_username))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$mail_password',env.mail_password))
        
        chars = string.letters + string.digits
        length = 10
        secret_key = ''.join(choice(chars) for _ in range(length))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$secret_key',secret_key))
        
        length = 22
        password_salt = ''.join(choice(chars) for _ in range(length))
        run("sed -i '' 's/{0}/{1}/' settings.py".format('$password_salt',password_salt))
        
def setup_supervisor(path = env.repo_path + "/webapp"):
    with cd(path):
        run("cp supervisord.conf.example supervisord.conf")
        run("sed -i '' 's/{0}/{1}/' supervisord.conf".format('$APP_PATH',env.full_path))
        run("venv/bin/supervisord")
        
def copy_settings(local_path="paperchase", remote_path = env.repo_path + "/webapp/paperchase"):
    local_file = local_path + "settings.py"
    remote_file = remote_path + "settings.py"
    put(local_file,remote_file)

def update_database(path = env.repo_path + "/webapp"):
    with cd(path):
        run("venv/bin/alembic upgrade head")

def copy_local_database(path = env.repo_path + "/webapp"):
    prompt("Enter local MySQL username, ", key="db_username", default="paperchase")
    prompt("What's the local MySQL database?", key="database", default="development")
    local('mysqldump -u {0} -p {1} > database_copy.sql'.format(env.db_username, env.database))
    put('database_copy.sql', path)
    with cd(path):
        prompt("What's the remote MySQL database?", key="database", default="paperchase_development")
        run('mysql --host=localhost --port=3306 --user=paperchase -p --reconnect {0} < database_copy.sql'.format(env.database))

def copy_repo_database(path = env.repo_path + "/webapp"):
    with cd(path):
        prompt("What's the MySQL database?", key="database", default="paperchase_development")
        run('mysql --host=localhost --port=3306 --user=paperchase -p --reconnect {0} < database_bootstrap.sql'.format(env.database))

def update_repo(path = env.repo_path):
    """Update the repo"""
    with cd(path):
        run("git pull")
        
def start_worker(path = env.repo_path + "/webapp"):
    with cd(path):
        run("venv/bin/supervisorctl start celeryworker")
        
def stop_worker(path = env.repo_path + "/webapp"):
    with cd(path):
        run("venv/bin/supervisorctl stop celeryworker")