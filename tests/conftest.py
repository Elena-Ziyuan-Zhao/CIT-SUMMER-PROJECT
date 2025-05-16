import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app
from db import db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create test DB and insert user
    with app.app_context():
        db.create_all()
        db.session.query(User).delete()
        db.session.commit()
        db.session.add(User(id=1, username='testuser', password='fakepass'))
        db.session.commit()

    with app.test_client() as client:
        # Re-open app context to access db
        with app.app_context():
            user = db.session.get(User, 1)
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)  
        yield client

    with app.app_context():
        db.drop_all()
    if os.path.exists('test.db'):
        os.remove('test.db')

@pytest.fixture(scope="session", autouse=True)
def create_fakenames_file():
    with open("fakenames.csv", "w") as f:
        f.write("Anonymous Panda\nAnonymous Fox\nAnonymous Owl\n")
    yield
    
