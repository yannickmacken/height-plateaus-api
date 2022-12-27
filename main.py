from fastapi import FastAPI
from starlette.requests import Request
from uvicorn import run

from geometry_operations import split_building_limit_by_height_plateau

app = FastAPI()


@app.get("/{project_id}/building-limit")
async def read_building_limit(project_id: int):
    return {"project_id": project_id}


@app.post("/{project_id}/building-limit")
async def create_building_limit(project_id: int, request: Request):
    geo_json = await request.body()

    # Create split building limits and update on database
    split_building_limit_by_height_plateau(building_limit=geo_json)

    # Save building limit on database

    return {"request": await request.body()}


@app.get("/{project_id}/height-plateau")
async def read_height_plateau(project_id: int):
    return {"project_id": project_id}


@app.post("/{project_id}/height-plateau")
async def create_height_plateau(project_id: int, request: Request):
    geo_json = await request.body()

    # Create split building limits and update on database
    split_building_limit_by_height_plateau(height_plateau=geo_json)

    # Save height plateau on database

    return {"project_id": project_id}


@app.get("/{project_id}/split-building-limit")
async def read_split_building_limit(project_id: int):
    return {"project_id": project_id}


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
