#!/usr/bin/python3
'''create a route /status on the object app_views that returns a JSON
with status code'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_json():
    '''return status'''
    return jsonify({"status": "OK"})
