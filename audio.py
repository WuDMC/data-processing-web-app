import requests
import wave
import base64
import os


def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download the file.")
        return None


def convert_to_wav(file_content, output_file):
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(2)  # Задаем количество каналов
        wf.setsampwidth(2)  # Задаем размер сэмпла в байтах
        wf.setframerate(16000)  # Задаем частоту дискретизации
        wf.writeframes(file_content)


def convert_to_base64(input_file):
    with open(input_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string.decode("utf-8")


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} deleted.")
    else:
        print(f"File {file_path} does not exist.")


def process_audio(url):
    file_content = download_file(url)
    if file_content:
        # Extract filename from the URL
        file_name = url.split("/")[-1]
        # Save the downloaded file
        with open(file_name, "wb") as f:
            f.write(file_content)

        # Convert to WAV
        wav_file = "output.wav"
        convert_to_wav(file_content, wav_file)  # Pass file content instead of filename

        # Convert to Base64
        base64_string = convert_to_base64(wav_file)

        # Delete temporary files
        delete_file(file_name)
        delete_file(wav_file)

        return base64_string
    else:
        print("Failed to download the file.")
        return None
