import datetime
import json


class MetadataParser:
    def parse_metadata(self, metadata):
        try:
            message = json.loads(metadata)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            if "document" in message:
                mime_type = message["document"]["mime_type"]
                file_name = f"doc_{mime_type}_{message['document']['file_unique_id']}"
            elif "voice" in message:
                file_name = f'voice_{message["voice"]["file_unique_id"]}.wav'
                mime_type = message["voice"]["mime_type"]
            elif "photo" in message:
                photo = message["photo"][0]
                file_name = f"photo_{photo['file_unique_id']}.jpeg"
                mime_type = "image/jpeg"
            elif "audio" in message:
                mime_type = message["audio"]["mime_type"]
                file_name = f'audio_{mime_type}_{message["audio"]["file_name"]}.wav'
            else:
                file_name = f"unknown_file_{timestamp}"
                mime_type = "text/plain"
            user_id = str(message.get("from", {}).get("id", "Unknown"))
            return file_name, mime_type, user_id

        except Exception as error:
            print(f"An error occurred while parsing the metadata: {error}")
            return None, None, None