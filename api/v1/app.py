#!/usr/bin/python3
"""start flask web api"""

from flask import jsonify
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(self):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formated status code for errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
