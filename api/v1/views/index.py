'''create a route /status on the object app_views that returns a JSON
with status code'''
from crypt import methods
from api.v1.views import app_views
from json import jsonify


@app_views.route('/status', methods='GET')
def status_json():
    ''''''
    return jsonify({"status": "OK"}), 200
