#!/usr/bin/python3
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.review import Review
# index

@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):

    review = storage.get('Review', review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(review.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if not key in ["id", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(review, key, value)
        review.save()
        return make_response(jsonify(review.to_dict()), 200)

@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(place_id):

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify([review.to_dict()
                                      for review in place.reviews], 200))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if not 'user_id' in request.json:
            abort(400, 'Missing user_id')
        if not 'text' in request.json:
            abort(400, 'Missing text')
        new_Review = Review(**request.get_json())
        user_id = storage.get('User', new_Review.user_id)
        if not user_id:
            abort(404)
        new_Review.place_id = place.id
        new_State.save()
        return make_response(jsonify(new_State.to_dict()), 201)
