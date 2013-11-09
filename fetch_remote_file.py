import os
import urllib2
import datetime


def fetch_remote_file(url, cache = '', expire = 0):

    if cache and expire:

        expire = (datetime.datetime.now() - datetime.timedelta(minutes=expire)).strftime('%s')

        if not os.path.isfile(cache) or int(os.path.getmtime(cache)) < int(expire):

            content = urllib2.urlopen(url).read()
            file_put_contents(cache, content)

        else:

            content = file_get_contents(cache)

    else:

        content = urllib2.urlopen(url).read()

    return content


def file_get_contents(file):

    if os.path.isfile(file):

        file = open(file, 'r')
        content = file.read()
        file.close()

        return content


def file_put_contents(file, content):

    file = open(file, 'w')
    file.write(content)
    file.close()

    return content