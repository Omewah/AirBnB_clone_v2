#!/usr/bin/python3
'''Starts Flask web application.'''
from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    '''Fstch the state lists from storage.'''
    state_lists = list(storage.all(State).values())
    state_lists.sort(key=lambda x: x.name)
    ctxt = {
        'states': state_lists
    }
    return render_template('7-states_list.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Remove the current SQLAlchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
