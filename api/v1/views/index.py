#!usr/bin/python3
"""
api/v1/views/index.py
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    status = {
            "status": "OK"
            }
    return jsonify(status)

@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieve the number of each object by type."""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    })
