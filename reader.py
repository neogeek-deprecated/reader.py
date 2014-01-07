import pickle

from hashlib import sha256
from urlparse import urlparse
from xml.dom import minidom

from fetch_remote_file import *


class Reader():

    cache = 'cache/'

    expire = 5

    feeds = []
    hashes = []
    stories = []

    def __init__(self):

        if not os.path.exists(self.cache):
            os.makedirs(self.cache)

        if os.path.isfile(self.cache + 'hashes.dict') and os.path.isfile(self.cache + 'stories.dict'):

            self.hashes = pickle.load(open(self.cache + 'hashes.dict', 'r'))
            self.stories = pickle.load(open(self.cache + 'stories.dict', 'r'))

    def add(self, url):

        self.feeds.append(url)

    def run(self):

        for url in self.feeds:

            self.parse(url, fetch_remote_file(url, self.cache + sha256(url).hexdigest(), self.expire))

        pickle.dump(self.hashes[0:1000], open(self.cache + 'hashes.dict', 'wb'))
        pickle.dump(self.stories[0:1000], open(self.cache + 'stories.dict', 'wb'))

    def parse(self, url, content):

        try:

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

        except Exception, e:
            print e