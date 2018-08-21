from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
# index

@app_views.route('/cities/<city_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])

def city(city_id):
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in storage.all('City').values() if city_id == city.id])

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

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_of_State(state_id):
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        state = storage.get('State', state_id)
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if not 'name' in request.json:
            abort(400, 'Missing name')
        new = request.get_json()
        new_city = City()
        new_city.name = new
        new_city.state_id = state.id
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 200)
