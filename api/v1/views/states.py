#!/usr/bin/python3
"""State object view """
from flask import Flask, jsonify, make_response, request, Response
from flask import abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False,  methods=['GET'])
def states():
    """retrieve State object(s)"""
    state_list = []
    all_states = storage.all(State)
    for k, v in all_states.items():
        state_list.append(v.to_dict())
    return (state_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def state_id(state_id):
    """Retrieves a State object based on id"""
    if state_id is not None:
        state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def state_add():
    """Adds a state object"""
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new = State(**data)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """Update an existing state object"""
    data = request.get_json()
    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400
    single_state = storage.get(State, state_id)
    if single_state is None:
        abort(404)

    setattr(single_state, 'name', data['name'])
    single_state.save()
    storage.save()

    return jsonify(single_state.to_dict())
