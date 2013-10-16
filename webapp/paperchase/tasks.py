# -*- coding: utf-8 -*-
"""
    paperchase.tasks
    ~~~~~~~~~~~~~~

    paperchase tasks module
"""

import logging
import dateutil.parser
import time
import datetime
import feedparser
import requests
import urlparse
from pytz import utc
from datetime import timedelta, date
from celery.utils.log import get_task_logger
from xml.sax import SAXException
from xml.etree import ElementTree as ET
from lxml import etree
from bs4 import BeautifulSoup

from flask.ext.mail import Message

from .core import mail
from .factory import create_celery_app
from .services import journals, papers
from .helpers import bozo_checker, days_since, deltatime, FaviconFetcher
from .settings import scraper_config

celery = create_celery_app()

logger = get_task_logger(__name__)
# This setting will be overwritten by fabric when launching the celery beat worker
logger.setLevel(scraper_config.get("log_level"))


whitelist_tags = ['span','sup', 'em']
blacklist_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
def sanitize_html(html, whitelist_tags = [], blacklist_tags = []):
    """
    Sanitize html. It accepts a BeautifulSoup tree or a string as input. It removes the html tags and their content if they 
    appear in the blacklist_tags array and hides all other tags that don't appear in whitelist_tags.
    """
    if isinstance(html, basestring):
        html = BeautifulSoup(html)
    for tag in html.findAll(True):
        if tag.name in blacklist_tags:
            tag.decompose()
        elif tag.name not in whitelist_tags:
            tag.hidden = True
        else:
            tag.attrs = {}
    return html.renderContents()  

def is_absolute(url):
    return bool(urlparse.urlparse(url).scheme)
    
def make_absolute_url(relative_url, page_url):
    """ 
    Create an absolute url for the relative_url by extracting the domain from the page_url
    """
    parsed_uri = urlparse.urlparse(page_url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return urlparse.urljoin(domain, relative_url)

def feed_requester(feed_url):
    """ 
    This function handles the requesting and parsing of the journal feed.
    The feed is requested and parsed using feedparser. If the function is successful it 
    will return a list of dicts for each article in the feed. If the function is not
    successful it shall return None.
    
    :param feed_url: A string with the url of the feed to retrieve.
    
    :return: the feed_data in dictionary format as parsed by feedparser.
    """
    feed_data = None
    try:
        feed_data = feedparser.parse(feed_url, agent=scraper_config.get("User-agent"))
    except SAXException as errno:
        logger.error("Failed to retrive {0}\nTraceback:\n{1}".format(feed_url, errno))

    if not feed_data:
        logger.error("Retriving feed from {0} returned nothing\n".format(feed_url))
        return None

    if feed_data.bozo:
        logger.warning("Feed at {0}, generated bozo error: {1}.\n".format(feed_url, feed_data.bozo_exception))
        if not bozo_checker(feed_data.bozo_exception):
            return None

    return feed_data
    
def extract_elements(article, paths):
    """
    Scrape elements from the article webpage and insert them into the article dictionary.
    
    :param article: The article to add.
    :param paths: Paths is a dictionary containing the name of the element to parse from the webpage of the article as key and the xpath corresponding to it as value
    """
    try:
        r = requests.get(article.get("url"))
    except Exception:
        logger.error("Something went wrong while requesting webpage of article: {0}".format(article.get("title")))
        return
    
    tree = etree.HTML(r.content)
    
    for path in paths:
        elements = tree.xpath(path.path)
        if len(elements) is 0:
            logger.warning("Article at URL {0} has no element {1}".format(article.get("url"),path.path))
            continue  
        element_string = sanitize_html(ET.tostring(elements[0]), whitelist_tags, blacklist_tags) # clean_element(elements[0])
        article[path.type] = element_string.strip(' \n')

def default_parser(entry):
    """
    Parse a raw entry from the feed, as extracted by feedparser,
    and fill it with the correct information we want to keep as journal entry.
    
    :param entry: The feed entry from feedparser
    
    :return: It returns a dictionary for the article with all the keys necessary to instantiate a new article object for the database
    """
    
    article = { "title": entry.get("title", "No title"),
                "url": entry.get("link", "#"),
                "created": entry.get("dc_date",datetime.datetime.utcnow()),
                "doi": entry.get("prism_doi",""),
                "ref": entry.get("dc_source",""),
                "abstract": entry.get("summary",""),
                "authors": entry.get("authors","")
                }
    article['doi'] = article['doi'][4:]  
    authors = article['authors']
    authors = [authors[i]['name'] for i in range(len(authors))]
    authors = ', '.join(authors)
    # let's sanitize authors from unwanted html tags
    authors = sanitize_html(authors)
    authors = authors.strip(' \n')
    
    # if the authors list is to long truncate it to 900 chars
    article['authors'] = (authors[:900] + '..') if len(authors) > 900 else authors
      
    return article

@celery.task    
def get_journals():
    """
    Gets journals that needs to be updated from the database. 
    The update frequency aka how many minutes between each time to 
    request the article, is defined in the config (config.py). 
    The method will update the last_checked column of the feed after is has 
    put it on the queue.
    """
    journals_list = journals.filter(journals.model().next_check <= datetime.datetime.utcnow()).all()
    for journal in journals_list:
        get_papers.delay(journal.id)

@celery.task
def get_papers(journal_id):
    """
    Fetch the papers, RSS feed, of a journal.
    
    :param journal_id: the id of the journal
    """
    journal = journals.get(journal_id)
    logger.debug("Getting papers for journal: {0}".format(journal.title))
    
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
    """
    Update the time of the next feed refresh for a journal using its fetched RSS feed.
    
    :param journal_id: the id of the journal
    :param feed_data: the RSS feed data of the journal used to compute the next refresh time
    """
    journal = journals.get(journal_id)
    logger.debug("Updating last_checked for journal: {0}".format(journal.title))
    journals.update(journal, last_checked = datetime.datetime.utcnow())
    
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

@celery.task         
def update_metadata(journal_id, feed_data):
    """
    This method updates the metadata of a journal, this function should be called if 
    the feed is newly added, or if it has been longer than N days since last 
    update. N days is defined in the config.
    
    :param journal_id: the id of the journal
    :param feed_data: The resulting dict from a feed_requester call.
    """
    journal = journals.get(journal_id)
    logger.debug("Updating metadata for journal: {0}".format(journal.title))
    paper = papers.first(journal_id=journal_id)
    if paper:
        paper_url = paper.url
        favicon_url = FaviconFetcher().find_favicon(paper_url)
        if favicon_url is not None:
            journals.update(journal, favicon = favicon_url)
        else:
            logger.wrarning("Can't find favicon at URL {1} for journal {0}".format(journal.title,paper_url))
        
    journals.update(journal, metadata_update = datetime.datetime.utcnow())
        
@celery.task
def add_article(entry, journal_id):
    """
    Adds an article to the database. The function will 
    check if the article already is in the DB. 
    
    :param entry: the data of the article
    :param journal_id: the id of the journal
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
    
@celery.task
def send_suggestion_email(json_msg):
    msg = Message('Journal suggestion', sender='dedalusj@gmail.com', recipients=['dedalusj@gmail.com'])
    msg.body = """{0}""".format(str(json_msg))
    mail.send(msg)