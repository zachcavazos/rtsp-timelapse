from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError

import os
import io
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary', "https://www.googleapis.com/auth/photoslibrary.sharing"]  # Only append to an album

# Replace with your album ID.  You'll need to find this in Google Photos.
ALBUM_ID = 'Aarya Timelapses'

# Path to the credentials JSON file downloaded from Google Cloud Console.
CREDENTIALS_FILE = 'client_secret.json'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    root_path = '/home/cavazos/src/rtsp-timelapse/'
    if os.path.exists(root_path + 'token.json'):
        creds = Credentials.from_authorized_user_file(root_path + 'token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open(root_path + 'token.json', 'w') as token:
                token.write(creds.to_json())
    except RefreshError as e:
        print(e)
        return -1
    return creds


if __name__ == '__main__':
    print(get_credentials())

