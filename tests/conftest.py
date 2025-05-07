import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from db import db
from models import User

@pytest.fixture
def client():
    # Configure app to use a temporary SQLite database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create all database tables before tests run
    with app.app_context():
        db.create_all()
        # Insert a mock user with ID 1
        test_user = User(id=1, username='testuser', password='fakepass')
        db.session.add(test_user)
        db.session.commit()

    # Yield test client to be used in tests
    with app.test_client() as client:
        yield client

    # Clean up: drop tables and remove test database file
    with app.app_context():
        db.drop_all()
    if os.path.exists('test.db'):
        os.remove('test.db')
