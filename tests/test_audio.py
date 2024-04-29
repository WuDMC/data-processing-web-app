import pytest
from audio import process_audio


@pytest.mark.parametrize(
    "url",
    ["https://download.samplelib.com/mp3/sample-9s.mp3"],
)
def test_process_audio(url):
    base64_string = process_audio(url)
    assert base64_string is not None, "The process_audio function returned None"
    assert isinstance(base64_string, str), "The return value is not a string"
    assert len(base64_string) > 0, "The Base64 string received is empty"
    assert base64_string.startswith(
        "UklGRgJd"
    ), "The Base64 string does not start with 'UklGRgJd'"
