#!/usr/bin/python3
'''
places handler
'''
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def getplace(place_id):

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ["user_id", "city_id",
                           "id", "created_at", "updated_at"]:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if not storage.get('User', request.get_json()['user_id']):
            abort(404)
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_place = Place(**request.get_json())
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201
