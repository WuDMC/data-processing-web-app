FROM python:3.10

RUN apt-get update && apt-get install -y --allow-unauthenticated ffmpeg

WORKDIR /app

COPY . /app/

RUN make install

EXPOSE 8080

CMD ["python", "web.py"]


