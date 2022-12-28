import json
from pathlib import Path

from fastapi.testclient import TestClient
import unittest

from main import app


client = TestClient(app)


class TestAPI(unittest.TestCase):
    """Test class for API."""

    # Setup
    project_id = 1
    base_path = Path(__file__).parent
    building_limit = base_path / "test_files" / "1" / "building_limits.geojson"
    height_plateaus = base_path / "test_files" / "1" / "height_plateaus.geojson"
    with open(building_limit, "rb") as stream:
        building_limit_json = json.load(stream)
    with open(height_plateaus, "rb") as stream:
        height_plateaus_json = json.load(stream)

    def test_read_building_limit(self):
        response = client.get(f"/{self.project_id}/building-limit")
        self.assertEqual(response.status_code, 200)

    def test_create_building_limit(self):
        response = client.post(
            url=f"/{self.project_id}/building-limit",
            json=self.building_limit_json
        )
        self.assertEqual(response.status_code, 201)

    def test_read_height_plateau(self):
        response = client.get(f"/{self.project_id}/height-plateau")
        self.assertEqual(response.status_code, 200)

    def test_create_height_plateau(self):
        response = client.post(
            url=f"/{self.project_id}/height-plateau",
            json=self.height_plateaus_json
        )
        self.assertEqual(response.status_code, 201)

    def test_read_split_building_limit(self):
        response = client.get(f"/{self.project_id}/split-building-limit")
        self.assertEqual(response.status_code, 200)
