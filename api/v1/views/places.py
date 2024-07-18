#!/usr/bin/python3
"""Place object view"""
from flask import Flask, jsonify, make_response, request, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places_by_city(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieve a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Create a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    if "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data["city_id"] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Update a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    storage.save()
    return jsonify(place.to_dict())
