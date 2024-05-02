install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

test:
	python -m pytest -v -s --show-capture=all tests/test_upload.py
	python -m pytest -v -s --show-capture=all tests/test_metadata.py
	python -m pytest -v -s --show-capture=all tests/test_detect.py
	python -m pytest -v -s --show-capture=all tests/test_web.py
	python -m pytest -v -s --show-capture=all tests/test_audio.py

format:
	black tests
	black *.py

lint:
	pylint --disable=R,C *.py

all: install test format
