import json
from flask import Flask, make_response, render_template, send_from_directory
app = Flask(__name__, template_folder='templates/')

from reader import Reader
from fetch_remote_file import *


@app.route('/css/<path:filename>')
def static_css(filename):

    return send_from_directory('static/css', filename)


@app.route('/img/<path:filename>')
def static_img(filename):

    return send_from_directory('static/img', filename)


@app.route('/js/<path:filename>')
def static_js(filename):

    return send_from_directory('static/js', filename)


@app.route('/')
def home():

    return render_template('app.html')


@app.route('/feeds')
def feeds():

    reader = Reader(5)

    reader.add('https://news.ycombinator.com/rss')
    reader.add('http://theverge.com/rss/index.xml')
    reader.add('http://polygon.com/rss/index.xml')

    reader.run()

    html_template = file_get_contents('templates/stories.html')

    return make_response((json.dumps({'stories': reader.stories[0:100], 'template': html_template}), 200, {
        'Access-Control-Allow-Origin': '*',
        'Content-type': 'application/json'
    }))

if __name__ == '__main__':

    app.run()
