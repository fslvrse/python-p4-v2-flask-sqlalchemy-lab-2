import pytest
from app import app, db

@pytest.fixture(scope='function', autouse=True)
def setup_database():
    """Setup and teardown a fresh database for every test function."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield  # Run the test
        db.session.remove()
        db.drop_all()
