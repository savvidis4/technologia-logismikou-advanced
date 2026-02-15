import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    # 1. Define the SAFE test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # FORCE RAM DB
        "JWT_SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False
    }

    # 2. Pass it into create_app so the Real DB is NEVER loaded
    app = create_app(test_config=test_config)

    # 3. Double-Check Safety (Nuclear Option)
    # If the app somehow still thinks it's using MySQL, ABORT IMMEDIATELY.
    if "mysql" in app.config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("🚨 ABORTING! Tests tried to run against production Database!")

    # 4. Create tables in the fake RAM database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_user(client):
    """
    This fixture registers a user in the temporary database.
    Any test that includes 'test_user' as an argument will have this 
    user pre-created in the database before the test starts.
    """
    user_data = {
        "email": "existing_user@uniwa.gr",
        "password": "StrongPassword123!",
        "ver_password": "StrongPassword123!"
    }
    
    # Register the user
    client.post('/register', json=user_data)
    
    # Return the data so the test knows what email/pass to use
    return user_data


@pytest.fixture
def client(app):
    # This creates a fake browser/client we can use to make requests to our API
    return app.test_client()