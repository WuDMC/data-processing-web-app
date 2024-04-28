import pytest
from metadata import MetadataParser


@pytest.fixture
def parser():
    return MetadataParser()


def test_parse_metadata_document(parser):
    metadata = '{"channel_chat_created": false, "delete_chat_photo": false, "document": {"file_name": "1119-0-4.jpg", "mime_type": "image/jpeg", "thumbnail": {"height": 170, "width": 170, "file_id": "AAMCAgADGQEAAyZmK3EGqTpBvFISp9I4WuzLUR5gWgACNU0AAmgiYUnTl-AEWUgxNQEAB20AAzQE", "file_size": 6209, "file_unique_id": "AQADNU0AAmgiYUly"}, "file_id": "BQACAgIAAxkBAAMmZitxBqk6QbxSEqfSOFrsy1EeYFoAAjVNAAJoImFJ05fgBFlIMTU0BA", "file_size": 11631, "file_unique_id": "AgADNU0AAmgiYUk", "thumb": {"file_id": "AAMCAgADGQEAAyZmK3EGqTpBvFISp9I4WuzLUR5gWgACNU0AAmgiYUnTl-AEWUgxNQEAB20AAzQE", "file_unique_id": "AQADNU0AAmgiYUly", "file_size": 6209, "width": 170, "height": 170}}, "group_chat_created": false, "supergroup_chat_created": false, "chat": {"first_name": "D", "id": 220428984, "type": "private", "username": "WuDMC"}, "date": 1714123014, "message_id": 38, "from": {"first_name": "D", "id": 220428984, "is_bot": false, "is_premium": true, "language_code": "en", "username": "WuDMC"}}'
    file_name, mime_type, folder_name = parser.parse_metadata(metadata)
    assert "AgADNU0AAmgiYUk" in file_name
    assert mime_type == "image/jpeg"
    assert folder_name == "220428984"


def test_parse_metadata_voice(parser):
    metadata = '{"channel_chat_created": false, "delete_chat_photo": false, "group_chat_created": false, "supergroup_chat_created": false, "voice": {"duration": 2, "mime_type": "audio/ogg", "file_id": "AwACAgIAAxkBAAMTZitpN09G4YxVXg5swK80bQK1CtYAAtBMAAJoImFJOs0IfBYLJw00BA", "file_size": 7657, "file_unique_id": "AgAD0EwAAmgiYUk"}, "chat": {"first_name": "D", "id": 220428984, "type": "private", "username": "WuDMC"}, "date": 1714121016, "message_id": 19, "from": {"first_name": "D", "id": 220428984, "is_bot": false, "is_premium": true, "language_code": "en", "username": "WuDMC"}}'
    file_name, mime_type, folder_name = parser.parse_metadata(metadata)
    assert "AgAD0EwAAmgiYUk" in file_name
    assert mime_type == "audio/ogg"
    assert folder_name == "220428984"


def test_parse_metadata_photo(parser):
    metadata = '{"caption": "asda", "channel_chat_created": false, "delete_chat_photo": false, "group_chat_created": false, "photo": [{"height": 51, "width": 90, "file_id": "AgACAgIAAxkBAAOIZizZxaWHjFlvzUaPp17Usx_0GvoAAhjcMRtcW2hJykncucOBkuwBAAMCAANzAAM0BA", "file_size": 1292, "file_unique_id": "AQADGNwxG1xbaEl4"}, {"height": 180, "width": 320, "file_id": "AgACAgIAAxkBAAOIZizZxaWHjFlvzUaPp17Usx_0GvoAAhjcMRtcW2hJykncucOBkuwBAAMCAANtAAM0BA", "file_size": 15466, "file_unique_id": "AQADGNwxG1xbaEly"}, {"height": 450, "width": 800, "file_id": "AgACAgIAAxkBAAOIZizZxaWHjFlvzUaPp17Usx_0GvoAAhjcMRtcW2hJykncucOBkuwBAAMCAAN4AAM0BA", "file_size": 68997, "file_unique_id": "AQADGNwxG1xbaEl9"}, {"height": 720, "width": 1280, "file_id": "AgACAgIAAxkBAAOIZizZxaWHjFlvzUaPp17Usx_0GvoAAhjcMRtcW2hJykncucOBkuwBAAMCAAN5AAM0BA", "file_size": 132519, "file_unique_id": "AQADGNwxG1xbaEl-"}], "supergroup_chat_created": false, "chat": {"first_name": "D", "id": 220428984, "type": "private", "username": "WuDMC"}, "date": 1714215365, "message_id": 136, "from": {"first_name": "D", "id": 220428984, "is_bot": false, "is_premium": true, "language_code": "en", "username": "WuDMC"}}'
    file_name, mime_type, folder_name = parser.parse_metadata(metadata)
    assert "AQADGNwxG1xbaEl4" in file_name
    assert mime_type == "image/jpeg"
    assert folder_name == "220428984"
