from detect import detect_faces_uri
from google.cloud import vision
import pytest


@pytest.fixture
def vision_client():
    try:
        client = vision.ImageAnnotatorClient()
        return client
    except Exception as e:
        pytest.fail(f"Failed to create Vision API client: {str(e)}")


def test_vision_client_connection(vision_client):
    assert vision_client is not None, "Failed to create Vision API client"


@pytest.fixture
def detect_function():
    return detect_faces_uri


def test_face_img_positive_response(detect_function):
    face_image = "https://img.freepik.com/free-photo/front-view-beautiful-woman-portrait_23-2149479366.jpg?w=1380&t=st=1714047423~exp=1714048023~hmac=fe68954343cf3880be040c9766746313a5295c0d29c94a85ba310b9b0b79bb85"
    assert detect_function(face_image) == "face detected"


def test_car_img_negative_response(detect_function):
    car_image = "https://imgd.aeplcdn.com/1056x594/n/cw/ec/132427/taisor-exterior-right-front-three-quarter-2.png?isig=0&q=80&wm=1"
    assert detect_function(car_image) == "no faces detected"


def test_invalid_uri_exception_response(detect_function):
    invalid_uri = "invalid_uri"
    try:
        detect_function(invalid_uri)
    except Exception as e:
        assert "Unsupported URI protocol specified" in str(e)
