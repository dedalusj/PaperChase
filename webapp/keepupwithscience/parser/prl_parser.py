from .default_parser import default_parser, clean_element, extract_elements

def prl_parser(entry):
    """
        Parse a raw entry from the feed, as extracted by feedparser, and fill it with the correct information we want to keep as journal entry
                    
        :param entry: The feed entry from feedparser
    
        :return: It returns a dictionary for the article with all the keys necessary to instantiate a new article object for the database
    """
    article = default_parser(entry)
    
    paths = {'abstract': '//div[@class="aps-abstractbox"]/p'}
    
    extract_elements(article, paths)
    
    return article