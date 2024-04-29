import requests
import base64
import os
import subprocess


def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download the file.")
        return None


def convert_to_wav(file_content, file_name, output_file):
    temp_input_file = f"temp_input{file_name}"
    with open(temp_input_file, "wb") as temp_file:
        temp_file.write(file_content)
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        temp_input_file,
        "-ar",
        "16000",  # Частота дискретизации 16 кГц
        output_file,
    ]
    subprocess.run(ffmpeg_command, check=True)
    os.remove(temp_input_file)


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
        file_name = url.split("/")[-1]
        wav_file = f"{file_name}.wav"
        convert_to_wav(file_content, file_name, wav_file)
        base64_string = convert_to_base64(wav_file)

        delete_file(file_name)
        delete_file(wav_file)

        return base64_string
    else:
        print("Failed to download the file.")
        return None
