"""
FastAPI entry point for email service.
Provides endpoints to trigger email send and manual fetch.
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from graph_api import send_mail, get_recent_emails
from utils import scheduler
from utils.db_utils import store_emails

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Graph Email Service")
app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, lambda request, exc: HTTPException(status_code=429, detail="Rate limit exceeded"))
app.add_middleware(SlowAPIMiddleware)

# Custom exception handler for RateLimitExceeded
@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

# Start background scheduler
scheduler.start_scheduler()

class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient: EmailStr

@app.get("/")
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
def root(request: Request):
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