from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class EmailSender(BaseModel):
    name: Optional[str]
    email: EmailStr

class EmailRecipient(BaseModel):
    name: Optional[str]
    email: EmailStr

class EmailAttachment(BaseModel):
    id: str
    name: str
    contentType: str
    size: int

class EmailSchema(BaseModel):
    id: str
    subject: str
    body: str
    sender: EmailSender
    toRecipients: List[EmailRecipient]
    ccRecipients: Optional[List[EmailRecipient]] = []
    receivedDateTime: datetime
    isRead: bool
    attachments: Optional[List[EmailAttachment]] = []
