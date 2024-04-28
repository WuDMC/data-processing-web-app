# how ro run

docker build . -t web-app
docker run -d -e GCP_CREDS='creds from json service account GCP' web-app


