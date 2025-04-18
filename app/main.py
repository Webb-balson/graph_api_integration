"""
FastAPI entry point for email service.
Provides endpoints to trigger email send and manual fetch.
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from graph_api import send_mail, get_recent_emails
from utils import scheduler
from utils.db_utils import store_emails

app = FastAPI(title="Graph Email Service")

# Start background scheduler
scheduler.start_scheduler()

class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient: EmailStr

@app.get("/")
def root():
    return {"message": "Graph Email Service is running."}

@app.post("/send-email")
def send_email(req: EmailRequest):
    """
    Send an email via Microsoft Graph.
    """
    try:
        send_mail(req.subject, req.body, req.recipient)
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch-emails")
def fetch_emails():
    """
    Manually fetch and store recent emails.
    """
    try:
        emails = get_recent_emails()
        store_emails(emails)
        return {"message": f"{len(emails)} emails fetched and stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app="main:app", host = "0.0.0.0", port = 8000)