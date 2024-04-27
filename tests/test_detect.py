import os
import json
import pytest
from detect import FaceDetector
import requests
import base64

# Image URLs
FACE_IMAGE_URL = "https://img.freepik.com/free-photo/front-view-beautiful-woman-portrait_23-2149479366.jpg?w=1380&t=st=1714047423~exp=1714048023~hmac=fe68954343cf3880be040c9766746313a5295c0d29c94a85ba310b9b0b79bb85"
CAR_IMAGE_URL = "https://imgd.aeplcdn.com/1056x594/n/cw/ec/132427/taisor-exterior-right-front-three-quarter-2.png?isig=0&q=80&wm=1"


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
    result = face_detector.detect_faces_uri(FACE_IMAGE_URL)
    result_json = json.loads(result)
    assert result_json["result"] is True
    assert result_json["faces_count"] == 1


def test_face_img64_positive_response(face_detector):
    response = requests.get(FACE_IMAGE_URL)
    response.raise_for_status()
    content_base64 = base64.b64encode(response.content).decode("utf-8")
    result = face_detector.detect_faces_base64(content_base64)
    result_json = json.loads(result)
    assert result_json["result"] is True
    assert result_json["faces_count"] == 1


def test_car_img_negative_response(face_detector):
    result = face_detector.detect_faces_uri(CAR_IMAGE_URL)
    result_json = json.loads(result)
    assert result_json["result"] is False
    assert result_json["faces_count"] == 0


def test_car_img64_negative_response(face_detector):
    response = requests.get(CAR_IMAGE_URL)
    response.raise_for_status()
    content_base64 = base64.b64encode(response.content).decode("utf-8")
    result = face_detector.detect_faces_base64(content_base64)
    result_json = json.loads(result)
    assert result_json["result"] is False
    assert result_json["faces_count"] == 0


def test_invalid_uri_exception_response(face_detector):
    invalid_uri = "invalid_uri"
    result = face_detector.detect_faces_uri(invalid_uri)
    result_json = json.loads(result)
    assert result_json["error"] == "Unsupported URI protocol specified: invalid_uri."
