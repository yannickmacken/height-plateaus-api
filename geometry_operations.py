from typing import List, Dict, Tuple, Optional

from shapely import MultiPolygon
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon, orient


def parse_feature_collection(geo_json: Dict) -> List[Tuple[Polygon, Dict]]:
    """Convert feature collection into list of polygons and properties."""
    feature_list = []
    for feature in geo_json["features"]:
        feature_list.append(parse_feature(feature))
    return feature_list


def parse_feature(feature: Dict) -> Tuple[Polygon, Dict]:
    """Convert feature geometry to polygon and extract properties."""
    polygon: Polygon = shape(feature["geometry"])
    props = feature.get("properties", {})
    return polygon, props


def add_polygon_to_collection(collection: Dict, polygon: Polygon, props: Dict):
    """Adds polygon geometry and props to GeoJSON collection."""
    intersection = orient(polygon, 1)  # Exterior counter-clockwise
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
    collection["features"].append(feature)


def split_building_limit_by_height(
    building_limit: Dict,
    height_plateau: Dict,
) -> Optional[Dict]:
    """Split building limit (GeoJSON) by height plateau (GeoJSON), and return
    resulting 'split building limits' as GeoJSON."""

    # Parse GeoJSONs to shapely polygons and properties
    parsed_building_limits = parse_feature_collection(building_limit)
    parsed_height_plateaus = parse_feature_collection(height_plateau)
    building_limit_polygon, _ = parsed_building_limits[0]

    # Initialize empty feature collection GeoJSON for split building limits
    split_building_limits_geo_json = {
            "type": "FeatureCollection",
            "features": []
        }

    # Split building limits by height plateaus
    for polygon, props in parsed_height_plateaus:
        intersection = building_limit_polygon.intersection(polygon)

        # If resulting overlap is polygon, add to collection
        if intersection and isinstance(intersection, Polygon):
            add_polygon_to_collection(
                split_building_limits_geo_json, intersection, props
            )

        # If resulting overlap is multi-polygon, add all to collection
        elif isinstance(intersection, MultiPolygon):
            for sub_polygon in list(intersection.geoms):
                if isinstance(sub_polygon, Polygon):
                    add_polygon_to_collection(
                        split_building_limits_geo_json, sub_polygon, props
                    )

    # Return GeoJSON string of split building limits
    return split_building_limits_geo_json
