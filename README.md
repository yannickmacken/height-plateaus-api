# height-plateaus-api

API service to split building boundary limit into segments by height. User can post 
and update building limits, post and update height lines as GeoJSON. The building 
limits are automatically split with the height lines. Building limits, height lines and 
split building limits can be requested back in GeoJSON format. The project index is 
defined in the url. A new project is created implicitly if user sends new post 
request with building limit or height lines with a non-existant project id in the url.

The following assumptions are made:
- height plateau is passed in request body as GeoJSON featurecollection of Polygons
- building limit is passed in request body as GeoJSON featurecollection of Polygons
- height lines of height plateau are non-overlapping
- height lines of height plateau when joined form single closed polygon
- height lines of height plateau when joined fully cover building limit
- building limit collection contains a single closed polygon

For the API schema, see openapi.json file.

