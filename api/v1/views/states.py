#!/usr/bin/python3
"""
Routes for managing State objects and associated operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    Retrieves all State objects.
    :return: JSON representation of all states.
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create state route.
    :return: Newly created state object.
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Gets a specific State object by ID.
    :param state_id: State object ID.
    :return: State object with the specified ID or error.
    """

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates specific State object by ID.
    :param state_id: State object ID.
    :return: State object and 200 on success, or 400 or 404 on failure.
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Deletes State by ID.
    :param state_id: State object ID.
    :return: Empty dictionary with 200 or 404 if not found.
    """

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
