import asyncio
import os
from typing import Dict, Optional

import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi import HTTPException
from starlette import status


load_dotenv()


def get_database():
    """Connect to MongoDB NoSQL database."""
    db_url = os.getenv('MONGO_URL')
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    client.get_io_loop = asyncio.get_running_loop  # Match motor loop to existing loop
    db = client['height_plateaus']
    return db


async def save_geometry_to_database(db, project_id: int, geo_json: Dict, key: str):
    """Save GeoJSON to MongoDB database, on document with project_id.
    If document with project_id does not exist, create document (upsert).
    Return result id."""

    # Save geometry to database
    result = await db.projects.update_one(
        filter={'project_id': project_id},
        update={'$set': {key: geo_json}},
        upsert=True
    )

    # If no match, modification or document added, raise HTTP Exception
    if not any([result.matched_count, result.modified_count, result.upserted_id]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{project_id} - {key} could not be updated in database."
        )


async def get_geometry_from_database(db, project_id: int, key: str) -> Optional[Dict]:
    """Get GeoJSON from MongoDB database, from document with project_id.
    If document with project_id does not exist, return None."""

    document = await db.projects.find_one(filter={'project_id': project_id})
    if document:
        return document.get(key, None)
    return None
