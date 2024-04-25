install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_detect.py

format:
	black *.py


lint:
	pylint --disable=R,C detect.py

all: install test format