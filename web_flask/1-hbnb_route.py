#!/usr/bin/python3
'''Starts Flask web application'''
from flask import Flask


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/')
def index():
    '''The home page.'''
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    '''Display the hbnb page.'''
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
