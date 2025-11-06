import pytest
from app import create_app
from app.db import db

@pytest.fixture()
def app():
    app = create_app(testing=True)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def cleanup_db(app):
    # Ensure a fresh DB per test
    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
