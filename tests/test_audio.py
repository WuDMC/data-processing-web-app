import pytest
from audio import process_audio
import os
import json
from upload import Uploader

METADATA = """
    {"channel_chat_created": false, "delete_chat_photo": false, "group_chat_created": false, "supergroup_chat_created": false, "voice": {"duration": 1, "mime_type": "audio/mp3", "file_id": "AwACAgIAAxkBAAIBk2YugCUfgTWhEZbTfKWgHOVG5tmLAAI9UAAC4Ux5SQz8_s1HmfRWNAQ", "file_size": 507, "file_unique_id": "tefffst22233mp3"}, "chat": {"first_name": "D", "id": 220428984, "type": "private", "username": "WuDMC"}, "date": 1714323494, "message_id": 403, "from": {"first_name": "D", "id": 220428984, "is_bot": false, "is_premium": true, "language_code": "en", "username": "WuDMC"}}
    """


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
    assert uploader is not None, "Failed to create Uploader instance"
    return uploader


@pytest.fixture(scope="module")
def base64_string():
    return process_audio(
        "https://download.samplelib.com/mp3/sample-6s.mp3"
    )


def test_process_audio(base64_string):
    assert base64_string is not None, "The process_audio function returned None"
    assert isinstance(base64_string, str), "The return value is not a string"
    assert len(base64_string) > 0, "The Base64 string received is empty"
    assert base64_string.startswith(
        "UklGR"
    ), "The Base64 string does not start with 'UklGR'"


def test_upload_audio(uploader, base64_string):
    result = uploader.upload_file_with_metadata(METADATA, base64_string)
    assert result is not None and "tefffst22233mp3" in result, "Failed to upload file"
