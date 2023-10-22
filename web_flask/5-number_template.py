#!/usr/bin/python3
'''Starts the Flask web application.
'''
from flask import Flask, render_template


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/')
def index():
    '''The home page.'''
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    '''Displays the hbnb page.'''
    return 'HBNB'


@app.route('/c/<text>')
def c_page(text):
    '''Displays c with any input text.'''
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>')
@app.route('/python', defaults={'text': 'is cool'})
def python_page(text):
    '''Displays python with any input text'''
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def number_page(n):
    '''Displays n is a number, if n is an integer.'''
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    '''HTML page for integer n.'''
    ctxt = {
        'n': n
    }
    return render_template('5-number.html', **ctxt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')