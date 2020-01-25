#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:11:38 2020

@author: liam
"""

from justwatch import JustWatch
import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
import time
just_watch = JustWatch(country='US')

# <codecell>

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# <codecell>
pages = 20

df = pd.DataFrame(columns = ["Title","Metascore"])

for page in range(0,pages):
    
    url = 'http://www.metacritic.com/browse/movies/score/metascore/all/filtered?page=' + str(page)
    movies = requests_retry_session().get(url, headers = headers)
        
    metacritic_content = BeautifulSoup(movies.content, 'html.parser')
    container = metacritic_content.find_all('td', class_ = 'clamp-summary-wrap')
    idx = 0
    for movie in container:
        print(idx)
        idx = idx + 1
        title = movie.find('h3').text
        results = just_watch.search_for_item(query = title, providers = ['nfx'], content_types = ['movie'])
        if results['items']:
            if results['items'][0]['title'] == title:
                metascore = movie.select('a.metascore_anchor div')[0].text
                df = df.append({"Title" : title, "Metascore" : metascore}, ignore_index = True)
    df.to_csv('file.csv',index=False)
    
