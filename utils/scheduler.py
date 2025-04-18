"""
Background scheduler that fetches and stores new emails periodically.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from app.graph_api import get_recent_emails
from utils.db_utils import store_emails

def fetch_and_store():
    """
    Fetch recent emails and store them in MongoDB.
    """
    try:
        emails = get_recent_emails()
        store_emails(emails)
        print(f"[Scheduler] Fetched and stored {len(emails)} emails.")
    except Exception as e:
        print(f"[Scheduler Error] {e}")

def start_scheduler():
    """
    Start background scheduler to run every hour.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, "interval", hours=1)
    scheduler.start()
    print("[Scheduler] Started.")
