#!/usr/bin/python3

"""Review object view"""
from flask import Flask, jsonify, make_response, request, abort
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """Retrieve a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return {}, 200

@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Create a new Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    data = request.get_json()
    if "user_id" not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    
    if "text" not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)
    
    data["place_id"] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)

@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Update a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    
    review.save()
    storage.save()
    return jsonify(review.to_dict())
