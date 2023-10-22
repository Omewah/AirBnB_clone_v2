#!/usr/bin/python3
'''Starts the Flask web application'''
from flask import Flask, render_template, Markup

from models import storage
from models.amenity import Amenity
from models.place import Place
from models.state import State


app = Flask(__name__)
'''The Flask application instance.'''
app.url_map.strict_slashes = False


@app.route('/hbnb')
def hbnb():
    '''The hbnb page.'''
    state_lists = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    places = list(storage.all(Place).values())
    state_lists.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)
    places.sort(key=lambda x: x.name)
    for state in state_lists:
        state.cities.sort(key=lambda x: x.name)
    for place in places:
        place.description = Markup(place.description)
    ctxt = {
        'states': state_lists,
        'amenities': amenities,
        'places': places
    }
    return render_template('100-hbnb.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''Remove the current SQLAlchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
