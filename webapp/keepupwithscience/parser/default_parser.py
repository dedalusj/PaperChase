import datetime
import time
import requests
from lxml import etree
from xml.etree import ElementTree as ET
from ..tasks import logger


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
    for key, value in paths.iteritems():
        try:
            elements = tree.xpath(value)
            if len(elements) is 0:
                logger.warning("Article at URL {0} has no element {1}".format(article.get("url"),value))
                continue  
            element = elements[0]
            clean_element(element)
            article[key] = content(element)
        except Exception:
            logger.error("Something went wrong while extracting path {0} from URL ".format(value,article.get("url")))
            continue

def default_parser(entry):
    """
        Parse a raw entry from the feed, as extracted by feedparser, and fill it with the correct information we want to keep as journal entry
                    
        :param entry: The feed entry from feedparser
    
        :return: It returns a dictionary for the article with all the keys necessary to instantiate a new article object for the database
    """
    if entry.get("updated_parsed"):
        created = datetime.datetime.fromtimestamp(time.mktime(entry.get("updated_parsed")))
    else:
        created = datetime.datetime.utcnow()
        
    article = { "title": entry.get("title", "No title"),
                "url": entry.get("link", "#"),
                "created": created,
                "doi": entry.get("prism_doi",""),
                "abstract": entry.get("summary",""),
                "authors": entry.get("author","")
                }
                    
    return article