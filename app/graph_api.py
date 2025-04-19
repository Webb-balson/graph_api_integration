"""
Handles communication with Microsoft Graph API using Authorization Code Flow.
Includes authentication, sending emails, and retrieving messages.
"""
import sys
import datetime
import requests
from msal import PublicClientApplication, TokenCache
from configs.config import Config

# Initialize MSAL TokenCache
# This is a simple in-memory cache for demonstration purposes.
global_token_cache = TokenCache()

# Initialize MSAL PublicClientApplication
app = PublicClientApplication(
    client_id=Config.CLIENT_ID,
    authority=Config.AUTHORITY,
    token_cache=global_token_cache,  # Use the global token cache
)

def get_access_token() -> str:
    """
    Acquire a bearer token using Authorization Code Flow.
    """
    # Check if a token is already cached
    accounts = app.get_accounts()
    if accounts:
        # Attempt to silently acquire a token from the cache
        result = app.acquire_token_silent(scopes=Config.SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    # If no token is cached, initiate the device flow
    # This will prompt the user to authenticate using a device code
    # and authorize the app. The device code will be displayed to the user.
    # The user will need to enter this code on a separate device (e.g., a phone or another computer).
    flow = app.initiate_device_flow(scopes=Config.SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to create device flow. Ensure the application is registered correctly.")
    print(flow["message"])  # Display the device code message to the user
    sys.stdout.flush()  # Ensure the message is printed immediately

    result = app.acquire_token_by_device_flow(flow)  # Wait for the user to complete the device flow
   
    if "access_token" not in result:
        print(f"Token acquisition failed: {result}")
        raise Exception(f"Failed to acquire token: {result.get('error_description', result)}")
    # print(f"Access Token: {result['access_token']}")
    return result["access_token"]

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
    response = requests.post("https://graph.microsoft.com/v1.0/me/sendMail", headers=headers, json=payload)
    if response.status_code != 202:  # 202 indicates the email was accepted for delivery
        print(f"Failed to send email: {response.status_code}, {response.text}")
        response.raise_for_status()
    print("Email sent successfully.")

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
    response = requests.get("https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages", headers=headers, params=params)
    if response.status_code != 200:  # 200 indicates a successful response
        print(f"Failed to fetch emails: {response.status_code}, {response.text}")
        response.raise_for_status()
    emails = response.json().get("value", [])
    print(f"Retrieved {len(emails)} emails.")
    return emails