import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    """Connect to MongoDB NoSQL database."""
    db_url = os.getenv('DATABASE_URL')
    client = MongoClient(db_url)
    return client.height_plateaus
