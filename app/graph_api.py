"""
Handles communication with Microsoft Graph API.
Includes authentication, sending emails, and retrieving messages.
"""

import os
import datetime
import requests
from msal import ConfidentialClientApplication, PublicClientApplication
from configs.config import Config

def get_access_token() -> str:
    """
    Acquire a bearer token from Microsoft Identity Platform using client credentials.
    """
    # app = ConfidentialClientApplication(
    #     client_id=Config.CLIENT_ID,
    #     authority=Config.AUTHORITY,
    #     client_credential=Config.CLIENT_SECRET
    # )

    app = PublicClientApplication(
        client_id=Config.CLIENT_ID,
        authority=Config.AUTHORITY,
        # client_credential=Config.CLIENT_SECRET
    )

    # token = app.acquire_token_for_client(scopes=Config.SCOPES)
    
    token = app.acquire_token_by_username_password(
            username=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            scopes=Config.SCOPES
        )
    
    if "access_token" not in token:
        raise Exception(f"Failed to acquire token: {token}")
    return token["access_token"]


def send_mail(subject: str, body: str, recipient: str):
    """
    Send an email via Microsoft Graph API.
    """
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [{"emailAddress": {"address": recipient}}]
        }
    }
    response = requests.post(Config.MAIL_SEND_URL, headers=headers, json=payload)
    response.raise_for_status()


def get_recent_emails():
    """
    Retrieve emails from the last 24 hours via Microsoft Graph API.
    """
    token = get_access_token()
    now = datetime.datetime.now()
    past = now - datetime.timedelta(days=1)
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "$filter": f"receivedDateTime ge {past.isoformat()}Z",
        "$orderby": "receivedDateTime desc",
        "$top": 50
    }
    response = requests.get(Config.MAIL_READ_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("value", [])
