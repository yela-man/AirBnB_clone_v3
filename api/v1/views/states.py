from flask import Flask, jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
# index

@app_views.route('/states', methods=['GET', 'POST'])
def allStates():
    if request.method == 'GET':
        return jsonify([state.to_dict() for state in storage.all('State').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if not 'name' in request.json:
            abort(400, 'Missing name')
        newState = State(request.json).save()
        return make_response(jsonify(newState.to_dict()), 200)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def aState(state_id):
    if request.method == 'GET':
        state = storage.get('State', state_id)
        if not state:
            abort(404)
        return make_response(jsonify(state), 200)

    if request.method == 'DELETE':
        state = storage.get('State', state_id)
        storage.delete(state)
        return make_response(jsonify({}), 200)
