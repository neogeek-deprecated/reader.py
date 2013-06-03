import os
import urllib2
import datetime


def fetch_remote_file(url, cache, expire):

    expire = (datetime.datetime.now() - datetime.timedelta(minutes=expire)).strftime('%s')

    if not os.path.isfile(cache) or int(os.path.getmtime(cache)) < int(expire):

        content = urllib2.urlopen(url).read()
        cache = open(cache, 'w')
        cache.write(content)
        cache.close()

    else:

        content = file_get_contents(cache)

    return content


def file_get_contents(file):

    if os.path.isfile(file):

        file = open(file, 'r')
        content = file.read()
        file.close()

        return content
