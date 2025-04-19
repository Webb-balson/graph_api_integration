import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import AsyncClient  # Use FastAPI's AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_send_email():
    """
    Test the /send-email endpoint.
    """
    # Mock the send_mail function
    with patch("app.graph_api.send_mail", new_callable=AsyncMock) as mock_send_mail:
        mock_send_mail.return_value = None  # Simulate successful email sending

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/send-email",
                json={
                    "subject": "Test Subject",
                    "body": "Test Body",
                    "recipient": "test@example.com"
                }
            )

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"message": "Email sent successfully."}
        mock_send_mail.assert_awaited_once_with("Test Subject", "Test Body", "test@example.com")

@pytest.mark.asyncio
async def test_fetch_emails():
    """
    Test the /fetch-emails endpoint.
    """
    # Mock the get_recent_emails and store_emails functions
    with patch("app.graph_api.get_recent_emails", new_callable=AsyncMock) as mock_get_recent_emails, \
         patch("app.main.store_emails", new_callable=AsyncMock) as mock_store_emails:
        
        mock_get_recent_emails.return_value = [
            {"id": "1", "subject": "Test Email", "body": "Test Body"}
        ]  # Simulate fetching emails
        mock_store_emails.return_value = None  # Simulate successful storage

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/fetch-emails")

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"message": "1 emails fetched and stored."}
        mock_get_recent_emails.assert_awaited_once()
        mock_store_emails.assert_awaited_once_with([
            {"id": "1", "subject": "Test Email", "body": "Test Body"}
        ])