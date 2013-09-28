# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""

from flask.ext.script import Manager

from paperchase.api import create_app
from paperchase.manage import *

manager = Manager(create_app())

manager.add_command('create_user', CreateUser())
manager.add_command('delete_user', DeleteUser())

manager.add_command('create_journal',CreateJournal())
manager.add_command('delete_journal',DeleteJournal())
manager.add_command('reset_journal',ResetJournal())

manager.add_command('create_category',CreateCategory())
manager.add_command('delete_category',DeleteCategory())
manager.add_command('add_category',AddCategoryToJournal())
manager.add_command('remove_category',DeleteCategoryFromJournal())
        
manager.add_command('create_path',CreatePath())
        
manager.add_command('run_app',RunApp())
manager.add_command('run_debug',RunDebug())

if __name__ == "__main__":
    manager.run()