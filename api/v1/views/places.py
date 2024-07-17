#!/usr/bin/python3
"""State object view """
from flask import Flask, jsonify, request, Response
from flask import abort
from models.state import State
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def places(city_id):
    """retrieve City object(s)"""
    city_list = []

    if city_id is not None:

        single_city = storage.get(City, city_id)

        if single_city is None:
            abort(404)

        all_places = storage.all(Place)

        for k, v in all_places.items():
            if getattr(v, 'city_id') == city_id:
                city_list.append(v.to_dict())

        return jsonify(city_list)

    else:
        abort(404)

@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def city_r(place_id):
    """Retreive city object with city_id"""
    if place_id is not None:

        single_place = storage.get(Place, place_id)

        if single_place is None:
            abort(404)

        return jsonify(single_place.to_dict())

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """Deletes a city object """
    if place_id is not None:
        del_place = storage.get("Place", place_id)

        if del_place is None:
            abort(404)

        del_place.delete()
        storage.save()
        return {}

    else:
        abort(404)



