import pytest
from audio import process_audio


@pytest.mark.parametrize(
    "url",
    ["https://file-examples.com/wp-content/storage/2017/11/file_example_MP3_700KB.mp3"],
)
def test_process_audio(url):
    base64_string = process_audio(url)
    assert base64_string is not None, "The process_audio function returned None"
    assert isinstance(base64_string, str), "The return value is not a string"
    assert len(base64_string) > 0, "The Base64 string received is empty"
    assert base64_string.startswith(
        "UklGRu"
    ), "The Base64 string does not start with 'UklGRu'"
