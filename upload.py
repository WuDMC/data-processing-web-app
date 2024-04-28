from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime
import base64
from googleapiclient.http import MediaIoBaseUpload
import io
from metadata import MetadataParser

PARENT_FOLDER_ID = "1VG4He-WCXn0K3tEF_13hyIgD5qFMTGHp"


class Uploader:
    def __init__(self, credentials_info):
        self.credentials_info = credentials_info
        self.metadata_parser = MetadataParser()
        self.service = self.authorize()

    def authorize(self):
        credentials = service_account.Credentials.from_service_account_info(
            self.credentials_info
        )
        return build("drive", "v3", credentials=credentials)

    def get_existing_folder_id(self, folder_name, parent_folder_id=PARENT_FOLDER_ID):
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"

            results = self.service.files().list(q=query, fields="files(id)").execute()
            existing_folders = results.get("files", [])
            if existing_folders:
                return existing_folders[0]["id"]
            else:
                return None
        except Exception as error:
            print(f"An error occurred while checking for existing folder: {error}")
            return None

    def get_file_info(self, file_id):
        try:
            file_info = (
                self.service.files().get(fileId=file_id, fields="id, name").execute()
            )
            return file_info
        except Exception as e:
            print(f"An error occurred while getting file info: {e}")
            return None

    def upload_file(
        self, file_name, mime_type, base64file, parent_folder_id=PARENT_FOLDER_ID
    ):
        try:
            # file_name, mime_type = self.metadata_parser.parse_metadata(metadata)
            file_data_decoded = base64.b64decode(base64file)
            media = MediaIoBaseUpload(io.BytesIO(file_data_decoded), mimetype=mime_type)
            file_metadata = {"name": file_name, "parents": [parent_folder_id]}
            file = (
                self.service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )

            print(
                f'File "{file_name}" has been uploaded to Google Drive with ID: {file.get("id")}'
            )
            return file.get("id")

        except Exception as error:
            print(f"An error occurred while uploading the file: {error}")
            return None

    def find_files_by_name(self, file_name, parent_folder_id=PARENT_FOLDER_ID):
        try:
            query = f"name='{file_name}'"
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"

            results = self.service.files().list(q=query, fields="files(id)").execute()
            existing_files = results.get("files", [])
            return [file["id"] for file in existing_files]

        except Exception as error:
            print(f"An error occurred while finding files: {error}")
            return []

    def delete_file(self, file_id):
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"File with ID '{file_id}' has been deleted")
        except Exception as error:
            print(f"An error occurred while deleting the file: {error}")

    def check_folder_permissions(self, folder_id):
        try:
            permissions = self.service.permissions().list(fileId=folder_id).execute()
            for permission in permissions.get("permissions", []):
                if permission["type"] == "anyone" and permission["role"] == "reader":
                    return True
            return False
        except Exception as error:
            print(f"An error occurred while checking permissions: {error}")
            return False

    def extend_permissions(self, folder_id):
        try:
            permission = {"type": "anyone", "role": "reader"}
            self.service.permissions().create(
                fileId=folder_id, body=permission
            ).execute()
            print(f"Permissions extended for folder with ID '{folder_id}'")
        except Exception as error:
            print(f"An error occurred while extending permissions: {error}")

    def create_folder(self, folder_name, parent_folder_id=PARENT_FOLDER_ID):
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_folder_id],
        }

        try:
            existing_folder_id = self.get_existing_folder_id(
                folder_name, parent_folder_id
            )
            if existing_folder_id:
                print(
                    f'Folder already existing, url: "{self.get_folder_url(existing_folder_id)}".'
                )
                return existing_folder_id

            file = self.service.files().create(body=metadata, fields="id").execute()
            print(f'Folder created, url: "{self.get_folder_url(file.get("id"))}".')
            return file.get("id")

        except Exception as error:
            print(f"An error occurred: {error}")
            return None

    def get_folder_url(self, folder_id):
        return f"https://drive.google.com/drive/folders/{folder_id}"

    def upload_file_with_metadata(self, metadata, base64_file):
        try:
            file_name, mime_type, folder_name = self.metadata_parser.parse_metadata(
                metadata
            )
            folder_id = self.get_existing_folder_id(folder_name)
            if not folder_id:
                folder_id = self.create_folder(folder_name)
            existing_files = self.find_files_by_name(file_name, folder_id)
            if existing_files:
                print(f"File with name '{file_name}' already exists in the folder.")
                return f"File with name '{file_name}' already exists in the folder, id: {existing_files}"
            file_id = self.upload_file(file_name, mime_type, base64_file, folder_id)
            if file_id:
                print(
                    f'File "{file_name}" uploaded to folder "{folder_name}" with ID: {file_id}'
                )
                print(f'URL: "{self.get_folder_url(PARENT_FOLDER_ID)}"')
                return f"{file_id} uploaded successfully to {self.get_folder_url(folder_id)} with filename {file_name}"

        except Exception as error:
            print(f"An error occurred while uploading file with metadata: {error}")
