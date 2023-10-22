#!/usr/bin/python3
'''Starts the Flask web application'''
from flask import Flask, render_template

from models import storage
from models.amenity import Amenity
from models.state import State


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def hbnb_filters():
    '''The hbnb filters page.'''
    state_lists = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    state_lists.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)
    for state in state_lists:
        state.cities.sort(key=lambda x: x.name)
    ctxt = {
        'states': state_lists,
        'amenities': amenities
    }
    return render_template('10-hbnb_filters.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Removes the current SQLAlchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
