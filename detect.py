from google.cloud import vision
from google.oauth2 import service_account
import json


class FaceDetector:
    def __init__(self, credentials_info):
        self.credentials_info = credentials_info
        self.client = self.authorize()

    def authorize(self):
        credentials = service_account.Credentials.from_service_account_info(
            self.credentials_info
        )
        return vision.ImageAnnotatorClient(credentials=credentials)

    def detect_img(self, image):
        response = self.client.face_detection(image=image)
        faces = (
            response.face_annotations if response.face_annotations is not None else []
        )

        likelihood_name = (
            "UNKNOWN",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        )

        result = {
            "result": bool(faces),
            "faces_count": len(faces),
            "info": [],
            "error": response.error.message if response.error.message else None,
        }

        for face in faces:
            face_info = {
                "anger": likelihood_name[face.anger_likelihood],
                "joy": likelihood_name[face.joy_likelihood],
                "surprise": likelihood_name[face.surprise_likelihood],
                "face_bounds": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in face.bounding_poly.vertices
                ],
            }
            result["info"].append(face_info)

        return json.dumps(result)

    def detect_faces_uri(self, uri):
        image = vision.Image()
        image.source.image_uri = uri
        result = self.detect_img(image)
        return result

    def detect_faces_base64(self, image_base64):
        image = vision.Image(content=image_base64)
        result = self.detect_img(image)
        return result
