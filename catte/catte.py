from http.client import HTTPException
import re
import sqlite3
import time
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

def get_posts(page):
    print("Getting posts...")
    soup = BeautifulSoup(page, from_encoding="iso-8859-1")
    posts = soup.find_all('table', id=re.compile("post[0-9]+"))
    if len(posts) != 40:
        print("Broken page")
        return None
    print("Got posts")
    return posts

def parse_posts(posts):
    print("Parsing posts...")
    images = []
    for post in posts:
        body = post.find('td', attrs={'class': 'postbody'})
        for link in body.find_all('a'):
            images.append(link['href'])
        for image in body.find_all('img'):
            images.append(image['src'])
    sanitized_images = []
    for image in images:
        if re.search('i\.somethingawful\.com', image) is not None:
            continue
        if re.search('youtube\.com', image) is not None:
            continue
        if re.match('http', image) is None:
            sanitized_images.append('http://forums.somethingawful.com/' + image)
        else:
            sanitized_images.append(image)
    for image in sanitized_images:
        print("Processing image " + image)
        row = db.execute('select * from raw_images where image_url=:image_url', {'image_url': image}).fetchone()
        if row is not None:
            print("Image already in database")
            continue
        row = db.execute('select attempt_count from deferred_images where image_url=:image_url', {'image_url': image}).fetchone()
        attempts = 0
        found = True
        if row is not None:
            attempts = row[0]
        if attempts == 5:
            print("Image permanently deferred")
            continue
        try:
            time.sleep(5)
            response = urlopen(image)
            if response.info().get_content_maintype() != 'image':
                found = False
        except (URLError, HTTPException):
            found = False
        if found is False:
            print("Image temporarily deferred")
            if attempts != 0:
                db.execute('update deferred_images set attempt_count=:attempt_count where image_url=:image_url', {'attempt_count': (attempts + 1), 'image_url': image})
            else:
                db.execute('insert into deferred_images (image_url, attempt_count) values (:image_url, :attempt_count)', {'image_url': image, 'attempt_count': 1})
            db.commit()
        else:
            print("Adding image to database")
            db.execute('insert into raw_images (image_url, image_data) values (:image_url, :image_data)', {'image_url': image, 'image_data': response.read()})
            db.commit()

print("Starting the catte parser")
db = sqlite3.connect('catte.db')
pages = db.execute('select page_data from raw_pages').fetchall()
print(str(len(pages)) + " pages already in database")
for page in pages:
    parse_posts(get_posts(page[0]))
last_page = len(pages)
for x in range(10):
    print("Grabbing page " + str(last_page + 1))
    try:
        response = urlopen('http://forums.somethingawful.com/showthread.php?threadid=3201527&userid=0&perpage=40&pagenumber=' + str(last_page + 1))
    except URLError:
        print("URLError when grabbing page")
        quit()
    raw_page = response.read()
    posts = get_posts(raw_page)
    if posts is None:
        quit()
    print("Adding page to database")
    db.execute('insert into raw_pages (page_data) values (:page_data)', {'page_data': raw_page})
    db.commit()
    parse_posts(posts)
    last_page += 1

