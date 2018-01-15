#!/usr/bin/python3
# Author : Mrinal Sinha

"""
    Python Script to download all the ebooks from 
    'allitebooks.com' into a mysqlite database.
"""

from lxml.html import fromstring
from requests  import get
from sqlite3   import connect
from tqdm      import tqdm

html = get('http://www.allitebooks.com/')
html = fromstring(html.text)

