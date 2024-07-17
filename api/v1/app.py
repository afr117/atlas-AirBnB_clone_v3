#!/usr/bin/python3
"""
app.py - Flask application for the HBNB API.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views


import os  # Ensure os is imported


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext

def teardown(exception):
    """Closes the storage on teardown."""
    storage.close()

if __name__ == "__main__":

    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', 5000)),
            threaded=True)
