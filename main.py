import json

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from database import get_database, save_geometry_to_database, get_geometry_from_database
from geometry_operations import split_building_limit_by_height


# Init app and connect to database
app = FastAPI()
db = get_database()


@app.get("/{project_id}/building-limit")
async def read_building_limit(project_id: int):
    """Get building limit GeoJSON from database."""
    building_limit = await get_geometry_from_database(db, project_id, 'building_limit')
    return building_limit


@app.post("/{project_id}/building-limit", status_code=status.HTTP_201_CREATED)
async def create_building_limit(project_id: int, request: Request):
    """Save building limit GeoJSON to db. If height plateau is determined for project,
    calculate and save building limits split by height plateau."""

    # Load GeoJSON object to Dict
    geo_json = await request.body()
    building_limit = json.loads(geo_json)

    # Save building limit to database
    await save_geometry_to_database(db, project_id, building_limit, 'building_limit')

    # Create split building limits and save to database
    height_plateau = await get_geometry_from_database(db, project_id, 'height_plateau')
    if height_plateau:
        split_building_limit = split_building_limit_by_height(
            building_limit, height_plateau
        )
        await save_geometry_to_database(
            db, project_id, split_building_limit, 'split_building_limit'
        )

    # Return string
    return_string = "Building limit created"
    if height_plateau:
        return_string += " and split by height plateau"
    return return_string


@app.get("/{project_id}/height-plateau")
async def read_height_plateau(project_id: int):
    """Get height plateau GeoJSON from database."""
    height_plateau = await get_geometry_from_database(db, project_id, 'height_plateau')
    return height_plateau


@app.post("/{project_id}/height-plateau", status_code=status.HTTP_201_CREATED)
async def create_height_plateau(project_id: int, request: Request):
    """Save height plateau GeoJSON to database. If building limit is determined for
    project, calculate and save building limits split by height plateau."""

    # Load GeoJSON object to Dict
    geo_json = await request.body()
    height_plateau = json.loads(geo_json)

    # Save height plateau to database
    await save_geometry_to_database(db, project_id, height_plateau, 'height_plateau')

    # Create split building limits and save to database
    building_limit = await get_geometry_from_database(db, project_id, 'building_limit')
    if building_limit:
        split_building_limit = split_building_limit_by_height(
            building_limit, height_plateau
        )
        await save_geometry_to_database(
            db, project_id, split_building_limit, 'split_building_limit'
        )

    # Return string
    return_string = "Height plateau created"
    if building_limit:
        return_string += " and building limit split"
    return return_string


@app.get("/{project_id}/split-building-limit")
async def read_split_building_limit(project_id: int):
    """Get split building limit GeoJSON from database."""
    split_building_limit = await get_geometry_from_database(
        db, project_id, 'split_building_limit'
    )
    return split_building_limit
