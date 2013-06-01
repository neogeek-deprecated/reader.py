from hashlib import sha256
from urlparse import urlparse
from xml.dom import minidom

from fetch_remote_file import *


class Reader():

    feeds = []
    stories = []

    def add(self, url):

        self.feeds.append(url)

    def parse(self, url, content):

        dom = minidom.parseString(content)

        for story in dom.getElementsByTagName('entry'):

            title = story.getElementsByTagName('title')[0].childNodes[0].nodeValue
            link = story.getElementsByTagName('link')[0].getAttribute('href')

            self.stories.append({
                'origin': urlparse(url).netloc,
                'site': urlparse(link).netloc,
                'title': title,
                'link': link,
                'hash': sha256(link).hexdigest()
            })

        for story in dom.getElementsByTagName('item'):

            title = story.getElementsByTagName('title')[0].childNodes[0].nodeValue
            link = story.getElementsByTagName('link')[0].childNodes[0].nodeValue

            self.stories.append({
                'origin': urlparse(url).netloc,
                'site': urlparse(link).netloc,
                'title': title,
                'link': link,
                'hash': sha256(link).hexdigest()
            })

    def run(self):

        self.stories = []

        for url in self.feeds:

            content = fetch_remote_file(url, 'cache/' + sha256(url).hexdigest(), 15)

            self.parse(url, content)
