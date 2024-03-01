#!/usr/bin/python3
"""
Main application setup.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Function to close storage connection upon application context teardown.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handler for 404 errors.
    :return: JSON response indicating the error.
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))

