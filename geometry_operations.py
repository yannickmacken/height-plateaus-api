from json import loads
from pathlib import Path
from typing import List, Dict, Tuple

from shapely.geometry import shape
from shapely.geometry.polygon import Polygon


def parse_feature_collection(geo_json: bytes) -> List[Tuple[Polygon, Dict]]:
    """Convert feature collection into list of polygons and properties."""
    feature_collection = loads(geo_json)
    feature_list = []
    for feature in feature_collection["features"]:
        feature_list.append(parse_feature(feature))
    return feature_list


def parse_feature(feature: Dict) -> Tuple[Polygon, Dict]:
    """Convert feature geometry to polygon and extract properties."""
    polygon: Polygon = shape(feature["geometry"])
    props = feature.get("properties", {})
    return polygon, props


def split_building_limit_by_height_plateau(
    building_limit: bytes = None,
    height_plateau: bytes = None,
):
    """Split building limit (GeoJSON) by height plateau (GeoJSON), and save
    resulting 'split building limits' to NoSQL database."""

    # Get building limit or height plateaus from database
    if not building_limit:
        building_limit = Path.read_bytes(
            Path(__file__).parent / "test_files" / "building_limit.json"
        )
    if not height_plateau:
        height_plateau = Path.read_bytes(
            Path(__file__).parent / "test_files" / "height_plateau.json"
        )

    # Parse GeoJSONs to shapely polygons and properties
    parsed_building_limits = parse_feature_collection(building_limit)
    parsed_height_plateaus = parse_feature_collection(height_plateau)
    if len(parsed_building_limits) != 1:
        raise Exception("One building limit allowed/required.")
    if len(parsed_height_plateaus) < 1:
        raise Exception("At least one height plateau polygon required.")
    building_limit_polygon, _ = parsed_building_limits[0]

    # Initialize empty featurecollection GeoJSON for split building limits
    split_building_limits_geo_json = {
            "type": "FeatureCollection",
            "features": []
        }

    # Split building limits by height plateaus
    for polygon, props in parsed_height_plateaus:
        intersection = building_limit_polygon.intersection(polygon)
        print("intersection", intersection)
        if intersection and isinstance(intersection, Polygon):

            # Add feature to split building limits GeoJSON
            feature = {
                "type": "Feature",
                "properties": {
                    "height": props["height"]
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        list(c) for c in list(intersection.exterior.coords)
                    ]]
                }
            }
            split_building_limits_geo_json["features"].append(feature)

    print("features", split_building_limits_geo_json)
