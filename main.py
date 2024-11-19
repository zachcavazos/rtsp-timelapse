import os
import requests
import glob
import google.auth
import json
import sys

import config

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from create_timelapse import create_timelapse
from delete_input import delete_input
from get_credentials import get_credentials
from notify_upload import notify_upload, notify_failure


def upload_media(media_path, creds):
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'

    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': os.path.basename(media_path),
        'X-Goog-Upload-Protocol': 'raw',
    }

    # Read the media file
    with open(media_path, 'rb') as f:
        data = f.read()

    # Upload the file to Google Photos
    response = requests.post(upload_url, headers=headers, data=data)

    if response.status_code == 200:
        upload_token = response.text
        print(f'Upload Token: {upload_token}')
        return upload_token
    else:
        print(f'Error uploading photo: {response.text}')
        return None


# Create media item in Google Photos (add photo to an album)
def create_media_item(upload_token, album_id, creds):
    create_url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'

    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-type': 'application/json',
    }

    # Request body to add media item to an album
    new_media_items = [
        {
            "description": "Uploaded via Python script",
            "simpleMediaItem": {
                "uploadToken": upload_token
            }
        }
    ]

    # Add album ID if provided
    if album_id:
        data = {
            "newMediaItems": new_media_items,
            "albumId": album_id  # This needs to be in the root object
        }
    else:
        data = {
            "newMediaItems": new_media_items
        }

    # Make the API request to create the media item
    response = requests.post(create_url, headers=headers, json=data)

    if response.status_code == 200:
        print('Photo added to album successfully!')
    else:
        print(f'Error adding photo to album: {response.text}')


def get_album_id(album_title, creds):
    root_path = '/home/cavazos/src/rtsp-timelapse/'
    with open(root_path + 'album.json', 'r') as f:
        album_details = json.load(f)
        if album_title in album_details:
            print('Album created in a previous run!')
            return album_details[album_title]
    
    create_album = 'https://photoslibrary.googleapis.com/v1/albums'
    headers = {'Authorization': f'Bearer {creds.token}', 'Content-type': 'application/json'}
    response = requests.post(create_album, headers=headers, json={'album': {'title': album_title}})
    if response.status_code == 200:
        print('Album created successfully!')
    else:
        print(f'Error creating album: {response.text}')
    
    with open(root_path + 'album.json', 'w') as f:
        album_details[album_title] = response.json().get('id')
        json.dump(album_details, f)
    return response.json().get('id')


def main(camera_name='nursery'):
    timelapse_path = create_timelapse(camera_name)
    creds = get_credentials()
    if not timelapse_path or creds == -1:
        notify_failure()
        return
    print(f'Timelapse Created at {timelapse_path}')
    album_id = get_album_id(config.TIMELAPSE_ALBUM, creds)
    upload_token = upload_media(timelapse_path, creds)
    if upload_token:
        create_media_item(upload_token, album_id, creds)
        notify_upload(camera_name)
    delete_input(camera_name)


if __name__ == '__main__':
    args = sys.argv
    camera_name = args[1] if len(args) > 1 else 'nursery'
    main(camera_name)


