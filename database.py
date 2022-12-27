import os

from dotenv import load_dotenv

load_dotenv()


def get_database():
    """Connect to MongoDB NoSQL database."""
    db_url = os.getenv('DATABASE_URL')
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    client.get_io_loop = asyncio.get_running_loop
    db = client['height_plateaus']
    return db
