#!/usr/bin/python3
'''
place amenities
'''
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from os import getenv
# index


@app_views.route('places/<place_id>/amenities', methods=['GET'])
def place_allamens(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    placeAmens = (place.amenities
                  if getenv("HBNB_TYPE_STORAGE") == "db"
                  else place.amenities())
    return jsonify([place.to_dict() for place in placeAmens])


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def place_amenity(place_id, amenity_id):

    amen = storage.get('Amenity', amenity_id)
    place = storage.get('Place', place_id)
    if not amen or not place:
        abort(404)

    placeAmens = (place.amenities
                  if getenv("HBNB_TYPE_STORAGE") == "db"
                  else place.amenities())

    if request.method == 'DELETE':
        if amen not in placeAmens:
            abort(404)
        if getenv("HBNB_TYPE_STORAGE") == "fs":
            del place.amenity_ids[amen.id]
        storage.delete(amen)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'POST':
        if amen not in placeAmens:
            if getenv("HBNB_TYPE_STORAGE") == "fs":
                place.amenity_ids.append(amen.id)
            else:
                place.amenities.append(amen)
            place.save()
        return make_response(jsonify(amen.to_dict()), 201)
