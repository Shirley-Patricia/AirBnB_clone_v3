#!/usr/bin/python3
'''Creates a new view for Place objects that handles
all default RESTFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def allPlaces(city_id):
    '''Retrieves the list of all City objects of a Place'''
    city = storage.get('City', city_id)
    if city:
        listPlaces = []
        for place in city.places:
            listPlaces.append(place.to_dict())
        return jsonify(listPlaces)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def objPlace(place_id):
    '''Retrieves a Place object'''
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    '''Delete a Place object'''
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlace(city_id):
    '''Createa a Place'''
    city = storage.get('City', city_id)
    if city:
        data_request = request.get_json()
        if type(data_request) is dict:
            if 'user_id' in data_request.keys:
                user = storage.get('User', data_request.user_id)
                if user:
                    for k in data_request.keys():
                        if k == "name":
                            obj = Place(**data_request)
                            storage.new(obj)
                            storage.save()
                            return jsonify(obj.to_dict()), 201
                        else:
                            abort(400, 'Missing name')
                else:
                    abort(404)
            else:
                abort(400, 'Missing user_id')
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    '''Updates a Place object'''
    place = storage.get('Place', place_id)
    if place:
        data_request = request.get_json()
        if type(data_request) is dict:
            noKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(place, key, value)
            storage.save()
            return jsonify(place.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
