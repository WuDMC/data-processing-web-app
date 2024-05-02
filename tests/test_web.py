import pytest
import json
from web import app as flask_app

TEST_BODY = {
    "image_64": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAQDAwQDAwQEAwQFBAQFBgoHBgYGBg0JCggKDw0QEA8NDw4RExgUERIXEg4PFRwVFxkZGxsbEBQdHx0aHxgaGxr/2wBDAQQFBQYFBgwHBwwaEQ8RGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhr/wAARCAEAAQADASIAAhEBAxEB/8QAFgABAQEAAAAAAAAAAAAAAAAAAAkI/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/EABQBAQAAAAAAAAAAAAAAAAAAAAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwDfwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAr/AAgCC/wAAIAgL/AAAAAAAAAAAAAAAAAAAAAAAACAIAL/AAIAgAAv8CAK/wAgCAv8AAAAAAAAAAAAAAAAAAAAACAIL/AgCAAAAAAC/wACAK/yAK/wAAAAAAAAAAAAAAAAAAAAIAr/AAAgCv8ACAIL/CAK/wAAIAgC/wAAIAr/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//Z",
    "metadata": '{"channel_chat_created": false, "delete_chat_photo": false, "group_chat_created": false, "photo": [{"height": 90, "width": 90, "file_id": "AgACAgIAAxkBAAPdZi0YgipV2nCIqUYceJKMKfgZ-k8AAsHdMRtcW2hJ284j9xd3lGUBAAMCAANzAAM0BA", "file_size": 695, "file_unique_id": "AQADwd0xG1xbaEl4"}, {"height": 256, "width": 256, "file_id": "AgACAgIAAxkBAAPdZi0YgipV2nCIqUYceJKMKfgZ-k8AAsHdMRtcW2hJ284j9xd3lGUBAAMCAANtAAM0BA", "file_size": 720, "file_unique_id": "AQADwd0xG1xbaEly"}], "supergroup_chat_created": false, "chat": {"first_name": "D", "id": 220428984, "type": "private", "username": "WuDMC"}, "date": 1714231426, "message_id": 221, "from": {"first_name": "D", "id": 220428984, "is_bot": false, "is_premium": true, "language_code": "en", "username": "WuDMC"}}',
}


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

def test_ffmpeg(app, client):
    result = client.get("/ffmpeg_installed")
    assert result.status_code == 200
    assert {"message": "FFmpeg is installed"} == json.loads(result.get_data(as_text=True))


def test_detect_faces(client):
    result = client.post("/detect_faces", json=TEST_BODY)
    assert result.status_code == 200
