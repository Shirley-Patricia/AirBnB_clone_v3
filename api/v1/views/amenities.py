#!/usr/bin/python3
'''Creates a new view for Amenity objects that handles
all default RESTFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allAmenities():
    '''Retrieves the list of all Amenities objects'''
    all_amenities = list(storage.all('Amenity').values())
    listAmenities = []
    for ameni in all_amenities:
        listAmenities.append(ameni.to_dict())
    return jsonify(listAmenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def objAmenity(amenity_id):
    '''Retrieves a Amenity object'''
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    '''Deletes a Amenity object according to its amenity_id'''
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    '''Creates a Amenity'''
    data_request = request.get_json()
    if type(data_request) is dict:
        for k in data_request.keys():
            if k == "name":
                obj = Amenity(**data_request)
                storage.new(obj)
                storage.save()
                return jsonify(obj.to_dict()), 201
            else:
                abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenitie(amenity_id):
    '''Updates a Amenitie object according to its amenity_id'''
    obj = storage.get('Amenity', amenity_id)
    if obj:
        data_request = request.get_json()
        if type(data_request) is dict:
            noKeys = ['id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
