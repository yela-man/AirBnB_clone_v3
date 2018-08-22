#!/usr/bin/python3
'''
places_reviews handler
'''
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.review import Review


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
            if key not in ["id", "user_id", "place_id",
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
        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')
        if 'text' not in request.json:
            abort(400, 'Missing text')
        new_Review = Review(**request.get_json())
        user_id = storage.get('User', new_Review.user_id)
        if not user_id:
            abort(404)
        new_Review.place_id = place.id
        new_Review.save()
        return make_response(jsonify(new_Review.to_dict()), 201)
