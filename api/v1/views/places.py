#!/usr/bin/python3
"""places for API routes v1"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User

# GET all places from a city
# ============================================================================


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_all_place(city_id):
    """get all places"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    list_places = [
        place.to_dict() for place in city.places if city.id == city_id]

    return jsonify(list_places)


# GET a place
# ============================================================================


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


# DELETE a place
# ============================================================================


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


# CREATE a place
# ============================================================================


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def post_place(city_id):
    """Creates a place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


# UPDATE a place
# ============================================================================


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_places(place_id):
    """Updates a place by its id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    ignore_key = ["id", "user_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore_key:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
