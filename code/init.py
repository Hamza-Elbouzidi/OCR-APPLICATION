from db.db import db
from app import app

# Ensure the app context is available
with app.app_context():
    # Create the tables in the database
    db.create_all()
