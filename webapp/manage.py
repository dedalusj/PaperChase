# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""

from flask.ext.script import Manager

from keepupwithscience.api import create_app
from keepupwithscience.manage import CreateJournalCommand, DeleteJournalCommand, ResetJournalCommand, ListJournalsCommand, CreateCategoryCommand, DeleteCategoryCommand, ListCategoriesCommand, ListJournalCategoriesCommand, AddCategoriesToJournalCommand, DeleteCategoryFromJournalCommand

manager = Manager(create_app())
manager.add_command('create_journal', CreateJournalCommand())
manager.add_command('delete_journal', DeleteJournalCommand())
manager.add_command('reset_journal', ResetJournalCommand())
manager.add_command('list_journals', ListJournalsCommand())
manager.add_command('create_category', CreateCategoryCommand())
manager.add_command('delete_category', DeleteCategoryCommand())
manager.add_command('list_categories', ListCategoriesCommand())
manager.add_command('list_journal_categories', ListJournalCategoriesCommand())
manager.add_command('add_categories_to_journal', AddCategoriesToJournalCommand())
manager.add_command('delete_category_from_journal', DeleteCategoryFromJournalCommand())

if __name__ == "__main__":
    manager.run()