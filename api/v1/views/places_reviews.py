#!/usr/bin/python3
'''Create a new view for Review object that handles
all default RESTFul API actions'''
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def allReview(place_id):
    '''Retrieves the list of all Review objects of a Place
    according to its place_id'''
    place = storage.get('Place', place_id)
    listReview = []
    if place:
        for i in place.reviews:
            listReview.append(i.to_dict())
        return jsonify(listReview)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getReview(review_id):
    '''Retrieves a Review object according to its review_id'''
    objReview = storage.get('Review', review_id)
    if objReview:
        return jsonify(objReview.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    '''Deletes a Review object according to its review_id'''
    objReview = storage.get('Review', review_id)
    if objReview:
        storage.delete(objReview)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createReview(place_id):
    '''Creates a Review according to the place_id'''
    place = storage.get('Place', place_id)
    if place:
        data_request = request.get_json()
        if type(data_request) is dict:
            if 'user_id' not in data_request.keys():
                abort(400, 'Missing user_id')
            if 'text' not in data_request.keys():
                abort(400, 'Missing text')
            else:
                user = storage.get('User', data_request['user_id'])
                if user:
                    objReview = Review(**data_request)
                    storage.new(objReview)
                    storage.save()
                    return jsonify(objReview.to_dict()), 201
                else:
                    abort(404)
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    '''Updates a Review object according to its review_id'''
    objReview = storage.get('Review', review_id)
    if objReview:
        data_request = request.get_json()
        if type(data_request) is dict:
            noKeys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(objReview, key, value)
            storage.save()
            return jsonify(objReview.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
