# -*- coding: utf-8 -*-
"""
    paperchase.manage.journals
    ~~~~~~~~~~~~~~~~~~~~~

    jorunals management commands
"""

import datetime
from flask.ext.script import Command, prompt, prompt_pass
from werkzeug.datastructures import MultiDict

from ..services import users

class CreateUser(Command):
    """Create a new user"""

    def run(self):
        email = prompt('email')
        password = prompt('password')
        user = users.create( email = email, password = password, registered_at = datetime.datetime.utcnow(), active = True, confirmed_at = datetime.datetime.utcnow())
        print '\nUser created successfully'
        print 'User(id=%s email=%s)' % (user.id, user.title)

class DeleteUser(Command):
    """Delete a user"""

    def run(self):
        email = prompt('User email')
        user = users.first(email = email)
        if not user:
            print 'Invalid user email'
            return
        users.delete(user)
        print 'User deleted successfully'