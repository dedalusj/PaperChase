# -*- coding: utf-8 -*-
"""
    keepupwithscience.tasks
    ~~~~~~~~~~~~~~

    keepupwithscience tasks module
"""

import time
import datetime
import logging
import dateutil.parser
from pytz import utc
from datetime import timedelta, date
from celery.utils.log import get_task_logger
from xml.sax import SAXException
import feedparser

from .core import mail
from .factory import create_celery_app
from .models import Journal, Paper
from .services import journals, papers
from .helpers import bozo_checker, days_since, parser_by_name
from .settings import scraper_config

celery = create_celery_app()

logger = get_task_logger(__name__)
logger.setLevel(scraper_config.get("log_level"))
# create file handler which logs even debug messages
fh = logging.FileHandler("log/tasks_{0}.log".format(date.today().isoformat()))
fh.setLevel(scraper_config.get("log_level"))
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

def feed_requester(feed_url):
    """ 
    This function handles the requesting and parsing of the journal feed. The feed is requested and parsed using feedparser. If the function is successful it will return a list of dicts for each article in the feed. If the function is not successful it shall return None.

    :param feed_url The url of the feed to retrieve.
    """
    feed_data = None
    try:
        feed_data = feedparser.parse(feed_url, agent=scraper_config.get("User-agent"))
    except SAXException as errno:
        logger.debug("Failed to retrive {0}\nTraceback:\n{1}".format(feed_url, errno))

    if not feed_data:
        logger.debug("Retriving feed from {0} returned nothing\n".format(feed_url))
        return None

    if feed_data.bozo:
        logger.info("Feed at {0}, generated bozo error: {1}.\n".format(feed_url, feed_data.bozo_exception))

        if not bozo_checker(feed_data.bozo_exception):
            return None

    return feed_data

@celery.task    
def get_journals():
    """
    Gets journals that needs to be updated from the database. The update frequency aka how many minutes between each time to request the article, is defined in the config (config.py). The method will update the last_checked column of the feed after is has put it on the queue.
    """
    # Get the unix timestamp used to filter feeds.
    # Any feed with last checked value less than this need to be updated.
    update_time = (datetime.datetime.utcnow()) - datetime.timedelta(seconds=scraper_config.get("update_frequency") * 60)

    journals_list = journals.filter(Journal.last_checked <= update_time).all()
    for journal in journals_list:
        get_papers.delay(journal.id)
        journals.update(journal, last_checked = datetime.datetime.utcnow())
        logger.debug("Updating journal last_checked: {0}".format(journal.title))

@celery.task
def get_papers(journal_id):
    journal = journals.get(journal_id)
    feed_url = journal.url
    feed_data = feed_requester(feed_url)
    if feed_data is not None and feed_data.get("entries"):
        parser_function_name = journal.parser_function
        parser_function = parser_by_name(parser_function_name)
        for entry in feed_data.entries:
            add_article.delay(entry, journal.id, parser_function)
        update_next_check.delay(journal.id, feed_data)
        if days_since(datetime.datetime.utcnow(), journal.metadata_update) >= scraper_config.get("metadata_update"):
            update_metadata.delay(journal.id, feed_data) 
   
@celery.task   
def update_next_check(journal_id, feed_data):
    journal = journals.get(journal_id)
    updateBase = feed_data.feed.get("sy_updatebase", None)
    if not updateBase:
        journals.update(journal, next_check = datetime.datetime.utcnow() - datetime.timedelta(seconds=scraper_config.get("update_frequency") * 60))
        return
    updateBase = dateutil.parser.parse(updateBase)
    updateBase = updateBase.astimezone(utc)
    
    # if the feed does not provide an updatePeriod we assume the RSS standard daily
    updatePeriod = feed_data.feed.get("sy_updateperiod", 'daily')
    updateFrequency = feed_data.feed.get("sy_updatefrequency", 1)
    
    time_to_next_check = detlatime(updatePeriod, updateFrequency)
    if not time_to_next_check:
        journals.update(journal, next_check = datetime.datetime.utcnow() + datetime.timedelta(seconds=scraper_config.get("update_frequency") * 60))
        return
    journals.update(journal, next_check = updateBase + time_to_next_check)
    journals.update(journal, last_checked = datetime.datetime.utcnow())

@celery.task         
def update_metadata(journal_id, feed_data):
    """
    This method updates the metadata of a feed, this function should be called if the feed is a feed that newly has been added to the system, or if it has been longer than n days since last update. N days is defined in the config.
    This method returns nothing.
    :param journal The journal service to change the metadata for.
    :param feed_data The resulting dict from a feed_requester call.
    """
    journal = journals.get(journal_id)
    journals.update(journal, metadata_update = datetime.datetime.fromtimestamp(time.time()))
	# Actually update the metadata
        
@celery.task
def add_article(entry, journal_id, parser_function):
    """
    Adds an article to the database. The function will check if the article already is in the DB. 
    :param article: The article to add.
    :param journal: The journal.
    :param parser_function: the parsing function for this journal
    :return: This function does not return anything.
    """
    
    # entry is simply an item out of the feed so it is guaranteed to have a link atrribute
    url = entry.get("link")
    stored_paper = papers.first(url=url)
    if stored_paper is not None:
        return
        
    paper = parser_function(entry)
    papers.create(created=paper.get("created"),
        title = paper.get("title"),
        abstract = paper.get("abstract"),
        doi = paper.get("doi"),
        url = paper.get("url"),
        authors = paper.get("authors"),
        journal_id = journal_id
    )
    logger.debug("Added new entry with doi: {0}".format(paper.get("url")))