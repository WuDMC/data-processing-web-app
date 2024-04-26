from google.cloud import vision
from google.oauth2 import service_account
import base64


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
        faces = response.face_annotations

        likelihood_name = (
            "UNKNOWN",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        )
        print("Faces:")

        for face in faces:
            print(f"anger: {likelihood_name[face.anger_likelihood]}")
            print(f"joy: {likelihood_name[face.joy_likelihood]}")
            print(f"surprise: {likelihood_name[face.surprise_likelihood]}")

            vertices = [
                f"({vertex.x},{vertex.y})" for vertex in face.bounding_poly.vertices
            ]

            print("face bounds: {}".format(",".join(vertices)))

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(
                    response.error.message
                )
            )

        if faces:
            return f"{len(faces)} face detected"
        else:
            return "no faces detected"

    def detect_faces_uri(self, uri):
        image = vision.Image()
        image.source.image_uri = uri
        result = self.detect_img(image)
        return result

    def detect_faces_base64(self, image_base64):
        image = vision.Image(content=image_base64)
        result = self.detect_img(image)
        return result
