```python
#!/usr/bin/python3
"""
Route for handling linking between places and amenities.
"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """
    Retrieves all amenities of a place.
    :param place_id: Place ID.
    :return: All amenities.
    """
    fetched_obj = storage.get("Place", str(place_id))
    all_amenities = []

    if fetched_obj is None:
        abort(404)

    for obj in fetched_obj.amenities:
        all_amenities.append(obj.to_json())

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an amenity from a place.
    :param place_id: Place ID.
    :param amenity_id: Amenity ID.
    :return: Empty dictionary or error.
    """
    if not storage.get("Place", str(place_id)) or not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetched_obj = storage.get("Place", place_id)
    found = False

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetched_obj.amenities.remove(obj)
            else:
                fetched_obj.amenity_ids.remove(obj.id)
            fetched_obj.save()
            found = True
            break

    if not found:
        abort(404)
    else:
        resp = jsonify({})
        resp.status_code = 201
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity with a place.
    :param place_id: Place ID.
    :param amenity_id: Amenity ID.
    :return: Returns Amenity object added or error.
    """
    fetched_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))

    if not fetched_obj or not amenity_obj:
        abort(404)

    for obj in fetched_obj.amenities:
        if str(obj.id) == amenity_id:
            return jsonify(obj.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_obj.amenities.append(amenity_obj)
    else:
        fetched_obj.amenities = amenity_obj

    fetched_obj.save()

    resp = jsonify(amenity_obj.to_json())
    resp.status_code = 201

    return resp
```
