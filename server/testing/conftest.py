import pytest
from server.app import app, db

@pytest.fixture(scope='function', autouse=True)
def setup_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()
