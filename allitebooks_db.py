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
from os        import path, makedirs

# Helper Function
def create_path(location):
    dirname = path.dirname(path.abspath(location))
    if not path.exists(dirname):
        makedirs(dirname)
    elif not path.isdir(dirname):
        raise RuntimeError('Invalid Path "%s"' % location)

html = get('http://www.allitebooks.com/')
html = fromstring(html.text)

db_schema = """
    CREATE TABLE IF NOT EXIST ebooks_index (
        category      CHAR,
        book_name     CHAR,
        cover_img     CHAR,
        authors       CHAR,
        isbn          CHAR,
        year          CHAR,
        pages         CHAR,
        description   CHAR,
        language      CHAR,
        file_size     CHAR,
        file_format   CHAR,
        categories    CHAR,
        download_link CHAR );
"""
