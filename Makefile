install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt &&\
	if ! which ffmpeg &> /dev/null; then \
		echo "ffmpeg not found. Installing..."; \
		apt update && apt install -y ffmpeg; \
	else \
		echo "ffmpeg found."; \
	fi

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
