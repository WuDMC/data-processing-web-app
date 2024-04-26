import os
import json
import pytest
from upload import Uploader
import requests
import base64

# Image URLs
FACE_IMAGE_URL = "https://img.freepik.com/free-photo/front-view-beautiful-woman-portrait_23-2149479366.jpg?w=1380&t=st=1714047423~exp=1714048023~hmac=fe68954343cf3880be040c9766746313a5295c0d29c94a85ba310b9b0b79bb85"
CAR_IMAGE_URL = "https://imgd.aeplcdn.com/1056x594/n/cw/ec/132427/taisor-exterior-right-front-three-quarter-2.png?isig=0&q=80&wm=1"


@pytest.fixture(scope="module", autouse=True)
def uploader():
    json_credentials = os.getenv("GCP_CREDS")
    assert (
        json_credentials is not None
    ), "Google Cloud credentials are not provided in environment variables"

    credentials_info = json.loads(json_credentials)
    assert isinstance(
        credentials_info, dict
    ), "Invalid credentials format, should be a JSON object"

    uploader = Uploader(credentials_info)
    assert uploader is not None, "Failed to create FaceDetector instance"
    return uploader


def test_check_folder_name(uploader):
    folder_id = "1tSjqUMBH5SfGw9lVe9nFJT0wOC2w8Y4w"
    expected_name = "media_from_tg"

    # Получение информации о папке
    folder_info = uploader.get_file_info(folder_id)
    assert (
        folder_info is not None
    ), f"Failed to retrieve folder info for folder ID: {folder_id}"

    # Проверка соответствия имени папки ожидаемому имени
    assert (
        folder_info.get("name") == expected_name
    ), f"Folder name does not match expected name"


def test_upload_file(uploader):
    metadata = """
    {"channel_chat_created": false, "delete_chat_photo": false, "document": {"file_name": "8ebd7672-9e80-4a5a-a8ce-93ca521d7b7b.jpeg", "mime_type": "image/jpeg", "thumbnail": {"height": 160, "width": 320, "file_id": "AAMCAgADGQEAAx1mK2s8k_uhCnMuDtbFRFgLQYTePAAC5kwAAmgiYUlLmdHpIFLscQEAB20AAzQE", "file_size": 9462, "file_unique_id": "AQAD5kwAAmgiYUly"}, "file_id": "BQACAgIAAxkBAAMdZitrPJP7oQpzLg7WxURYC0GE3jwAAuZMAAJoImFJS5nR6SBS7HE0BA", "file_size": 61100, "file_unique_id": "AgAD5kwAAmgiYUk", "thumb": {"file_id": "AAMCAgADGQEAAx1mK2s8k_uhCnMuDtbFRFgLQYTePAAC5kwAAmgiYUlLmdHpIFLscQEAB20AAzQE", "file_unique_id": "AQAD5kwAAmgiYUly", "file_size": 9462, "width": 320, "height": 160}}, "group_chat_created": false, "supergroup_chat_created": false, "chat": {"first_name": "D", "id": 220428984, "type": "private", "username": "WuDMC"}, "date": 1714121532, "message_id": 29, "from": {"first_name": "D", "id": 220428984, "is_bot": false, "is_premium": true, "language_code": "en", "username": "WuDMC"}}
    """
    file_data = requests.get(CAR_IMAGE_URL).content
    base64file = base64.b64encode(file_data).decode("utf-8")

    # Загрузка файла
    file_id = uploader.upload_file(metadata, base64file)

    # Проверка успешности загрузки файла
    assert file_id is not None, "Failed to upload file"