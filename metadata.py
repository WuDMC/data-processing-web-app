import datetime
import json


class MetadataParser:
    def parse_metadata(self, metadata):
        try:
            # Преобразование строки metadata в объект Message
            message = json.loads(metadata)

            # Получение данных файла из объекта Message
            if "document" in message:
                file_name = f"doc_{message["document"]["file_unique_id"]}'
                mime_type = message["document"]["mime_type"]
            elif "voice" in message:
                file_name = f'voice_{message["voice"]["file_unique_id"]}.wav'
                mime_type = message["voice"]["mime_type"]
            elif "photo" in message:
                photo = message["photo"][0]
                file_name = f"photo_{photo["file_unique_id"]}.jpeg"
                mime_type = "image/jpeg"
            else:
                raise "incorrect metadata"

            user_id = str(message["from"]["id"])

            print(f"file_name: {file_name} mime_type:{mime_type}")
            return file_name, mime_type, user_id

        except Exception as error:
            print(f"An error occurred while parsing the metadata: {error}")
            return None, None
