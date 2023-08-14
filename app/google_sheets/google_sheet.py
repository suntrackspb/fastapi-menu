import os.path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import GOOGLE_REDIRECT_PORT

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")
SAMPLE_RANGE_NAME = os.getenv("GOOGLE_TABLE_RANGE")


def auth():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=int(GOOGLE_REDIRECT_PORT))
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_data(creds: Any):
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get("values", [])
        if not values:
            print("No data found.")
            return False
        return values

    except HttpError as err:
        print(err)
