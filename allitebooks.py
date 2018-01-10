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

#################################################################
#      INDEXING ALL THE EBOOKS AVAILABLE INTO A CSV FILE
#################################################################

def index():
    with open(FILE_NAME, 'w') as csvfile:
        write = writer(csvfile)
        write.writerow(['Category', 'Title', 'Author(s)', 'ISBN', 'Year', 'Cover_Image', 'Description',
                        'Pages', 'Categories', 'Language', 'File_Size', 'File_Format', 'Download_Link'])

        categories_title = html.xpath('//*[@id="side-content"]/ul/li/a/text()')
        categories_link  = html.xpath('//*[@id="side-content"]/ul/li/a/@href')
        category         = dict(zip(categories_title, categories_link))

        for c_title, link in tqdm(category.items(), 'Categories'):
            category_html = get(link)
            category_html = fromstring(category_html.text)
            pages = int(category_html.xpath('//*[@id="main-content"]/div/div/a[last()]/text()')[0])
            
            for page in tqdm(range(pages), c_title):
                books = get(link + 'page/{}/'.format(page+1))
                books = fromstring(books.text)
                books_link = books.xpath('//*[@id="main-content"]//header/h2/a/@href')
                
                for each_book in tqdm(books_link, 'Page - {}'.format(page+1)):
                    book = get(each_book)
                    book = fromstring(book.text)

                    # Getting book details.
                    book_category    = title
                    book_title       = book.xpath('//*[@id="main-content"]/div/article/header/h1/text()')[0]
                    book_description = (book.xpath('//*[@class="entry-content"]/p[1]/text() | \
                                                    //*[@class="entry-content"]/div[1]/text()') or [None])[0]
                    book_image       = (book.xpath('//*[@id="main-content"]/div/article/header/div/div[1]/a/img/@src') or [None])[0]
                    book_author      = (book.xpath('//*[@id="main-content"]//div[@class="book-detail"]//dd[1]/a/text()') or [None])
                    book_author      = ', '.join(x for x in book_author) if len(book_author) > 1 else (book_author[0] or [None])
                    book_isbn        = (book.xpath('//*[@id="main-content"]//div[@class="book-detail"]//dd[2]/text()') or [None])[0]
                    download_link    = (book.xpath('//*[@id="main-content"]//span[@class="download-links"][1]/a/@href') or [None])[0]

                    write.writerow([book_category, book_title, book_description, book_image, book_author, book_isbn, download_link])

#################################################################
#      DOWNLOADING ALL THE EBOOKS AVAILABLE FROM CSV FILE
#################################################################

def download():
    files = ZipFile(ZIP_NAME).namelist()
    with ZipFile(ZIP_NAME, 'a', ZIP_DEFLATED) as output:
        with open(FILE_NAME, 'r') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                b_name    = row['Download_Link']
                response  = get(b_name)
                file_name = b_name.split('/')[-1]
                if file_name not in files:
                    print('\rDownloading : {}'.format(file_name), end='')
                    output.writestr(b_name.split('/')[-1], response.content)
                else:
                    print('\rSkipping : {}'.format(file_name), end='')

if len(sys.argv) > 1:
    if sys.argv[1] == 'download': 
        download()
    elif sys.argv[1] == 'index': 
        index()
    else:
        sys.exit(1)
else:
    index()
    download()