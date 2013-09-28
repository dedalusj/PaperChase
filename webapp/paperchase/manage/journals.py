# -*- coding: utf-8 -*-
"""
    paperchase.manage.journals
    ~~~~~~~~~~~~~~~~~~~~~

    jorunals management commands
"""

import datetime
from flask.ext.script import Command, prompt
from werkzeug.datastructures import MultiDict

from ..services import journals, categories, paths

def find_journal():
    keyword = prompt('Journal identifier')
    journal = journals.first(title=keyword)
    if journal:
        return journal
    journal = journals.first(short_title=keyword)
    if journal:
        return journal
    journal = journals.first(url=keyword)
    if journal:
        return journal
    return None

class CreateJournal(Command):
    """Create a journal"""

    def run(self):
        title = prompt('Title')
        short_title = prompt('Short title')
        url = prompt('URL')
        journal = journals.create( title = title, short_title = short_title, url = url, last_checked = datetime.datetime.utcnow(), next_check = datetime.datetime.utcnow(), metadata_update = datetime.datetime.utcnow() )
        print '\nJournal created successfully'
        print 'Journal(id=%s title=%s)' % (journal.id, journal.title)

class DeleteJournal(Command):
    """Delete a journal"""

    def run(self):
        journal = find_journal()
        if not journal:
            print 'Invalid journal'
            return
        jorunals.delete(journal)
        print 'Journal deleted successfully'
        
class ResetJournal(Command):
    """Reset the last_checked and metadata_update field of a journal"""
    
    def run(self):
        journal = find_journal()
        if not journal:
            print 'Invalid journal'
            return
        journals.update(journal,last_checked=datetime.datetime.datetime(year=2013,month=1,day=1))
        journals.update(journal,metadata_update=datetime.datetime.datetime(year=2013,month=1,day=1))
        print 'Journal reset'
            
class CreateCategory(Command):
    """Create a category"""

    def run(self):
        name = prompt('Name')
        description = prompt('Description')
        category = categories.create( name = name, description = description )
        print '\nCategory created successfully'
        print 'Category(id=%s name=%s)' % (category.id, category.name)

class DeleteCategory(Command):
    """Delete a category"""

    def run(self):
        name = prompt('Name')
        category = categories.first(name=name)
        if not category:
            print 'Invalid category'
            return
        categories.delete(category)
        print 'Category deleted successfully'
            
class AddCategoryToJournal(Command):
    """Add categories to a journal"""

    def run(self):
        journal = find_journal()
        if not journal:
            print 'Invalid journal'
            return
        
        name = prompt('Category name')
        category = categories.first(name=name)
        if not category:
            create_new = prompt('Category does not exist do you want to create it? (y/n)')
            if create_new is 'y':
                description = prompt('Description')
                category = categories.create( name = name, description = description )
            else:
                print 'Invalid category'
                return
            
        journal.categories.append(category)
        journals.save(journal)
        print 'Category added to journal succesfully'
        
            
class DeleteCategoryFromJournal(Command):
    """Remove a category from a journal"""

    def run(self):
        journal = find_journal()
        if not journal:
            print 'Invalid journal'
            return
        
        name = prompt('Category name')
        category = journal.categories.filter(name==name).one()
        if not category:
            print 'Invalid category'
            return
            
        journal.categories.remove(category)
        journals.save(journal)
        print 'Category remove from journal succesfully'
        
class CreatePath(Command):
    """Create a path"""

    def run(self):
        journal = find_journal()
        if not journal:
            print 'Invalid journal'
            return
        type = prompt('Type')
        path = prompt('Path')
        path = paths.create( type = type, path = path, journal_id = journal.id )
        print '\nPath created successfully'
        print 'Path(id=%s)' % (path.id)