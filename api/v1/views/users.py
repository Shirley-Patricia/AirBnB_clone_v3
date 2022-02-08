#!/usr/bin/python3
'''Creates a new view for User object that handles
all default RESTFul API actions.'''
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def listUser():
    '''Retrieves the list of all User objects'''
    allUsers = list(storage.all('User').values())
    listUsers = []
    for user in allUsers:
        listUsers.append(user.to_dict())
    return jsonify(listUsers)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def objUser(user_id):
    '''retrieves a User object according to its user_id'''
    obj = storage.get('User', user_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deleteUser(user_id):
    '''Deletes a User object according to its user_id'''
    obj = storage.get('User', user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    '''Creates a User'''
    data_request = request.get_json()
    if type(data_request) is dict:
        if 'email' not in data_request.keys():
            abort(400, 'Missing email')
        if 'password' not in data_request.keys():
            abort(400, 'Missing password')
        obj = User(**data_request)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201
    else:
        abort(400, 'Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    '''Updates a User object according to its user_id'''
    obj = storage.get('User', user_id)
    if obj:
        data_request = request.get_json()
        if type(data_request) is dict:
            noKeys = ['id', 'email', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
