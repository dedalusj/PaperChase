import string
import StringIO
import getpass
from random import choice
from datetime import date

from fabric.api import *
from fabric.operations import prompt
from jinja2 import Template, Environment, FileSystemLoader

env.user = 'paperchase'
env.repo_path = 'PaperChase'
env.web_app_path = env.repo_path + '/webapp'
env.db_username = 'paperchase'
env.database = 'paperchase_development'
env.local_database = 'development'
env.mail_address = 'dedalusj@gmail.com'
env.mail_server = 'smtp.gmail.com'
env.mail_port = '465'
env.mail_use_ssl = 'True'
env.mail_username = 'dedalusj@gmail.com'

SUPERVISOR_CONF_FILE = 'supervisord.conf'
SETTINGS_FILE = 'settings.py'

prompt("Enter a password for the mail service, ", key="mail_password")

def _render_template(template_name, context):
    env = Environment(loader = FileSystemLoader('config_templates'))
    template = env.get_template(template_name)
    return template.render(context)

# Define host names for inside and outside the LAN
def inside():
    env.hosts = ['brick.local']

def outside():
    env.hosts = ['dedalusj.dyndns.org']
    
def vm():
    env.hosts = ['paperchasevm.local']  
    env.app_path = '/Users/' + env.user + '/' + env.repo_path
    
# Setup and maintenance of the remote server
def make_dir():
    run("mkdir {0}".format(env.repo_path))

def setup_repo():
    """Original clone of the repo"""
    with cd(env.repo_path):
        run("git clone https://github.com/dedalusj/PaperChase.git .")
        with cd('webapp'):
            run("mkdir log")
            
def update_repo():
    """Update the repo"""
    with cd(env.repo_path):
        run("git pull")

def setup_venv():
    with cd(env.web_app_path):
        run("curl -O https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py")
        run("python virtualenv.py venv")
        run("venv/bin/pip install -r requirements.txt")
    fix_feedparser(path)
        
def fix_feedparser():
    with cd(env.web_app_path):
        run("mkdir temp")
        cd("temp")
        run("git clone https://github.com/dedalusj/feedparser.git .")
        run("mv feedparser/feedparser.py ../venv/lib/python2.7/")
        cd("..")
        run("rm -fdr temp")
        
def prompt_for_settings():
    db_pass = getpass.getpass(prompt='Enter the paperchase user password for the database, ')
    env.db_password = db_pass
    mail_pass = getpass.getpass(prompt='Enter a password for the mail service, ')
    env.mail_password = mail_pass

def setup_settings():
    prompt_for_settings()
    path = env.web_app_path + "/paperchase"
    with cd(path):
        chars = string.letters + string.digits
        length = 10
        env.secret_key = ''.join(choice(chars) for _ in range(length))
        length = 22
        env.password_salt = ''.join(choice(chars) for _ in range(length))
        
        settings = StringIO.StringIO()
        settings.write(_render_template(SETTINGS_FILE, env))
        put(settings, SETTINGS_FILE)
        
def copy_settings():
    local_path="paperchase"
    remote_path = env.web_app_path + "/paperchase"
    local_file = local_path + "settings.py"
    remote_file = remote_path + "settings.py"
    put(local_file,remote_file)

def update_database():
    with cd(env.web_app_path):
        run("venv/bin/alembic upgrade head")

def copy_local_database():
    local('mysqldump -u {0} -p {1} > database_copy.sql'.format(env.db_username, env.local_database))
    put('database_copy.sql', env.web_app_path)
    with cd(env.web_app_path):
        run('mysql --host=localhost --port=3306 --user=paperchase -p --reconnect {0} < database_copy.sql'.format(env.database))

def copy_repo_database():
    with cd(env.web_app_path):
        run('mysql --host=localhost --port=3306 --user=paperchase -p --reconnect {0} < database_bootstrap.sql'.format(env.database))

def setup_supervisor():
    with cd(env.web_app_path):
        supervisor_conf = StringIO.StringIO()
        supervisor_conf.write(_render_template(SUPERVISOR_CONF_FILE, env))
        put(supervisor_conf, SUPERVISOR_CONF_FILE)
        run("venv/bin/supervisord")
        
def start_worker():
    with cd(env.web_app_path):
        run("venv/bin/supervisorctl start celeryworker")
        
def stop_worker():
    with cd(env.web_app_path):
        run("venv/bin/supervisorctl stop celeryworker")
        
def run_redis():
    with settings(warn_only=True):
        run('redis-server')
        
def start_app():
    with cd(env.web_app_path):
        run("venv/bin/supervisorctl start paperchase")

def stop_app():
    with cd(env.web_app_path):
        run("venv/bin/supervisorctl stop paperchase")
        