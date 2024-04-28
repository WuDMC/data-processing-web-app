from flask import Flask, jsonify, request
from detect import FaceDetector
from upload import Uploader
from audio import process_audio

import os
import json

app = Flask(__name__)
face_detector = FaceDetector(json.loads(os.getenv("GCP_CREDS")))
uploader = Uploader(json.loads(os.getenv("GCP_CREDS")))


@app.route("/")
def index():
    return jsonify({"Hello": "Mitek"})


@app.route("/detect_faces", methods=["POST"])
def detect_faces():
    if request.method == "POST":
        data = request.get_json()
        image_url = data.get("image_url")
        image_64 = data.get("image_64")
        metadata = data.get("metadata")
        if not image_url and not image_64:
            return jsonify({"error": "Missing image_url or image_64 parameter"}), 400

        try:
            if image_64:
                face_detection_result = face_detector.detect_faces_base64(image_64)
                result_json = json.loads(face_detection_result)
                upload_result = (
                    uploader.upload_file_with_metadata(metadata, image_64)
                    if result_json["result"]
                    else "no faces = no upload, sorry bro"
                )
            else:
                face_detection_result = face_detector.detect_faces_uri(image_url)
                upload_result = "cant upload url, please use base64 file format"
            return (
                jsonify(
                    {
                        "face_detection_result": face_detection_result,
                        "upload_result": upload_result,
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/detect_faces", methods=["GET"])
def detect_faces_not():
    return jsonify({"error": "YOU SHALL NO PASS! Use POST request"})


@app.route("/save_audio", methods=["POST"])
def save_audio():
    if request.method == "POST":
        data = request.get_json()
        audio_url = data.get("audio_url")
        metadata = data.get("metadata")
        if not audio_url and not metadata:
            return jsonify({"error": "Missing audio_url or metadata parameter"}), 400

        try:
            upload_result = uploader.upload_file_with_metadata(
                metadata, process_audio(audio_url)
            )
            return (
                jsonify(
                    {
                        "upload_result": upload_result,
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/save_audio", methods=["GET"])
def save_audio_not():
    return jsonify({"error": "YOU SHALL NO PASS! Use POST request babe!!!!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
