"""
FastAPI entry point for email service.
Provides endpoints to trigger email send and manual fetch.
"""
from typing import Optional
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.graph_api import send_mail, get_recent_emails
from utils import scheduler
from utils.db_utils import store_emails, users_collection, contacts_collection

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Graph Email Service")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Custom exception handler for RateLimitExceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

class EmailRequest(BaseModel):
    subject: str
    body: str
    recipient: EmailStr


app = FastAPI(title="Graph Email Service")

@app.on_event("startup")
async def startup_event():
    """
    Start the scheduler when the application starts.
    """
    scheduler.start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown the scheduler when the application stops.
    """
    scheduler.shutdown()
    print("[Scheduler] Stopped.")

@app.get("/")
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
async def root(request: Request):
    return {"message": "Graph Email Service is running."}

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class Contact(BaseModel):
    user_id: str  # This will be the ObjectId of the user in string format
    contact_name: str
    phone_number: str
    email: EmailStr

@app.post("/create-user")
async def create_user(user: User):
    """
    Create a new user and store it in the users collection.
    """
    try:
        user_data = user.dict()
        result = await users_collection.insert_one(user_data)
        return {"message": "User created successfully.", "user_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.post("/add-contact")
async def add_contact(contact: Contact):
    """
    Add a contact for a specific user.
    """
    try:
        # Ensure the user exists
        user = await users_collection.find_one({"name": contact.user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        contact_data = contact.dict()
        result = await contacts_collection.insert_one(contact_data)
        return {"message": "Contact added successfully.", "contact_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add contact: {str(e)}")

@app.get("/get-user-contacts/{user_id}")
async def get_user_contacts(user_id: str, contact_name: Optional[str] = None):
    """
    Fetch contacts for a specific user by user_id and optionally by contact_name.
    """
    try:
        # Ensure the user exists
        user = await users_collection.find_one({"name": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        # Build the query
        query = {"user_id": user_id}
        if contact_name:
            query["contact_name"] = contact_name

        # Fetch contacts based on the query
        contacts_cursor = contacts_collection.find(query)
        contacts = await contacts_cursor.to_list(length=None)
        for contact in contacts:
            contact["_id"] = str(contact["_id"])  # Convert ObjectId to string for JSON serialization

        return {
            "user": {"id": str(user["_id"]), "name": user["name"], "email": user["email"]},
            "contacts": contacts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user contacts: {str(e)}")


@app.post("/send-email")
async def send_email(req: EmailRequest):
    """
    Send an email via Microsoft Graph.
    """
    try:
        await send_mail(req.subject, req.body, req.recipient)
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch-emails")
async def fetch_emails():
    """
    Manually fetch and store recent emails.
    """
    try:
        emails = await get_recent_emails()
        await store_emails(emails)
        return {"message": f"{len(emails)} emails fetched and stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    async def main():
        config = uvicorn.Config(app="main:app", host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(main())
