from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime
import base64
from googleapiclient.http import MediaIoBaseUpload
import io

class Uploader:
    def __init__(self, credentials_info):
        self.credentials_info = credentials_info
        self.service = self.authorize()

    def authorize(self):
        credentials = service_account.Credentials.from_service_account_info(
            self.credentials_info
        )
        return build("drive", "v3", credentials=credentials)

    def create_folder(self, folder_name, parent_folder_id=None):
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_folder_id:
            metadata["parents"] = [parent_folder_id]
        else:
            metadata["parents"] = ["1tSjqUMBH5SfGw9lVe9nFJT0wOC2w8Y4w"]

        try:
            existing_folder_id = self.get_existing_folder_id(
                folder_name, parent_folder_id
            )
            if existing_folder_id:
                print(f"Папка '{folder_name}' уже существует в родительской папке.")
                return existing_folder_id

            file = self.service.files().create(body=metadata, fields="id").execute()
            print(f'Folder ID: "{file.get("id")}".')
            return file.get("id")

        except Exception as error:
            print(f"An error occurred: {error}")
            return None

    def get_existing_folder_id(self, folder_name, parent_folder_id=None):
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
                self.service.files()
                .get(fileId=file_id, fields="id, name")
                .execute()
            )
            return file_info
        except Exception as e:
            print(f"An error occurred while getting file info: {e}")
            return None

    def parse_metadata(self, metadata):
        try:
            # Преобразование строки metadata в объект Message
            message = json.loads(metadata)

            # Определение типа файла (документ, аудио или изображение)
            if "document" in message:
                file_type = "document"
            elif "voice" in message:
                file_type = "voice"
            else:
                file_type = "photo"

            # Получение данных файла из объекта Message
            if file_type == "document":
                file_name = message["document"]["file_name"]
                mime_type = message["document"]["mime_type"]
            elif file_type == "voice":
                file_name = message["voice"]["file_name"]
                mime_type = message["voice"]["mime_type"]
            else:  # Для фотографии
                file_name = message["photo"]["file_name"]
                mime_type = message["photo"]["mime_type"]

            return file_name, mime_type

        except Exception as error:
            print(f"An error occurred while parsing the metadata: {error}")
            return None, None

    def upload_file(self, metadata, base64file, parent_folder_id=None):
        try:
            file_name, mime_type = self.parse_metadata(metadata)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_file_name = f"{file_name}_{timestamp}"
            file_data_decoded = base64.b64decode(base64file)
            media = MediaIoBaseUpload(io.BytesIO(file_data_decoded), mimetype=mime_type)
            file_metadata = {"name": unique_file_name}
            if parent_folder_id:
                file_metadata["parents"] = [parent_folder_id]
            else:
                file_metadata["parents"] = ["1tSjqUMBH5SfGw9lVe9nFJT0wOC2w8Y4w"]
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

    def find_files_by_name_and_type(self, file_name, mime_type, parent_folder_id=None):
        try:
            query = f"name='{file_name}' and mimeType='{mime_type}'"
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"

            results = self.service.files().list(q=query, fields="files(id)").execute()
            existing_files = results.get('files', [])
            return [file['id'] for file in existing_files]

        except Exception as error:
            print(f"An error occurred while finding files: {error}")
            return []

    def delete_file(self, file_id):
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"File with ID '{file_id}' has been deleted")
        except Exception as error:
            print(f"An error occurred while deleting the file: {error}")
