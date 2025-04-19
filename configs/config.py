"""Configuration settings for the application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "graph_email"
COLLECTION_NAME = "emails"

# Microsoft Graph API configuration
class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPES = ["Mail.Read", "Mail.Send"]  # Required permissions
