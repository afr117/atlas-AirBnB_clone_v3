# api/v1/app.py

from flask import Flask
from models import storage
from api.v1.views import app_views
import os  # Import os module

app = Flask(__name__)

# Register the blueprint for API routes
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Teardown function that closes the database session."""
    storage.close()

if __name__ == "__main__":
    # Run the Flask server
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', 5000)),
            threaded=True)
