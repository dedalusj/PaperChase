import string
import StringIO
import getpass
from random import choice
from datetime import date

from fabric.api import *
from fabric.operations import prompt
from jinja2 import Template, Environment, FileSystemLoader


# Global settings variables
SUPERVISOR_CONF_FILE = 'supervisord.conf'
SETTINGS_FILE = 'settings.py'
ADMIN_EMAIL = 'paperchase.app@gmail.com'
MAIN_REPO = 'https://github.com/dedalusj/PaperChase.git'

env.user = 'paperchase'
env.repo_path = 'PaperChase'
env.web_app_path = env.repo_path + '/webapp'
env.db_username = 'paperchase'
env.database = 'paperchase_production'
env.local_database = 'development'
env.mail_address = ADMIN_EMAIL
env.mail_server = 'smtp.gmail.com'
env.mail_port = '465'
env.mail_use_ssl = 'True'
env.mail_username = ADMIN_EMAIL
env.virtual_env = 'venv'

# Settings specific to the deploy environment   
def vm():
    env.hosts = ['paperchasevm.local']  
    env.app_path = '/Users/' + env.user + '/' + env.repo_path
    

# Utility method to render the configuration file templates
def _render_template(template_name, context):
    env = Environment(loader = FileSystemLoader('config_templates'))
    template = env.get_template(template_name)
    return template.render(context)
    
# Setup and maintenance of the remote server
def make_dir():
    run("mkdir {0}".format(env.repo_path))

def setup_repo():
    """Original clone of the repo"""
    with cd(env.repo_path):
        run("git clone {0} .".format(MAIN_REPO))
        with cd('webapp'):
            run("mkdir log")
            
def update_repo():
    """Update the repo"""
    with cd(env.repo_path):
        run("git pull")

def setup_venv():
    with cd(env.web_app_path):
        run("curl -O https://raw.github.com/pypa/virtualenv/1.9.X/virtualenv.py")
        run("python virtualenv.py {0}".format(env.virtual_env))
        run("{0}/bin/pip install -r requirements.txt".format(env.virtual_env))
    fix_feedparser()
        
def fix_feedparser():
    with cd(env.web_app_path):
        run("mkdir temp")
        with cd("temp"):
            run("git clone https://github.com/dedalusj/feedparser.git .")
            run("mv feedparser/feedparser.py ../venv/lib/python2.7/")
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

def update_database():
    with cd(env.web_app_path):
        run("{0}/bin/alembic upgrade head".format(env.virtual_env))

def copy_local_database():
    local('mysqldump -u {0} -p {1} > database_copy.sql'.format(env.db_username, env.local_database))
    put('database_copy.sql', env.web_app_path)
    with cd(env.web_app_path):
        run('mysql --host=localhost --port=3306 --user={0} -p --reconnect {1} < database_copy.sql'.format(env,db_username, env.database))

def copy_repo_database():
    with cd(env.web_app_path):
        run('mysql --host=localhost --port=3306 --user={0} -p --reconnect {1} < database_bootstrap.sql'.format(env.db_username, env.database))

def setup_supervisor():
    with cd(env.web_app_path):
        supervisor_conf = StringIO.StringIO()
        supervisor_conf.write(_render_template(SUPERVISOR_CONF_FILE, env))
        put(supervisor_conf, SUPERVISOR_CONF_FILE)
        run("{0}/bin/supervisord".format(env.virtual_env))
        
def start_worker():
    with cd(env.web_app_path):
        run("{0}/bin/supervisorctl start celeryworker".format(env.virtual_env))
        
def stop_worker():
    with cd(env.web_app_path):
        run("{0}/bin/supervisorctl stop celeryworker".format(env.virtual_env))
        
def run_redis():
    with settings(warn_only=True):
        run('redis-server')
        
def start_app():
    with cd(env.web_app_path):
        run("{0}/bin/supervisorctl start paperchase".format(env.virtual_env))

def stop_app():
    with cd(env.web_app_path):
        run("{0}/bin/supervisorctl stop paperchase".format(env.virtual_env))
        
def initial_setup(local_data = 'False'):
    make_dir()
    setup_repo()
    setup_venv()
    setup_settings()
    
    update_database()
    if local_data == 'True':
        copy_local_database()
    else:
        copy_repo_database()
    
    run_redis()
    setup_supervisor()
    start_worker()
    start_app()
    
def update_app():
    stop_worker()
    stop_app()
    update_repo()
    udate_database()
    start_worker()
    start_app()
    