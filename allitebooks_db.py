#!/usr/bin/python3
# Author : Mrinal Sinha

"""
    Python Script to download all the ebooks from
    'allitebooks.com' into a mysqlite database.
"""

from lxml.html          import fromstring
from requests           import get
from sqlite3            import connect
from tqdm               import tqdm
from os                 import path, makedirs

db_schema = """
    CREATE TABLE IF NOT EXISTS ebooks_index (
        category      CHAR NOT NULL,
        book_name     CHAR NOT NULL,
        cover_img     CHAR NOT NULL,
        authors       CHAR,
        isbn          CHAR,
        year          CHAR,
        pages         CHAR,
        description   CHAR,
        language      CHAR,
        file_size     CHAR,
        file_format   CHAR,
        categories    CHAR,
        download_link CHAR NOT NULL UNIQUE,
        download_file BLOB );
"""

html = get('http://www.allitebooks.com/')
html = fromstring(html.text)

conn = connect('allitebooks.db')
curs = conn.cursor()
curs.executescript(db_schema)
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

            def get_value(name, link = None):
                header_details = book.xpath('//*[@id="main-content"]/div/article/header')[0]
                if name is 'title': return (header_details.xpath('./h1/text()') or [''])[0]
                if name is 'dlink': return (book.xpath('//span[@class="download-links"]/a[contains\
                                            (@href, "file.allitebooks.com")]/@href') or [''])[0]
                if name is 'cover': return (header_details.xpath('.//div/a/img/@src') or [''])[0]
                if name is 'descr':
                    desc = book.xpath('//div[@class="entry-content"]//text()')
                    return ' '.join([x for x in [x.strip() for x in desc]])
                if link: return ', '.join([x for x in (header_details.xpath('.//*[text() = "{}"]\
                                    /following-sibling::dd[1]/a/text()'.format(name)) or [''])])
                return (header_details.xpath('.//*[text() = "{}"]/following-sibling::dd[1]//text()'.format(name)) or [''])[0]

            down = get(get_value('dlink'))
            curs.execute("INSERT OR REPLACE INTO ebooks_index \
                        (category, book_name, cover_img, authors, isbn, year, pages, description, \
                        language, file_size, file_format, categories, download_link, download_file) VALUES \
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (c_title, get_value('title'), \
                        get_value('cover'), get_value('Author:', link = True), get_value('ISBN-10:'),\
                        get_value('Year:'), get_value('Pages:'), get_value('descr'), get_value('Language:'),\
                        get_value('File size:'), get_value('File format:'), get_value('Category:', link = True),\
                        get_value('dlink'), down.content))
            conn.commit()
conn.close()