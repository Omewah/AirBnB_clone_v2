#!/usr/bin/python3
'''Starts the Flask web application.'''
from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    '''Fetches the cities by states from storage.'''
    state_lists = list(storage.all(State).values())
    state_lists.sort(key=lambda x: x.name)
    for state in state_lists:
        state.cities.sort(key=lambda x: x.name)
    ctxt = {
        'states': state_lists
    }
    return render_template('8-cities_by_states.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Remove the current SQLAlchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
