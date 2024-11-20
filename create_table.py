from models import db
from usta_tutoriales import app  # Assuming your app is in usta_tutoriales/__init__.py

with app.app_context():
    db.create_all()