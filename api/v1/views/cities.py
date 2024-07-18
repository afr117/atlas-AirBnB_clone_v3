#!/usr/bin/python3
"""State object view """
from flask import (Flask, jsonify, make_response, request, Response)
from flask import abort
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    """retrieve City object(s)"""
    print("===cities===")
    city_list = []

    all_cities = storage.all(City)

    single_state = storage.get(State, state_id)

    if single_state is None:
        abort(404)

    for k, v in all_cities.items():
        if getattr(v, 'state_id') == state_id:
            city_list.append(v.to_dict())

    return jsonify(city_list)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET'])
def city(city_id):
    """Retreive city object with city_id"""
    if city_id is not None:
        all_cities = storage.all(City)

        single_city = storage.get(City, city_id)

        if single_city is None:
            print("Aborting...")
            abort(404)

        return jsonify(single_city.to_dict())

    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['DELETE'])
def city_delete(city_id):
    """Deletes a city object """
    if city_id is not None:
        del_city = storage.get(City, city_id)

        if del_city is None:
            abort(404)

        del_city.delete()
        storage.save()
        return {}

    else:
        abort(404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['POST'])
def city_add(state_id):
    """Adds a city object"""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    single_state = storage.get(State, state_id)
    if single_state is None:
        abort(404)

    new = City(**data)
    setattr(new, 'state_id', state_id)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def city_update(city_id):
    """Update a city object"""
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    single_city = storage.get(City, city_id)
    if single_city is None:
        abort(404)

    # Update only allowed fields
    if 'name' in data:
        setattr(single_city, 'name', data['name'])

    single_city.save()
    storage.save()

    return jsonify(single_city.to_dict()), 200
