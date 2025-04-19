"""
Background scheduler that fetches and stores new emails periodically.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.graph_api import get_recent_emails
from utils.db_utils import store_emails
import asyncio

async def fetch_and_store():
    """
    Fetch recent emails and store them in MongoDB.
    """
    try:
        emails = await get_recent_emails()
        await store_emails(emails)
        print(f"[Scheduler] Fetched and stored {len(emails)} emails.")
    except Exception as e:
        print(f"[Scheduler Error] {e}")

# Initialize the scheduler
scheduler = AsyncIOScheduler()

def start_scheduler():
    """
    Start the background scheduler.
    """
    # Add a job to fetch and store emails every hour
    scheduler.add_job(lambda: asyncio.create_task(fetch_and_store()), "interval", hours=1)
    scheduler.start()
    print("[Scheduler] Started.")