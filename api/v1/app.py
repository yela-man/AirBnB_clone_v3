from flask import Flask, render_template, abort
from models import storage
from os import getenv
from api.v1.views import app_views
# app
app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close(exception):
    storage.close()

if __name__ == "__main__":
    apiHost = getenv("HBNB_API_HOST") or "0.0.0.0"
    apiPort = getenv("HBNB_API_PORT") or 5000
    app.run(host=apiHost, port=apiPort, threaded=True)
