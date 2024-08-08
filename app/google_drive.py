import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
import json
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = 'client_secrets.json'

def get_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8081)
    service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
    return service

def get_folder_id():
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config['drive_folder_id']

def upload_to_drive(filepath, filename, folder_name):
    service = get_service()
    folder_id = get_folder_id()

    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath, mimetype='video/mp4')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID:', file.get('id'))
    return file.get('id')
