# -*- coding: utf-8 -*-
"""
    paperchase.settings
    ~~~~~~~~~~~~~~~

    paperchase settings module
"""

from datetime import timedelta
import logging

scraper_config = {
    "User-agent": "paperchase-v{0}".format(0.01),

    # How often to look for updates in minutes
    "update_frequency": 5,

    # How often to update the metadata information about a feed in days.
    "metadata_update": 1,

    "log_level": logging.WARNING,
}

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = '{{ secret_key }}'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{{ db_username }}:{{ db_password }}'\
                          '@localhost:3306/{{ database }}?charset=utf8'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ALWAYS_EAGER = False
CELERYBEAT_SCHEDULE = {
    'refresh-journals': {
        'task': 'paperchase.tasks.get_journals',
        'schedule': timedelta(minutes=scraper_config.get("update_frequency"))
    },
}

PASSWORD_SALT = '{{ password_salt }}'

MAIL_DEFAULT_SENDER = '{{ mail_address }}'
MAIL_SERVER = '{{ mail_server }}'
MAIL_PORT = {{ mail_port }}
MAIL_USE_SSL = {{ mail_use_ssl }}
MAIL_USERNAME = '{{ mail_username }}'
MAIL_PASSWORD = '{{ mail_password }}'

DOMAIN = '{{ domain }}'

# The time limit for article to import when a user subscribe
# to a new journal. This number is in units of weeks and counts
# from the time of subscription backwards
SUBSCRIPTION_IMPORT = 2
