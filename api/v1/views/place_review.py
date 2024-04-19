#!/usr/bin/python3
"""place reviews for API routes v1"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


# GET all reviews from a place
# ============================================================================


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_all_reviews_from_place(place_id):
    """get all reviews from place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = storage.all(Review).values()

    list_reviews = [
        review.to_dict() for review in reviews if review.place_id == place_id
    ]

    return jsonify(list_reviews)


# GET 1 review
# ============================================================================


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """get review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


# DELETE a review
# ============================================================================


@app_views.route("reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """delete review by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


# CREATE a review
# ============================================================================


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """create new review"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    if "text" not in data:
        abort(400, "Missing text")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


# UPDATE a user
# ============================================================================


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """updtae user by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    ignore_key = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore_key:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
