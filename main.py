from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from uvicorn import run

from database import get_database
from geometry_operations import split_building_limit_by_height_plateau


# Init app and connect to db
app = FastAPI()
db = get_database()


@app.get("/{project_id}/building-limit")
async def read_building_limit(project_id: int):
    return {"project_id": project_id}


@app.post("/{project_id}/building-limit", status_code=status.HTTP_201_CREATED)
async def create_building_limit(project_id: int, request: Request):
    geo_json = await request.body()

    # Save building limit on database
    document = {"test": 'yeahh'}
    await db.projects.insert_one(document)

    # Create split building limits and update on database
    try:
        split_building_limit_by_height_plateau(
            project_id=project_id, building_limit=geo_json
        )
    except Exception as e:
        return {"Split building limit status": e}
    return {"Split building limit status": "success"}


@app.get("/{project_id}/height-plateau")
async def read_height_plateau(project_id: int):
    return {"project_id": project_id}


@app.post("/{project_id}/height-plateau", status_code=status.HTTP_201_CREATED)
async def create_height_plateau(project_id: int, request: Request):
    geo_json = await request.body()

    # Save height plateau on database

    # Create split building limits and update on database
    try:
        split_building_limit_by_height_plateau(
            project_id=project_id, height_plateau=geo_json
        )
    except Exception as e:
        return {"Split building limit status": e}
    return {"Split building limit status": "success"}


@app.get("/{project_id}/split-building-limit")
async def read_split_building_limit(project_id: int):
    return {"project_id": project_id}


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
