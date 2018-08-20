from flask import Flask, jsonify, make_response
from api.v1.views import app_views
# index
@app_views.route('/status', methods=['GET'])
def getStatus():
    return make_response(jsonify({'status':'OK'}), 200)
