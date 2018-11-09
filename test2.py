import googlemaps
from datetime import datetime
import pprint

gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Geocoding an address
geocode_result = gmaps.geocode('mckinsey hq california')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)


pprint.pprint(geocode_result)
#print(directions_result)