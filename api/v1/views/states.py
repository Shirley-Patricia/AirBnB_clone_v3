#!/usr/bin/python3
'''Creates a new view for State objects that handles
all default RESTFul API actions'''
import json
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allStates():
    '''Retrieves the list of all State objects'''
    all_states = list(storage.all('State').values())
    listStates = []
    for s in all_states:
        listStates.append(s.to_dict())
    return jsonify(listStates)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    '''Creates a State'''
    data_request = request.get_json()
    if type(data_request) is dict:
        for k in data_request.keys():
            if k == "name":
                obj = State(**data_request)
                storage.new(obj)
                storage.save()
                return jsonify(obj.to_dict()), 201
            else:
                return jsonify(message="Missing name"), 400
    else:
        return jsonify(message="Not a JSON"), 400


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def stateId(state_id):
    '''Retrieves a State object according to its id'''
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updateState(state_id):
    '''Updates a State object according to its state_id'''
    obj = storage.get('State', state_id)
    if obj:
        data_request = request.get_json()
        if type(data_request) is dict:
            noKeys = ['id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict())
        else:
            return jsonify(message="Not a JSON"), 404
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id):
    '''Deletes a State object according to its state_id'''
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)
