```python
#!/usr/bin/python3
"""
Endpoints for providing index information.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Endpoint to check the status.
    :return: JSON response indicating status.
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Endpoint to get statistics of all objects.
    :return: JSON containing counts of all objects.
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
```
