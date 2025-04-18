"""
Handles MongoDB operations for storing and retrieving emails.
"""

from pymongo import MongoClient
from configs import config

client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]

def store_emails(emails: list):
    """
    Insert emails into MongoDB if they do not already exist.
    """
    for email in emails:
        if not collection.find_one({"id": email["id"]}):
            collection.insert_one(email)

def insert_record(record: dict):
    """
    Insert a single record into MongoDB.
    """
    collection.insert_one(record)


if __name__ == "__main__":
    # Example usage
    emails = [
        {"id": "1", "subject": "Test Email 1", "body": "This is a test email."},
        {"id": "2", "subject": "Test Email 2", "body": "This is another test email."}
    ]
    # store_emails(emails)
    # Insert a single record
    record = {"id": "3", "subject": "Test Email 3", "body": "This is a third test email."}
    insert_record(record)
    # Check if the record was inserted     
    inserted_record = collection.find_one({"id": "3"})
    if inserted_record:
        print(f"Inserted record: {inserted_record}")
    else:
        print("Record not found.")