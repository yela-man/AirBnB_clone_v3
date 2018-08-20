from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
# index

@app_views.route('/states', methods=['GET', 'POST'])
def all_states():
    if request.method == 'GET':
        return jsonify([state.to_dict() for state in storage.all('State').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if not 'name' in request.json:
            abort(400, 'Missing name')
        new = request.get_json()
        new_State = State()
        new_State.name = new
        new_State.save()
        return make_response(jsonify(new_State.to_dict()), 200)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state(state_id):
    if request.method == 'GET':
        state = storage.get('State', state_id)
        if not state:
            abort(404)
        return make_response(jsonify(state.to_dict()), 200)

    if request.method == 'DELETE':
        state = storage.get('State', state_id)
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
