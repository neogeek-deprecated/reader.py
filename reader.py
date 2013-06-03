import pickle

from hashlib import sha256
from urlparse import urlparse
from xml.dom import minidom

from fetch_remote_file import *


class Reader():

    expire = 0

    feeds = []
    hashes = []
    stories = []

    def __init__(self, expire=15):

        if os.path.isfile('cache/hashes.dict') and os.path.isfile('cache/stories.dict'):

            self.hashes = pickle.load(open('cache/hashes.dict', 'r'))
            self.stories = pickle.load(open('cache/stories.dict', 'r'))

        self.expire = expire

    def add(self, url):

        self.feeds.append(url)

    def parse(self, url, content):

        dom = minidom.parseString(content)

        for story in dom.getElementsByTagName('entry'):

            title = story.getElementsByTagName('title')[0].childNodes[0].nodeValue
            link = story.getElementsByTagName('link')[0].getAttribute('href')
            hash = sha256(link).hexdigest()

            if hash not in self.hashes:

                self.stories.insert(0, {
                    'origin': urlparse(url).netloc,
                    'site': urlparse(link).netloc,
                    'title': title,
                    'link': link,
                    'hash': hash
                })

                self.hashes.append(hash)

        for story in dom.getElementsByTagName('item'):

            title = story.getElementsByTagName('title')[0].childNodes[0].nodeValue
            link = story.getElementsByTagName('link')[0].childNodes[0].nodeValue
            hash = sha256(link).hexdigest()

            if hash not in self.hashes:

                self.stories.insert(0, {
                    'origin': urlparse(url).netloc,
                    'site': urlparse(link).netloc,
                    'title': title,
                    'link': link,
                    'hash': hash
                })

                self.hashes.append(hash)

    def run(self):

        for url in self.feeds:

            content = fetch_remote_file(url, 'cache/' + sha256(url).hexdigest(), self.expire)

            self.parse(url, content)

        pickle.dump(self.hashes, open('cache/hashes.dict', 'wb'))
        pickle.dump(self.stories, open('cache/stories.dict', 'wb'))
