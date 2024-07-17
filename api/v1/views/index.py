#!/usr/bin/python3
"""
index.py - API views for handling status and stats endpoints.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding classes
classes = {
    'amenities': Amenity,
    'cities': City,
    'places': Place,
    'reviews': Review,
    'states': State,
    'users': User
}

@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the number of each objects by type."""
    stats_dict = {}

    for key, cls in classes.items():
        stats_dict[key] = storage.count(cls)

    return jsonify(stats_dict)

if __name__ == '__main__':
    pass
