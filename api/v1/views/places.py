#!/usr/bin/python3
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
# index


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE'])

def getplace(place_id):

    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if not key in ["user_id", "city_id",
                           "id", "created_at", "updated_at"]:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST', 'PUT'])

def places(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if not key in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if not 'user_id' in request.json:
            abort(400, 'Missing user_id')
        if not storage.get('User', request.json['user_id']):
            abort(404)
        if not name in request.json:
            abort(400, 'Missing name')
        new_place = Place(**request.get_json())
        new_place.city_id = city_id
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)
