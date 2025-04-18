"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "graph_email"
COLLECTION_NAME = "emails"

# Microsoft Graph API configuration
class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    USER_EMAIL = os.getenv("USER_EMAIL")
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPES = ["https://graph.microsoft.com/.default"]
    REDIRECT_URI = "http://localhost:8000/getAToken"
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    MAIL_SEND_URL = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/sendMail"
    MAIL_READ_URL = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/inbox/messages"
    
