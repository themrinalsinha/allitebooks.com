#!/usr/bin/python3

from lxml.html import fromstring
from requests  import get
from tqdm      import tqdm
from csv       import writer, DictReader
from zipfile   import ZipFile, ZIP_DEFLATED

html  = get('http://www.allitebooks.com/')
html  = fromstring(html.text)
pages = int(html.xpath('//*[@id="main-content"]/div/div/a[last()]/text()')[0])

#################################################################
#      INDEXING ALL THE EBOOKS AVAILABLE INTO A CSV FILE
#################################################################

with open('books_list.csv', 'w') as csvfile:
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

with ZipFile('ebooks_allitbooks.zip', 'a', ZIP_DEFLATED) as output:
    with open('books_list.csv', 'r') as csvfile:
        reader     = DictReader(csvfile)
        for row in reader:
            b_name   = row['Download_Link']
            response = get(b_name)
            print('\rDownloading : {}'.format(b_name.split('/')[-1]), end='')
            output.writestr(b_name.split('/')[-1], response.content)