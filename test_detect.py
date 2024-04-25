import os
import json
import pytest
from detect import FaceDetector


@pytest.fixture(scope="module", autouse=True)
def face_detector():
    json_credentials = os.getenv("GCP_CREDS")
    assert (
        json_credentials is not None
    ), "Google Cloud credentials are not provided in environment variables"

    credentials_info = json.loads(json_credentials)
    assert isinstance(
        credentials_info, dict
    ), "Invalid credentials format, should be a JSON object"

    detector = FaceDetector(credentials_info)
    assert detector is not None, "Failed to create FaceDetector instance"
    return detector


def test_face_img_positive_response(face_detector):
    face_image = "https://img.freepik.com/free-photo/front-view-beautiful-woman-portrait_23-2149479366.jpg?w=1380&t=st=1714047423~exp=1714048023~hmac=fe68954343cf3880be040c9766746313a5295c0d29c94a85ba310b9b0b79bb85"
    assert face_detector.detect_faces_uri(face_image) == "1 face detected"


def test_car_img_negative_response(face_detector):
    car_image = "https://imgd.aeplcdn.com/1056x594/n/cw/ec/132427/taisor-exterior-right-front-three-quarter-2.png?isig=0&q=80&wm=1"
    assert face_detector.detect_faces_uri(car_image) == "no faces detected"


def test_invalid_uri_exception_response(face_detector):
    invalid_uri = "invalid_uri"
    with pytest.raises(Exception) as e:
        face_detector.detect_faces_uri(invalid_uri)
    assert "Unsupported URI protocol specified" in str(e.value)
