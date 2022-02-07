#!/usr/bin/python3
'''Entry point for the app'''
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST') or '0.0.0.0'
port = getenv('HBNB_API_PORT') or 5000


@app.teardown_appcontext
def teardown_appcontext(self):
    '''This method marked with teardown_appcontext()
    are are called every time the app context tears down.'''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    '''returns a JSON-formatted 404 status code response'''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=host,
            port=port,
            threaded=True)
