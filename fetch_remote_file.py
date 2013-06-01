import os
import urllib2
import datetime


def fetch_remote_file(url, cache, expire):

    expire = (datetime.datetime.now() - datetime.timedelta(minutes=expire)).strftime('%s')

    if not os.path.isfile(cache) or int(os.path.getmtime(cache)) < int(expire):

        output = urllib2.urlopen(url).read()
        cache = open(cache, 'w')
        cache.write(output)
        cache.close()

    else:

        cache = open(cache, 'r')
        output = cache.read()
        cache.close()

    return output
