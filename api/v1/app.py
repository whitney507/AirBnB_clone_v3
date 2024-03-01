#!/usr/bin/python3

'''

Create a Flask app and register the blueprint app_views to the Flask instance named app.

'''


from os import getenv

from flask import Flask, jsonify

from flask_cors import CORS

from models import storage

from api.v1.views import app_views


app = Flask(__name__)


# Enable CORS and specify allowed origins:

CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})


# Register the blueprint app_views:

app.register_blueprint(app_views)

app.url_map.strict_slashes = False



# Teardown the SQLAlchemy Session object after each request:

@app.teardown_appcontext

def teardown_engine(exception):

    '''

    Closes the current SQLAlchemy Session object.

    '''

    storage.close()



# Error handlers for expected application behavior:

@app.errorhandler(404)

def not_found(error):

    '''

    Return error message 'Not Found'.

    '''

    response = {'error': 'Not found'}

    return jsonify(response), 404



if __name__ == '__main__':

    HOST = getenv('HBNB_API_HOST', '0.0.0.0')

    PORT = int(getenv('HBNB_API_PORT', 5000))

    app.run(host=HOST, port=PORT, threaded=True)
