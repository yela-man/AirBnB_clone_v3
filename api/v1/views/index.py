#!/usr/bin/python3
'''
index page for flask
displays status and stats
'''
from flask import Flask, jsonify, make_response
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def getStatus():
    return make_response(jsonify({'status': 'OK'}), 200)


@app_views.route('/stats', methods=['GET'])
def getCount():
    count_dict = {"amenities": 'Amenity',
                  "cities": 'City',
                  "places": 'Place',
                  "reviews": 'Review',
                  "states": 'State',
                  "users": 'User'}

    from models import storage

    for k in count_dict.keys():
        count_dict[k] = storage.count(count_dict.get(k))
    return make_response(jsonify(count_dict), 200)
