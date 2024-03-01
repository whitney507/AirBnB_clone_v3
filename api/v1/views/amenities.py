#!/usr/bin/python3
"""
Routes for managing Amenity objects and associated operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    Retrieves all Amenity objects.
    :return: JSON representation of all amenities.
    """
    amenity_list = []
    amenity_obj = storage.all("Amenity")
    for obj in amenity_obj.values():
        amenity_list.append(obj.to_json())

    return jsonify(amenity_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Create amenity route.
    :return: Newly created amenity object.
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    resp = jsonify(new_amenity.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Gets a specific Amenity object by ID.
    :param amenity_id: Amenity object ID.
    :return: Amenity object with the specified ID or error.
    """

    fetched_obj = storage.get("Amenity", str(amenity_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates specific Amenity object by ID.
    :param amenity_id: Amenity object ID.
    :return: Amenity object and 200 on success, or 400 or 404 on failure.
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("Amenity", str(amenity_id))
    if fetched_obj is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Deletes Amenity by ID.
    :param amenity_id: Amenity object ID.
    :return: Empty dictionary with 200 or 404 if not found.
    """

    fetched_obj = storage.get("Amenity", str(amenity_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})

