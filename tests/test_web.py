import pytest
import json
from web import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(app, client):
    result = client.get("/")
    assert result.status_code == 200
    assert {"Hello": "Mitek"} == json.loads(result.get_data(as_text=True))
