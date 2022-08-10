import os
import requests
import httplib2 
from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
from google.oauth2 import service_account
import google.auth.transport.requests
import config as cfg


class GoogleDriver():

    CREDENTIALS_FILE = os.path.join(cfg.BASE_DIR, "creds/creds_api.json")
    SHEET_ID = cfg.SHEET_ID
    revision_date = None

    @classmethod
    def get_data(cls):
        response = cls.get_service_sheet().spreadsheets().values().get(spreadsheetId=cls.SHEET_ID, majorDimension='ROWS',
        range='Data').execute()
        if response.get('values'):
            return [tuple(x) for x in response['values'][1:]]
        else:
            return []

    @classmethod
    def get_service_sheet(cls):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds_service = ServiceAccountCredentials.from_json_keyfile_name(cls.CREDENTIALS_FILE, scopes).authorize(httplib2.Http())
        return googleapiclient.discovery.build('sheets', 'v4', http=creds_service)

    @classmethod
    def get_service_drive_token(cls):
        credentials = service_account.Credentials.from_service_account_file(cls.CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials.token

    @classmethod
    def get_revisions(cls):
        revisions_uri = f'https://www.googleapis.com/drive/v3/files/{cls.SHEET_ID}/revisions'
        headers = {'Authorization': f'Bearer {cls.get_service_drive_token()}'}
        response = requests.get(revisions_uri, headers=headers).json()
        return response['revisions'][-1]['modifiedTime']

    @classmethod
    def check_new_revisions(cls):
        revision_date = cls.get_revisions()
        if cls.revision_date!=revision_date:
            cls.revision_date = revision_date
            return True
        else:
            return False


