
from typing import Dict, List, Tuple
import math
import json
import urllib.request
import os
from pyproj import Transformer

#_MAP_HEIGHT = 727.0
#_MAP_WIDTH = _MAP_HEIGHT * 2
#_X_OFFSET = 694
#_Y_OFFSET = 66

transformer = Transformer.from_crs('EPSG:4326', 'EPSG:27700')

key = os.environ['DATAPOINT_API_KEY']
context = urllib.request.urlopen(
    f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key={key}"
)

data = json.load(context)
with open('site_list.json', 'w') as outfile:
    json.dump(data, outfile)

def in_range(lat: float, lon: float) -> bool:
    return 49.9 < lat < 58.7 and -7.4 < lon < 1.8


def lat_lon_to_x_y(lat: float, lon: float, min_x: float, max_x: float, min_y: float, max_y: float) -> Tuple[int, int]:
    raw_x, raw_y = transformer.transform(lat, lon)
    x = (raw_x - min_x) / (max_x - min_x) * 38
    y = (raw_y - min_y) / (max_y - min_y) * -59 + 59
    return int(x), int(y)


xy_points: Dict[Tuple[int, int], int] = {}
site_list: List[Tuple[float, float, int, str]] = []

max_x = 0.0
min_x = 1_000_000.0
max_y = 0.0
min_y = 1_000_000.0

for location in data["Locations"]["Location"]:
    lat = float(location["latitude"])
    lon = float(location["longitude"])
    if in_range(lat, lon):
        x, y = transformer.transform(lat, lon)
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

print(f"min={min_x},{min_y}. max={max_x},{max_y}")

for location in data["Locations"]["Location"]:
    lat = float(location["latitude"])
    lon = float(location["longitude"])
    if in_range(lat, lon):
        x, y = lat_lon_to_x_y(
            lat,
            lon,
            min_x,
            max_x,
            min_y,
            max_y
        )

        if not (x, y) in xy_points:
            xy_points[x, y] = 1
            site_list.append((lat, lon, int(location["id"]), location["name"]))

sorted_site_list = sorted(site_list, key=lambda x: (x[0], x[1]))

with open('site_list.py', 'w') as outfile:
    outfile.write("site_list = [\n")
    for item in sorted_site_list:
        outfile.write(f"    {item},\n")
    outfile.write("]\n")

from PIL import Image
image = Image.new('RGB', (64, 64))

density_count = 0
for x in range(64):
    for y in range(64):
        color = 0, 0, 0
        if (x, y) in xy_points:
            if (x, y) in xy_points:
                c = 255
                color = 255, 255, 255

        image.putpixel((x, y), color)

image.save("image.png", "PNG")

