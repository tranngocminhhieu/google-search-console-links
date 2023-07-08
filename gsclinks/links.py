import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm import tqdm

class SearchConsoleLinks():
    def __init__(self, cookies, resource_id, user_number=None):
        self.resource_id = resource_id

        if user_number == None:
            path_prefix = str()
        else:
            path_prefix = f'u/{user_number}/'
        self.url = f'https://search.google.com/{path_prefix}search-console/links/drilldown'

        self.requests = requests.Session()
        self.requests.cookies = requests.utils.cookiejar_from_dict(cookies)

    def get_links(self, params):
        res = self.requests.get(url=self.url, params=params)
        if not res.ok:
            raise ConnectionError("Too many requests, Google has blocked you temporarily, we should stop now and try again in 24 hours. If you are using get_all... functions, please set the sleep parameter larger to make sure Google won't block you")
        # Parse the content to HTML
        soup = BeautifulSoup(markup=res.content, features='html.parser')
        # Find the HTML contain data
        data = soup.find_all(name='div', attrs={'class': 'OOHai'})
        # Extract data from HTML
        contents = [div.contents[0] for div in data]
        links = [content for content in contents if type(content) != Tag]
        return links

    def get_sites(self):
        '''
        :return: a list of domains
        '''
        params = {
            'resource_id': self.resource_id,
            'type': 'DOMAIN'
        }
        sites = self.get_links(params=params)
        return sites

    def get_target_pages(self, site):
        '''
        :param site: a site as string
        :return: a list of target pages
        '''
        params = {
            'resource_id': self.resource_id,
            'type': 'DOMAIN',
            'domain': site
        }
        target_pages = self.get_links(params=params)
        return target_pages

    def get_linking_pages(self, site, target_page):
        '''

        :param site: a site as string
        :param target_page: a target page as string
        :return: a list of linking pages
        '''
        params = {
            'resource_id': self.resource_id,
            'type': 'DOMAIN',
            'target': target_page,
            'domain': site
        }
        linking_pages = self.get_links(params=params)
        return linking_pages

    def get_all_target_pages(self, sites, sleep=5):
        '''

        :param sites: a list of sites
        :param sleep: time to rest between each request sending (seconds).
        :return: a list of dict
        '''
        all_target_pages = []
        for site in tqdm(sites, desc='Get target pages'):
            target_pages = self.get_target_pages(site)
            data = [{'site': site, 'target_page': target_page} for target_page in target_pages]
            all_target_pages += data
            time.sleep(sleep)
        return all_target_pages

    def get_all_linking_pages(self, target_pages, sleep=5):
        '''

        :param target_pages: a list of dict, it is the get_all_target_pages function result
        :param sleep: time to rest between each request sending (seconds)
        :return: a list of dict
        '''
        all_linking_pages = []
        for page in tqdm(target_pages, desc='Get linking pages'):
            site = page['site']
            target_page = page['target_page']
            linking_pages = self.get_linking_pages(site=site, target_page=target_page)
            data = [{'site': site, 'target_page': target_page, 'linking_page': linking_page} for linking_page in linking_pages]
            all_linking_pages += data
            time.sleep(sleep)
        return all_linking_pages

    def get_all_links(self, sleep=10):
        '''
        The function will get sites first, then get all target pages, then get all linking pages.

        :param sleep: time to rest between each request sending (seconds)
        :return: a list of dict
        '''
        sites = self.get_sites()
        all_target_pages = self.get_all_target_pages(sites, sleep=sleep)
        all_linking_pages = self.get_all_linking_pages(all_target_pages, sleep=sleep)
        return all_linking_pages