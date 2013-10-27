import re
import requests
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup

class FaviconFetcher():

    def _htc(self,m):
        return chr(int(m.group(1),16))
    
    def _url_decode(self,url):
        rex = re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
        return rex.sub(self._htc,url)
    
    def _extract_path(self,url):
        return self._url_decode(url.lstrip("/"))
    
    def _extract_domain(self,url):
        return "http://" + urlparse( self._extract_path(url) )[1]
    
    def icon_at_root(self,domain):
        root_icon_path = domain + "/favicon.ico"
        r = requests.get(root_icon_path)
        if r.status_code == 200:
            return root_icon_path
        return None
    
    def icon_in_page(self,url):
        path = self._extract_path(url) 
        r = requests.get(path) 
        if r.status_code == 200:
            page_soup = BeautifulSoup(r.content)
            page_soup_icon = page_soup.find("link",rel=re.compile("^(shortcut|icon|shortcut icon)$",re.IGNORECASE))
            if page_soup_icon:
                page_icon_href = page_soup_icon.get("href")
                if page_icon_href:
                    page_icon_path = urljoin(path,page_icon_href)
                else:
                    return None
                page_path_favicon_result = requests.get(page_icon_path)
                if page_path_favicon_result.status_code == 200:
                    return page_icon_path       
        return None
    
    def find_favicon(self,url):
        domain = self._extract_domain(url)
        candidate_url = self.icon_at_root(domain)
        if candidate_url:
            return candidate_url
        candidate_url = self.icon_in_page(domain)
        if candidate_url:
            return candidate_url
        candidate_url = self.icon_in_page(url)
        if candidate_url:
            return candidate_url
        return None