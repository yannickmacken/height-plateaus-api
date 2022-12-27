# height-plateaus-api
API service to split building boundary limit into segments by height

The following assumptions are made:
- height plateau is passed in request body as GeoJSON featurecollection
- building limit is passed in request body as GeoJSON featurecollection
- height lines of height plateau are non-overlapping
- height lines of height plateau when joined form single closed polygon
- height lines of height plateau when joined fully cover building limit
- building limit collection contains a single closed polygon
