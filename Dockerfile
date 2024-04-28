FROM mwader/static-ffmpeg:6.0-1 AS ffmpeg 

FROM python:3.10.11-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_ROOT=/src

COPY --from=ffmpeg /ffmpeg /usr/local/bin/

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY . /app/

RUN make install

EXPOSE 8080

RUN find . | grep -E "(__pycache__|\.pytest_cache|\.pyc|\.pyo$)" | xargs rm -rf

CMD ["python", "web.py"]


