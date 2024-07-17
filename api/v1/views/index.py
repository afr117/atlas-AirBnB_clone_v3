#!/usr/bin/python3
"""
index.py - API views for handling status endpoint.
"""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.__init__ import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Returns the number of each type of object instance
    """
    return jsonify({
                    "amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)
                    })
