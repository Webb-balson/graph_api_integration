"""
Handles MongoDB operations for storing and retrieving emails.
"""

from pymongo import MongoClient
from configs import config
from utils.schemas import EmailSchema
import json

# Initialize MongoDB client
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]
users_collection = db["users_coll"]
contacts_collection = db["contacts_coll"]

def preprocess_email(email: dict) -> dict:
    """
    Pre-process raw email data from Microsoft Graph API to match the schema.
    """
    return {
        "id": email["id"],
        "subject": email.get("subject", ""),
        "body": email.get("body", {}).get("content", ""),  # Extract the content field
        "sender": {
            "name": email.get("from", {}).get("emailAddress", {}).get("name", ""),
            "email": email.get("from", {}).get("emailAddress", {}).get("address", "")
        },
        "toRecipients": [
            {
                "name": recipient.get("emailAddress", {}).get("name", ""),
                "email": recipient.get("emailAddress", {}).get("address", "")
            }
            for recipient in email.get("toRecipients", [])
        ],
        "ccRecipients": [
            {
                "name": recipient.get("emailAddress", {}).get("name", ""),
                "email": recipient.get("emailAddress", {}).get("address", "")
            }
            for recipient in email.get("ccRecipients", [])
        ],
        "receivedDateTime": email.get("receivedDateTime", ""),
        "isRead": email.get("isRead", False),
        "attachments": [
            {
                "id": attachment.get("id", ""),
                "name": attachment.get("name", ""),
                "contentType": attachment.get("contentType", ""),
                "size": attachment.get("size", 0)
            }
            for attachment in email.get("attachments", [])
        ]
    }

def store_emails(emails: list):
    """
    Insert emails into MongoDB if they do not already exist.
    """
    for email in emails:
        try:
            # Pre-process the email data
            processed_email = preprocess_email(email)

            # Validate and parse the email using Pydantic
            validated_email = EmailSchema(**processed_email).model_dump()  # Convert to dictionary for MongoDB
            if not collection.find_one({"id": validated_email["id"]}):
                collection.insert_one(validated_email)

        except Exception as e:
            print(f"[Error] Failed to store email: {e}")

        # Write the retrived email to a file
        with open("my_email_json.json", "w") as f:
            json.dump(emails, f, indent=4)


def fetch_email_count():
    """
    Fetch all emails from MongoDB.
    """
    return collection.count_documents({})

def fetch_emails():
    """
    Fetch all emails from MongoDB.
    """
    return list(collection.find({}))

if __name__ == "__main__":
    # Example usage
    emails = [
        {
            "id": "1",
            "subject": "Test Email",
            "body": "This is a test email.",
            "sender": {"name": "John Doe", "email": "john.doe@example.com"},
            "toRecipients": [{"name": "Jane Smith", "email": "jane.smith@example.com"}],
            "ccRecipients": [],
            "receivedDateTime": "2025-04-19T10:30:00Z",
            "isRead": False,
            "attachments": []
        }
    ]

    # Fetch all emails
    # emails = fetch_emails()
    # num_emails = len(emails)
    # print(f"Fetched {num_emails} emails from the database.")
    # print(f"Total emails in the database: {emails}")

    # List my user contacts
    contacts = list(users_collection.find({}))
    print(f"Fetched {len(contacts)} contacts from the database.")
    print(contacts)
