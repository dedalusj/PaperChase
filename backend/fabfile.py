import string
import StringIO
import getpass
from random import choice

from fabric.api import *
from jinja2 import Environment, FileSystemLoader


# Global settings variables
SUPERVISOR_CONF_FILE = 'supervisord.conf'
SETTINGS_FILE = 'settings.py'
ADMIN_EMAIL = 'paperchase.app@gmail.com'
MAIN_REPO = 'https://github.com/dedalusj/PaperChase.git'

# HOST_CONF_FILE = 'nginx.conf'
# REMOTE_NGINX_PATH = '/usr/local/etc/nginx/nginx.conf'

env.user = 'paperchase'
env.repo_path = 'PaperChase'
env.backend_path = env.repo_path + '/backend'
env.db_username = 'paperchase'
env.database = 'paperchase_production'
env.local_database = 'development'
env.mail_address = ADMIN_EMAIL
env.mail_server = 'smtp.gmail.com'
env.mail_port = '465'
env.mail_use_ssl = 'True'
env.mail_username = ADMIN_EMAIL
env.virtual_env = 'venv'
env.domain = 'dedalusj.dyndns.org'
env.app_name = 'paperchase'


# Settings specific to the deploy environment
def macVM():
    env.hosts = ['paperchasevm.local']
    env.app_path = '/Users/' + env.user + '/' + env.repo_path


def cubietruck():
    env.hosts = ['192.168.1.5']
    env.app_path = '/home/' + env.user + '/' + env.repo_path


# Utility method to render the configuration file templates
def _render_template(template_name, context):
    env = Environment(loader=FileSystemLoader('config_templates'))
    template = env.get_template(template_name)
    return template.render(context)


# Setup and maintenance of the remote server
def make_dir():
    run("mkdir {0}".format(env.repo_path))


def setup_repo():
    """Original clone of the repo"""
    with cd(env.repo_path):
        run("git clone {0} .".format(MAIN_REPO))
        run("mkdir log")  # create the main log dir
    # with cd(env.backend_path):
    #     run("mkdir log")  # create the backend log dir


def update_repo():
    """Update the repo"""
    with cd(env.repo_path):
        run("git pull")


def setup_venv():
    """Setup the python virtual environment"""
    with cd(env.backend_path):
        # run("curl -O https://raw.github.com/pypa/virtualenv/" +
        # "1.9.X/virtualenv.py")
        run("virtualenv {0}".format(env.virtual_env))
        run("{0}/bin/pip install -r requirements-production.txt".format(env.virtual_env))
    fix_feedparser()


def fix_feedparser():
    """Download a patch for feedparser that fix a bug with parsing authors"""
    with cd(env.backend_path + "/" + env.virtual_env + "/lib/python2.7/" +
            "site-packages/"):
        run("curl -O https://raw.github.com/dedalusj/feedparser/master/" +
            "feedparser/feedparser.py")


def prompt_for_settings():
    db_pass = getpass.getpass(
        prompt='Enter the paperchase user password for the database, ')
    env.db_password = db_pass
    mail_pass = getpass.getpass(
        prompt='Enter a password for the mail service, ')
    env.mail_password = mail_pass


def compile_settings():
    prompt_for_settings()
    path = env.backend_path + "/paperchase"
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
    with cd(env.backend_path):
        run("{0}/bin/alembic upgrade head".format(env.virtual_env))


def copy_local_database():
    """
    Dump the database state from the development environment and load it onto
    the production environment.
    """
    local('mysqldump -u {0} -p {1} > database_copy.sql'.format(
        env.db_username, env.local_database))
    put('database_copy.sql', env.backend_path)
    with cd(env.backend_path):
        run("mysql --host=localhost --port=3306 --user={0} -p --reconnect {1}"
            " < database_copy.sql".format(
            env, db_username, env.database))


def copy_repo_database():
    """Load the minimal database file from the repository into the production database"""
    with cd(env.backend_path):
        run("mysql --host=localhost --port=3306 --user={0} -p --reconnect {1}" +
            " < database_bootstrap.sql".format(
            env.db_username, env.database))


def setup_supervisor():
    with cd(env.backend_path):
        supervisor_conf = StringIO.StringIO()
        supervisor_conf.write(_render_template(SUPERVISOR_CONF_FILE, env))
        put(supervisor_conf, SUPERVISOR_CONF_FILE)
        run("{0}/bin/supervisord".format(env.virtual_env))


def reload_supervisor():
    with cd(env.backend_path):
        run('{0}/bin/supervisorctl update'.format(env.virtual_env))


def start_worker():
    with cd(env.backend_path):
        run("{0}/bin/supervisorctl start celeryworker".format(env.virtual_env))


def stop_worker():
    with cd(env.backend_path):
        run("{0}/bin/supervisorctl stop celeryworker".format(env.virtual_env))


def start_app():
    with cd(env.backend_path):
        run("{0}/bin/supervisorctl start paperchase".format(env.virtual_env))


def stop_app():
    with cd(env.backend_path):
        run("{0}/bin/supervisorctl stop paperchase".format(env.virtual_env))


def initial_setup(local_data='False'):
    make_dir()
    setup_repo()
    setup_venv()
    compile_settings()
    update_database()
    if local_data == 'True':
        copy_local_database()
    else:
        copy_repo_database()
    setup_supervisor()


def update_app():
    stop_worker()
    stop_app()
    update_repo()
    compile_settings()
    update_database()
    reload_supervisor()
    start_worker()
    start_app()
