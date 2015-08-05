import json

from flask import Flask, render_template, make_response
app = Flask(__name__)

from reader import Reader
from fetch_remote_file import *

config = json.loads(file_get_contents('config.json'))

@app.route('/')
def home():

    return render_template('app.html')

@app.route('/feed')
def feeds():

    reader = Reader()

    for feed in config['feeds']:
        reader.add(feed)

    reader.run()

    stories = reader.stories[0:100]

    return make_response(json.dumps({
            'count': len(stories),
            'stories': stories,
            'template': file_get_contents('templates/stories.hbs')
        }), 200, {
            'Content-type': 'application/json'
        })

if __name__ == '__main__':

    app.run()
