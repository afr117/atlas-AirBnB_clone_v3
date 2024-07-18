#!/usr/bin/python3
"""
app.py - Flask application for the HBNB API.
"""

from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """Closes the storage on teardown."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', 5000)),
            threaded=True)
