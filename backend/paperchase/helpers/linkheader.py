import re

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:[^:@]+?:[^:@]*?@|)'  # basic auth
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def url(value):
    """Validate a URL.

    :param string value: The URL to validate
    :returns: The URL if valid.
    :raises: ValueError
    """
    if not regex.search(value):
        message = u"{0} is not a valid URL".format(value)
        if regex.search('http://' + value):
            message += u". Did you mean: http://{0}".format(value)
        raise ValueError(message)
    return value


def composeLinkHeader(data):
    """
    Compose a string to be returned in the response as Link
    Header: http://www.w3.org/wiki/LinkHeader

    :param dict data: A dictionary containing a set of keys and values (URLs) to be
                      included in the link header.
    :returns: A Link Header formatted string with the keys and values in the data dict.
              An empty string for an empty dict.
    """
    links = []
    for key, value in data.items():
        links.append(''.join(['<', url(value), '>; rel="', str(key), '"']))
    return ', '.join(links)
