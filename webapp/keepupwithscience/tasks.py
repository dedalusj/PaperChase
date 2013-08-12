# -*- coding: utf-8 -*-
"""
    keepupwithscience.tasks
    ~~~~~~~~~~~~~~

    keepupwithscience tasks module
"""

import logging
import dateutil.parser
from pytz import utc
import time
import datetime
from datetime import timedelta, date
from celery.utils.log import get_task_logger
import feedparser
import requests
from xml.sax import SAXException
from lxml import etree
from xml.etree import ElementTree as ET

from .core import mail
from .factory import create_celery_app
from .models import Journal, Paper
from .services import journals, papers
from .helpers import bozo_checker, days_since, deltatime
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

def content(tag):
    return tag.text + ''.join(ET.tostring(e) for e in tag)

def clean_element(tree_element):
    """
    Format an xml node element. It makes the node a paragraph node, remove all link tags (for now later maybe more) and remove all attributes  
        
    :param tree_element: The element to format. tree_element must be an instance of etree._Element

    :return: This function does not return anything.
    """
    try:
        tree_element.tag = 'p'
        # remove link tags from an element and maybe other things in the future
        etree.strip_tags(tree_element,'a')
        for attr in tree_element.keys():
            del tree_element.attrib[attr]
    except Exception:
        logger.error("Something went wrong while cleaning element: {0}".format(tree_element))
    
def extract_elements(article, paths):
    """
    Scrape elements from the article webpage and insert them into the article dictionary  
        
    :param article: The article to add.
    
    :param paths: Paths is a dictionary containing the name of the element to parse from the webpage of the article as key and the xpath corresponding to it as value
    
    :return: This function does not return anything.
    """
    try:
        r = requests.get(article.get("url"))
    except Exception:
        logger.error("Something went wrong while requesting webpage of article: {0}".format(article.get("title")))
        return
    
    tree = etree.HTML(r.content)
    for path in paths:
        try:
            elements = tree.xpath(path.path)
            if len(elements) is 0:
                logger.warning("Article at URL {0} has no element {1}".format(article.get("url"),path.path))
                continue  
            element = elements[0]
            clean_element(element)
            article[path.type] = content(element)
        except Exception:
            logger.error("Something went wrong while extracting path {0} from URL ".format(path.path,article.get("url")))
            continue

def default_parser(entry):
    """
        Parse a raw entry from the feed, as extracted by feedparser, and fill it with the correct information we want to keep as journal entry
                    
        :param entry: The feed entry from feedparser
    
        :return: It returns a dictionary for the article with all the keys necessary to instantiate a new article object for the database
    """
    
    article = { "title": entry.get("dc_title", "No title"),
                "url": entry.get("link", "#"),
                "created": entry.get("dc_date",datetime.datetime.utcnow()),
                "doi": entry.get("dc_identifier",""),
                "ref": entry.get("dc_source",""),
                "abstract": entry.get("summary",""),
                "authors": entry.get("authors","")
                }
    article['doi'] = article['doi'][4:]  
    authors = [authors[i]['name'] for i in range(len(authors))]
    authors = ', '.join(authors)           
    return article

@celery.task    
def get_journals():
    """
    Gets journals that needs to be updated from the database. The update frequency aka how many minutes between each time to request the article, is defined in the config (config.py). The method will update the last_checked column of the feed after is has put it on the queue.
    """
    journals_list = journals.filter(Journal.next_check <= datetime.datetime.utcnow()).all()
    for journal in journals_list:
        get_papers.delay(journal.id)
        logger.debug("Updating journal last_checked: {0}".format(journal.title))

@celery.task
def get_papers(journal_id):
    journal = journals.get(journal_id)
    feed_url = journal.url
    feed_data = feed_requester(feed_url)
    if feed_data is not None and feed_data.get("entries"):
        for entry in feed_data.entries:
            add_article.delay(entry, journal.id)
        update_check.delay(journal.id, feed_data)
        if days_since(datetime.datetime.utcnow(), journal.metadata_update) >= scraper_config.get("metadata_update"):
            update_metadata.delay(journal.id, feed_data) 
   
@celery.task   
def update_check(journal_id, feed_data):
    journal = journals.get(journal_id)
    updateBase = feed_data.feed.get("sy_updatebase", None)
    if not updateBase:
        journals.update(journal, next_check = datetime.datetime.utcnow() - datetime.timedelta(seconds=scraper_config.get("update_frequency") * 60))
        return
    updateBase = dateutil.parser.parse(updateBase)
    updateBase = updateBase.astimezone(utc)
    updateBase = updateBase.replace(tzinfo=None)
    
    # if the feed does not provide an updatePeriod we assume the RSS standard daily
    updatePeriod = feed_data.feed.get("sy_updateperiod", 'daily')
    updateFrequency = feed_data.feed.get("sy_updatefrequency", 1)
    
    time_between_updates = deltatime(updatePeriod, updateFrequency)
    if not time_between_updates:
        journals.update(journal, next_check = datetime.datetime.utcnow() + datetime.timedelta(seconds=scraper_config.get("update_frequency") * 60))
        return
        
    seconds_from_updateBase = datetime.datetime.utcnow() - updateBase
    seconds_to_next_update = time_between_updates.total_seconds() - seconds_from_updateBase.total_seconds() % time_between_updates.total_seconds()
    journals.update(journal, next_check = datetime.datetime.utcnow() + timedelta(seconds=seconds_to_next_update))
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
    try:
        paper_url = papers.first(journal_id=journal_id).url
        paper_page = requests.get(paper_url)
        tree = etree.html(paper_page.content)
        favicon_url = tree.xpath('//link[@rel="icon" or @rel="shortcut icon"]/@href')
        journals.update(journal, favicon = favicon_url[0])
    except Exception:
        logger.error("The journal {0} at URL {1} does not have a favicon".format(jorunal.title,paper_url))
        
    journals.update(journal, metadata_update = datetime.datetime.utcnow())
	
        
@celery.task
def add_article(entry, journal_id):
    """
    Adds an article to the database. The function will check if the article already is in the DB. 
    :param article: The article to add.
    :param journal: The journal.
    :return: This function does not return anything.
    """
    
    # entry is simply an item out of the feed so it is guaranteed to have a link atrribute
    url = entry.get("link")
    stored_paper = papers.first(url=url)
    if stored_paper is not None:
        return
        
    paper = default_parser(entry)
    journal = journals.get(journal_id)
    paths = journal.paths.all()
    extract_elements(paper, paths)
    papers.create(created=paper.get("created"),
        title = paper.get("title"),
        abstract = paper.get("abstract"),
        doi = paper.get("doi"),
        ref = paper.get("ref"), 
        url = paper.get("url"),
        authors = paper.get("authors"),
        journal_id = journal_id
    )
    logger.debug("Added new entry with doi: {0}".format(paper.get("url")))