

# # Leaflet cluster map of talk locations
#
# (c) 2016-2017 R. Stuart Geiger, released under the MIT license
#
# Run this from the _talks/ directory, which contains .md files of all your talks. 
# This scrapes the location YAML field from each .md file, geolocates it with
# geopy/Nominatim, and uses the getorg library to output data, HTML,
# and Javascript for a standalone cluster map.
#
# Requires: glob, getorg, geopy

import glob
import getorg
from geopy import Nominatim

g = glob.glob("*.md")


# geopy >= 2.0 requires a user agent when using Nominatim.
# Without it a `TypeError` will be raised on initialization.
geocoder = Nominatim(user_agent="talkmap")
location_dict = {}
permalink = ""
title = ""


for file in g:
    with open(file, 'r') as f:
        lines = f.read()

    location = ""
    if 'location: "' in lines:
        loc_start = lines.find('location: "') + 11
        lines_trim = lines[loc_start:]
        loc_end = lines_trim.find('"')
        location = lines_trim[:loc_end]

    if location:
        geocoded = geocoder.geocode(location)
        if geocoded:
            location_dict[location] = geocoded
            print(location, "\n", geocoded)


m = getorg.orgmap.create_map_obj()
getorg.orgmap.output_html_cluster_map(location_dict, folder_name="../talkmap", hashed_usernames=False)




