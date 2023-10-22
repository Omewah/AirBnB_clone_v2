#!/usr/bin/python3
'''Starts the Flask web application'''
from flask import Flask, render_template

from models import storage
from models.state import State


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
    '''Fetches the states lists from storage DB.'''
    states = None
    state = None
    state_lists = list(storage.all(State).values())
    case = 404
    if id is not None:
        res = list(filter(lambda x: x.id == id, state_lists))
        if len(res) > 0:
            state = res[0]
            state.cities.sort(key=lambda x: x.name)
            case = 2
    else:
        states = state_lists
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        states.sort(key=lambda x: x.name)
        case = 1
    ctxt = {
        'states': states,
        'state': state,
        'case': case
    }
    return render_template('9-states.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Remove the current SQLAlchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
