from main import app
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_template(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register_template(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_qualifications_template(client):
    response = client.get('/qualifications')
    assert response.status_code == 401


def test_logout_template(client):
    response = client.get('/logout')
    assert response.status_code == 500
