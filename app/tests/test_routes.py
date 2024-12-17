# tests/test_routes.py
import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302  # redirect to login
