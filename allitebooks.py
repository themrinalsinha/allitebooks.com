#!/usr/bin/python3
# Author : Mrinal Sinha

"""
Script to download all the ebooks from 'allitebooks.com'.
Use:
    python3 allitebooks.com <index, download> or blank
        index    - to generate only the index off all the files
        download - to donwload all the indexed link from CSV. (or)
        leave blank to first run the index script and then run the download
"""

from lxml.html import fromstring
from requests  import get
from tqdm      import tqdm
from csv       import writer, DictReader
from zipfile   import ZipFile, ZIP_DEFLATED
import sys

FILE_NAME = 'books_list.csv'
ZIP_NAME  = 'allitebooks_ebooks.zip'

html  = get('http://www.allitebooks.com/')
html  = fromstring(html.text)
pages = int(html.xpath('//*[@id="main-content"]/div/div/a[last()]/text()')[0])

#################################################################
#      INDEXING ALL THE EBOOKS AVAILABLE INTO A CSV FILE
#################################################################

def index():
    with open(FILE_NAME, 'w') as csvfile:
        write = writer(csvfile)
        write.writerow(['Book_Title', 'Book_Link', 'Download_Link'])
        for page in tqdm(range(pages), 'Indexing pages'):
            book = get('http://www.allitebooks.com/page/{}/'.format(page+1))
            book = fromstring(book.text)
            books_title = html.xpath('//*[@id="main-content"]//header/h2/a/text()')
            books_link  = html.xpath('//*[@id="main-content"]//header/h2/a/@href')
            downloads_l = []
            for d in tqdm(books_link, 'Fetching download links'):
                d_link = fromstring(get(d).text)
                d_link = d_link.xpath('//*[@id="main-content"]/div/article/footer/div/span/a/@href')
                downloads_l.append(d_link[0])
            for index in range(len(books_title)):
                write.writerow([books_title[index], books_link[index], downloads_l[index]])

#################################################################
#      DOWNLOADING ALL THE EBOOKS AVAILABLE FROM CSV FILE
#################################################################

def download():
    with ZipFile(ZIP_NAME, 'a', ZIP_DEFLATED) as output:
        with open(FILE_NAME, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                b_name   = row['Download_Link']
                response = get(b_name)
                print('\rDownloading : {}'.format(b_name.split('/')[-1]), end='')
                output.writestr(b_name.split('/')[-1], response.content)

if len(sys.argv) > 1:
    if sys.argv[1] == 'download': 
        download()
    elif sys.argv[1] == 'index': 
        index()
    else:
        sys.exit()
else:
    index()
    download()