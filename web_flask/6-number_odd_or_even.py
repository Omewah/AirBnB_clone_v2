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
    '''The hbnb page.'''
    return 'HBNB'


@app.route('/c/<text>')
def c_page(text):
    '''Displays c with any text input value.'''
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>')
@app.route('/python')
def python_page(text='is cool'):
    '''Displays python with any text input value.'''
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def number_page(n):
    '''Displays n is a number, if n is an integer'''
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    '''The template for integer n.'''
    ctxt = {
        'n': n
    }
    return render_template('5-number.html', **ctxt)


@app.route('/number_odd_or_even/<int:n>')
def number_odd_or_even(n):
    '''The template for integer n, if odd or even.'''
    ctxt = {
        'n': n
    }
    return render_template('6-number_odd_or_even.html', **ctxt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
